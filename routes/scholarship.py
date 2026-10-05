import os
import json
import uuid
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    jsonify,
    send_file,
    abort,
    current_app
)
from sqlalchemy import or_, and_, func
from werkzeug.utils import secure_filename

from extensions import db
from models.scholarship import (
    Scholarship,
    ScholarshipCycle,
    ScholarshipApplication,
    ScholarshipField,
    StudentDocument,
    ScholarshipApplicationDocument,
    ScholarshipApplicationClick,
    is_valid_http_url
)
from models.saved_opportunity import SavedOpportunity
from models.user import User
from models.student_profile import StudentProfile
from services.scholarship_eligibility import eligibility_engine

scholarship = Blueprint(
    "scholarship",
    __name__,
    url_prefix="/scholarships"
)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_student_data():
    """Helper to assemble student attributes from session, User, and StudentProfile"""
    data = {
        "full_name": "",
        "state": "",
        "district": "",
        "gender": "",
        "category": "",
        "class_grade": "",
        "course": "",
        "education_level": "",
        "family_income": "",
        "percentage": "",
        "is_disabled": False,
        "college_name": ""
    }

    if not session.get("user_id"):
        return data

    user = User.query.get(session["user_id"])
    if not user:
        return data

    data["full_name"] = user.full_name or ""
    data["state"] = user.state or ""
    data["district"] = user.district or ""
    data["class_grade"] = user.class_grade or ""
    data["course"] = user.course or ""
    data["education_level"] = user.class_grade or ""
    data["college_name"] = user.college_name or ""

    profile = StudentProfile.query.filter_by(user_id=user.id).first()
    if profile:
        if profile.state:
            data["state"] = profile.state
        if profile.district:
            data["district"] = profile.district
        if profile.current_class:
            data["class_grade"] = profile.current_class
            data["education_level"] = profile.current_class
        if profile.school_college:
            data["college_name"] = profile.school_college

    return data


# =========================================================================
# 1. SCHOLARSHIP DISCOVERY EXPLORER (Search, Filters, Pagination)
# =========================================================================

@scholarship.route("/")
def scholarship_list():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    state = request.args.get("state", "").strip()
    provider_type = request.args.get("provider_type", "").strip()
    edu_level = request.args.get("level", "").strip()
    gender = request.args.get("gender", "").strip()
    income = request.args.get("income", type=float)
    status_filter = request.args.get("status", "").strip()
    sort_by = request.args.get("sort", "closing_soon").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 12

    query = Scholarship.query

    # Search Filter
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Scholarship.title.ilike(pattern),
                Scholarship.short_title.ilike(pattern),
                Scholarship.provider.ilike(pattern),
                Scholarship.provider_name.ilike(pattern),
                Scholarship.category.ilike(pattern),
                Scholarship.sub_category.ilike(pattern),
                Scholarship.eligibility.ilike(pattern),
                Scholarship.description.ilike(pattern),
                Scholarship.ministry.ilike(pattern),
                Scholarship.state.ilike(pattern),
                Scholarship.streams.ilike(pattern),
                Scholarship.courses.ilike(pattern)
            )
        )

    # Category Filter
    if category and category != "All":
        query = query.filter(Scholarship.category.ilike(f"%{category}%"))

    # State Filter
    if state and state != "All":
        query = query.filter(
            or_(
                Scholarship.state.ilike(f"%{state}%"),
                Scholarship.state == "All India",
                Scholarship.national_or_state == "National"
            )
        )

    # Provider Type Filter
    if provider_type and provider_type != "All":
        query = query.filter(Scholarship.provider_type.ilike(f"%{provider_type}%"))

    # Education Level Filter
    if edu_level and edu_level != "All":
        query = query.filter(
            or_(
                Scholarship.education_level.ilike(f"%{edu_level}%"),
                Scholarship.education_level.is_(None)
            )
        )

    # Gender Eligibility Filter
    if gender and gender != "All":
        if gender.lower() == "female only":
            query = query.filter(Scholarship.gender_eligibility.ilike("%female%"))
        else:
            query = query.filter(Scholarship.gender_eligibility.in_(["All", gender]))

    # Income Limit Filter
    if income:
        query = query.filter(
            or_(
                Scholarship.family_income_limit >= income,
                Scholarship.family_income_limit.is_(None),
                Scholarship.family_income_limit == 0
            )
        )

    # Cycle Status Filter
    if status_filter:
        query = query.join(ScholarshipCycle).filter(ScholarshipCycle.status == status_filter)

    # Sorting
    if sort_by == "name_asc":
        query = query.order_by(Scholarship.title.asc())
    elif sort_by == "name_desc":
        query = query.order_by(Scholarship.title.desc())
    elif sort_by == "state":
        query = query.order_by(Scholarship.state.asc(), Scholarship.title.asc())
    else:
        # Default: verified first, then ID
        query = query.order_by(
            func.coalesce(Scholarship.verification_status, "VERIFIED").desc(),
            Scholarship.id.asc()
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    scholarships = pagination.items

    # Filter Options
    categories_raw = db.session.query(Scholarship.category).distinct().all()
    categories = sorted([c[0] for c in categories_raw if c[0]])

    states_raw = db.session.query(Scholarship.state).distinct().all()
    all_states = sorted([s[0] for s in states_raw if s[0] and s[0] != "All India"])

    provider_types_raw = db.session.query(Scholarship.provider_type).distinct().all()
    provider_types = sorted([pt[0] for pt in provider_types_raw if pt[0]])

    saved_scholarship_ids = set()
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="scholarship"
        ).all()
        saved_scholarship_ids = {s.item_id for s in user_saved}

    # Summary metrics for header banner
    total_count = Scholarship.query.count()
    central_count = Scholarship.query.filter_by(provider_type="Central Government").count()
    state_count = Scholarship.query.filter_by(provider_type="State Government").count()
    csr_count = Scholarship.query.filter(
        or_(
            Scholarship.provider_type.ilike("%CSR%"),
            Scholarship.provider_type.ilike("%Trust%")
        )
    ).count()

    return render_template(
        "scholarship/list.html",
        scholarships=scholarships,
        pagination=pagination,
        categories=categories,
        states=all_states,
        provider_types=provider_types,
        search=search,
        selected_category=category,
        selected_state=state,
        selected_provider_type=provider_type,
        selected_level=edu_level,
        selected_gender=gender,
        selected_income=income,
        selected_status=status_filter,
        selected_sort=sort_by,
        saved_scholarship_ids=saved_scholarship_ids,
        metrics={
            "total": total_count,
            "central": central_count,
            "state": state_count,
            "csr": csr_count
        }
    )


# =========================================================================
# 2. SCHOLARSHIP DOSSIER (Comprehensive Profile View)
# =========================================================================

@scholarship.route("/<identifier>", endpoint="scholarship_detail")
@scholarship.route("/details/<identifier>", endpoint="scholarship_details")
def scholarship_detail(identifier):
    # Support lookup by numeric ID or URL slug
    if identifier.isdigit():
        sch = Scholarship.query.get_or_404(int(identifier))
    else:
        sch = Scholarship.query.filter_by(slug=identifier).first_or_404()

    # Active Cycle
    cycle = sch.active_cycle

    # Saved status
    is_saved = False
    if session.get("user_id"):
        is_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="scholarship",
            item_id=sch.id
        ).first() is not None

    # Student Match Evaluation if logged in
    match_eval = None
    if session.get("user_id"):
        st_data = get_current_student_data()
        match_eval = eligibility_engine.evaluate(sch, st_data)

    # Similar Scholarships
    similar = Scholarship.query.filter(
        Scholarship.category == sch.category,
        Scholarship.id != sch.id
    ).limit(3).all()

    # User Application in Progress for this scholarship (if any)
    user_app = None
    if session.get("user_id"):
        user_app = ScholarshipApplication.query.filter_by(
            user_id=session["user_id"],
            scholarship_id=sch.id
        ).order_by(ScholarshipApplication.created_at.desc()).first()

    return render_template(
        "scholarship/details.html",
        scholarship=sch,
        cycle=cycle,
        is_saved=is_saved,
        match_eval=match_eval,
        similar=similar,
        user_app=user_app
    )


# =========================================================================
# 2B. CONTROLLED APPLICATION REDIRECT & ANALYTICS (SECTIONS 8, 9, 10, 12)
# =========================================================================

@scholarship.route("/<identifier>/apply-redirect", endpoint="apply_redirect")
@scholarship.route("/apply-redirect/<identifier>", endpoint="apply_redirect_alt")
@scholarship.route("/<identifier>/redirect", endpoint="apply_redirect_legacy")
def apply_redirect(identifier):
    """
    Controlled application redirect flow enforcing:
    1. Validation of URL (no javascript:, data:, localhost, etc.)
    2. Distinction between official_website and official_application_url
    3. Deadline awareness (blocks apply if cycle is closed)
    4. Safe recording of outbound click analytics (never capturing student credentials)
    5. Departure warning page before transferring to external portal
    """
    if str(identifier).isdigit():
        sch = Scholarship.query.get_or_404(int(identifier))
    else:
        sch = Scholarship.query.filter_by(slug=str(identifier)).first_or_404()

    cycle = sch.active_cycle
    meta = sch.apply_button_meta

    # 1. Deadline check
    if cycle and cycle.status == "CLOSED":
        return render_template(
            "scholarship/apply_unavailable.html",
            scholarship=sch,
            cycle=cycle,
            meta=meta,
            reason="The application window for this scholarship cycle is closed."
        ), 200

    # 2. Check if valid application URL exists
    target_url = sch.resolved_application_url
    if not target_url or not is_valid_http_url(target_url) or not sch.has_direct_apply:
        return render_template(
            "scholarship/apply_unavailable.html",
            scholarship=sch,
            cycle=cycle,
            meta=meta,
            reason="An official direct application link is currently unavailable or undergoing statutory verification."
        ), 200

    # 3. Safe Outbound Click Analytics (SECTION 9: NEVER capture credentials/OTPs)
    click_source = request.args.get("source", "detail_page").strip()
    try:
        user_id = session.get("user_id")
        click = ScholarshipApplicationClick(
            scholarship_id=sch.id,
            user_id=user_id,
            cycle_id=cycle.id if cycle else None,
            target_url=target_url,
            click_source=click_source[:50]
        )
        db.session.add(click)
        db.session.commit()
    except Exception:
        db.session.rollback()

    # 4. Immediate redirect if confirmed, otherwise display departure advisory
    confirm = request.args.get("confirm", "0").strip()
    if confirm == "1":
        return redirect(target_url)

    return render_template(
        "scholarship/redirect_departure.html",
        scholarship=sch,
        cycle=cycle,
        target_url=target_url,
        official_website=sch.resolved_official_website
    )


# =========================================================================
# 3. "FIND SCHOLARSHIPS FOR ME" (Personalized Discovery & Evaluation)
# =========================================================================

@scholarship.route("/find-for-me", methods=["GET", "POST"], endpoint="find_scholarships_for_me")
@scholarship.route("/find", methods=["GET", "POST"], endpoint="find_for_me")
def find_scholarships_for_me():
    # Pre-populate from session if available
    st_data = get_current_student_data()

    if request.method == "POST":
        st_data["education_level"] = request.form.get("education_level", st_data["education_level"]).strip()
        st_data["course"] = request.form.get("course", st_data["course"]).strip()
        st_data["state"] = request.form.get("state", st_data["state"]).strip()
        st_data["gender"] = request.form.get("gender", st_data["gender"]).strip()
        st_data["category"] = request.form.get("category", st_data["category"]).strip()
        st_data["family_income"] = request.form.get("family_income", st_data["family_income"]).strip()
        st_data["percentage"] = request.form.get("percentage", st_data["percentage"]).strip()
        st_data["is_disabled"] = request.form.get("is_disabled") == "1"

    # Evaluate against all verified scholarships
    all_scholarships = Scholarship.query.filter(
        Scholarship.verification_status.in_(["VERIFIED", "NEEDS_REVIEW"])
    ).all()

    evaluated = eligibility_engine.match_all(all_scholarships, st_data)

    # Group into categories for student clarity
    strong_matches = [e for e in evaluated if e["status"] == "ELIGIBLE"]
    likely_matches = [e for e in evaluated if e["status"] == "LIKELY_ELIGIBLE"]
    partial_matches = [e for e in evaluated if e["status"] == "PARTIALLY_MATCHED"]
    ineligible = [e for e in evaluated if e["status"] == "NOT_ELIGIBLE"]

    saved_scholarship_ids = set()
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="scholarship"
        ).all()
        saved_scholarship_ids = {s.item_id for s in user_saved}

    # Distinct states for form dropdown
    states_raw = db.session.query(Scholarship.state).distinct().all()
    all_states = sorted([s[0] for s in states_raw if s[0] and s[0] != "All India"])

    return render_template(
        "scholarship/find_for_me.html",
        student_data=st_data,
        strong_matches=strong_matches,
        likely_matches=likely_matches,
        partial_matches=partial_matches,
        ineligible_count=len(ineligible),
        states=all_states,
        saved_scholarship_ids=saved_scholarship_ids,
        has_searched=(request.method == "POST" or bool(session.get("user_id")))
    )


# =========================================================================
# 4. INSTANT ELIGIBILITY CHECK API ("Why Am I Eligible?")
# =========================================================================

@scholarship.route("/api/check-eligibility", methods=["POST"])
def api_check_eligibility():
    payload = request.get_json() or {}
    sch_id = payload.get("scholarship_id")
    if not sch_id:
        return jsonify({"success": False, "error": "scholarship_id is required"}), 400

    sch = Scholarship.query.get_or_404(sch_id)

    # Combine provided student data with saved profile if authenticated
    st_data = get_current_student_data()
    for k in ["state", "gender", "category", "family_income", "percentage", "education_level", "course"]:
        if payload.get(k):
            st_data[k] = payload.get(k)
    if "is_disabled" in payload:
        st_data["is_disabled"] = bool(payload.get("is_disabled"))

    eval_result = eligibility_engine.evaluate(sch, st_data)
    return jsonify({
        "success": True,
        "scholarship_id": sch.id,
        "scholarship_title": sch.title,
        "evaluation": eval_result
    })


# =========================================================================
# 5. ONE APPLICATION EXPERIENCE (Application Readiness & Initiation)
# =========================================================================

@scholarship.route("/apply/<int:scholarship_id>", methods=["GET", "POST"])
def apply_scholarship(scholarship_id):
    if "user_id" not in session:
        flash("Please log in to initiate and manage your scholarship application.", "info")
        return redirect(url_for("auth.login", next=request.url))

    sch = Scholarship.query.get_or_404(scholarship_id)
    user = User.query.get(session["user_id"])
    cycle = sch.active_cycle

    # Retrieve or create draft application
    app_record = ScholarshipApplication.query.filter_by(
        user_id=user.id,
        scholarship_id=sch.id
    ).first()

    if not app_record:
        ref_num = f"MPATH-SCH-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
        app_record = ScholarshipApplication(
            user_id=user.id,
            scholarship_id=sch.id,
            cycle_id=cycle.id if cycle else None,
            application_number=ref_num,
            status="DRAFT",
            submission_type="EXTERNAL_PORTAL_PREPARED" if sch.application_method == "EXTERNAL_PORTAL" else "MPATH_ASSISTED",
            progress_percent=25
        )
        db.session.add(app_record)
        db.session.commit()

    # Evaluate eligibility snapshot
    st_data = get_current_student_data()
    eval_result = eligibility_engine.evaluate(sch, st_data)
    app_record.eligibility_snapshot = json.dumps(eval_result)
    db.session.commit()

    # Load dynamic fields for this scholarship (or global fields)
    fields = ScholarshipField.query.filter(
        or_(
            ScholarshipField.scholarship_id == sch.id,
            ScholarshipField.scholarship_id.is_(None)
        )
    ).order_by(ScholarshipField.order).all()

    # User's uploaded documents in their vault
    user_documents = StudentDocument.query.filter_by(user_id=user.id).all()

    # Form Submission Handler
    if request.method == "POST":
        action = request.form.get("action", "save_draft")

        # Capture dynamic fields
        form_payload = {}
        for f in fields:
            val = request.form.get(f.field_name, "").strip()
            form_payload[f.field_name] = val
        app_record.form_data = json.dumps(form_payload)

        # External reference number if student has already registered on official portal
        ext_ref = request.form.get("external_reference_number", "").strip()
        if ext_ref:
            app_record.external_reference_number = ext_ref

        # Student notes
        app_record.student_notes = request.form.get("student_notes", "").strip()

        # Handle Action
        if action == "save_draft":
            app_record.status = "DRAFT"
            app_record.progress_percent = 50
            db.session.commit()
            flash("Application draft saved successfully. You can continue anytime!", "success")
            return redirect(url_for("scholarship.apply_scholarship", scholarship_id=sch.id))

        elif action == "continue_to_portal":
            # Officially initiated
            app_record.status = "SUBMITTED"
            app_record.progress_percent = 85
            app_record.submitted_at = datetime.now()
            db.session.commit()
            flash(
                "Application preparation completed! Redirecting you to the official scholarship portal. Remember to keep your application reference safe.",
                "success"
            )
            portal_url = sch.resolved_application_url
            if not portal_url or not is_valid_http_url(portal_url):
                flash("Direct online application link is currently unavailable for this scheme.", "warning")
                return redirect(url_for("scholarship.apply_redirect", identifier=sch.id))

            # Record click analytics safely
            try:
                click = ScholarshipApplicationClick(
                    scholarship_id=sch.id,
                    user_id=user.id,
                    cycle_id=cycle.id if cycle else None,
                    target_url=portal_url,
                    click_source="preparation_wizard"
                )
                db.session.add(click)
                db.session.commit()
            except Exception:
                db.session.rollback()

            return redirect(url_for("scholarship.apply_redirect", identifier=sch.id, confirm="1"))

        elif action == "mpath_submit":
            app_record.status = "SUBMITTED"
            app_record.progress_percent = 100
            app_record.submitted_at = datetime.now()
            db.session.commit()
            flash(f"Application #{app_record.application_number} successfully registered in your MPath dashboard!", "success")
            return redirect(url_for("scholarship.my_applications"))

    # Calculate profile completion for this application
    saved_answers = app_record.parsed_form_data
    filled_fields = sum(1 for f in fields if saved_answers.get(f.field_name))
    completion_rate = int((filled_fields / len(fields)) * 100) if fields else 100

    return render_template(
        "scholarship/apply.html",
        scholarship=sch,
        cycle=cycle,
        application=app_record,
        fields=fields,
        user_documents=user_documents,
        eval_result=eval_result,
        student_data=st_data,
        saved_answers=saved_answers,
        completion_rate=completion_rate
    )


# =========================================================================
# 6. "MY SCHOLARSHIP APPLICATIONS" DASHBOARD & TRACKING
# =========================================================================

@scholarship.route("/my-applications")
def my_applications():
    if "user_id" not in session:
        flash("Please log in to view your scholarship applications.", "info")
        return redirect(url_for("auth.login", next=request.url))

    user_id = session["user_id"]
    applications = (
        ScholarshipApplication.query.filter_by(user_id=user_id)
        .order_by(ScholarshipApplication.updated_at.desc())
        .all()
    )

    # Metrics
    total_apps = len(applications)
    in_progress = sum(1 for a in applications if a.status in ["DRAFT", "FORM_IN_PROGRESS", "PROFILE_INCOMPLETE", "DOCUMENTS_PENDING"])
    submitted = sum(1 for a in applications if a.status in ["SUBMITTED", "READY_TO_SUBMIT"])
    verified = sum(1 for a in applications if a.status in ["INSTITUTE_VERIFICATION", "DEPARTMENT_VERIFICATION"])
    approved = sum(1 for a in applications if a.status in ["APPROVED", "PAYMENT_PENDING", "PAYMENT_RECEIVED"])

    return render_template(
        "scholarship/my_applications.html",
        applications=applications,
        metrics={
            "total": total_apps,
            "in_progress": in_progress,
            "submitted": submitted,
            "verified": verified,
            "approved": approved
        }
    )


# =========================================================================
# 7. UPDATE APPLICATION STATUS (Manual Student Progress Sync)
# =========================================================================

@scholarship.route("/application/<int:app_id>/update-status", methods=["POST"])
def update_application_status(app_id):
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    app_record = ScholarshipApplication.query.get_or_404(app_id)
    if app_record.user_id != session["user_id"]:
        return jsonify({"success": False, "error": "Access denied"}), 403

    new_status = request.form.get("status")
    ext_ref = request.form.get("external_reference_number")
    notes = request.form.get("notes")

    valid_statuses = [
        "DRAFT", "READY_TO_SUBMIT", "SUBMITTED", "INSTITUTE_VERIFICATION",
        "DEPARTMENT_VERIFICATION", "CORRECTION_REQUIRED", "APPROVED",
        "REJECTED", "PAYMENT_PENDING", "PAYMENT_RECEIVED", "CLOSED"
    ]

    if new_status in valid_statuses:
        app_record.status = new_status
        app_record.user_declared_status = new_status
        app_record.user_declared_status_updated_at = datetime.now()

    if ext_ref:
        app_record.external_reference_number = ext_ref.strip()

    if notes is not None:
        app_record.student_notes = notes.strip()

    db.session.commit()
    flash("Application tracking status updated successfully.", "success")
    return redirect(url_for("scholarship.my_applications"))


# =========================================================================
# 8. SECURE STUDENT DOCUMENT VAULT
# =========================================================================

@scholarship.route("/documents")
def document_vault():
    if "user_id" not in session:
        flash("Please log in to access your secure document vault.", "info")
        return redirect(url_for("auth.login", next=request.url))

    user_id = session["user_id"]
    documents = StudentDocument.query.filter_by(user_id=user_id).order_by(StudentDocument.uploaded_at.desc()).all()

    standard_doc_types = [
        ("INCOME_CERTIFICATE", "Family Income Certificate (Revenue Authority)"),
        ("DOMICILE_CERTIFICATE", "Domicile / Residential Certificate"),
        ("CASTE_CERTIFICATE", "Caste / Tribe / Community Certificate (SC/ST/OBC)"),
        ("EWS_CERTIFICATE", "Economically Weaker Section (EWS) Certificate"),
        ("MARKSHEET_10", "Class 10 Passing Certificate & Marksheet"),
        ("MARKSHEET_12", "Class 12 Passing Certificate & Marksheet"),
        ("MARKSHEET_LAST", "Previous Year / Semester Marksheet"),
        ("BONAFIDE_CERTIFICATE", "College Bonafide Student Certificate"),
        ("FEE_RECEIPT", "Current Academic Year College Fee Receipt"),
        ("AADHAAR_CARD", "Aadhaar Card Copy (Masked)"),
        ("DISABILITY_CERTIFICATE", "Disability Certificate / UDID Card (PwD)"),
        ("BANK_PASSBOOK", "Bank Passbook First Page / Cancelled Cheque"),
        ("PHOTO", "Passport Size Photograph"),
        ("SIGNATURE", "Applicant Signature Scan")
    ]

    return render_template(
        "scholarship/documents.html",
        documents=documents,
        standard_doc_types=standard_doc_types
    )


@scholarship.route("/documents/upload", methods=["POST"])
def upload_document():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    user_id = session["user_id"]
    doc_type = request.form.get("document_type", "OTHER").strip()
    notes = request.form.get("notes", "").strip()

    if "file" not in request.files:
        flash("No file was selected for upload.", "danger")
        return redirect(url_for("scholarship.document_vault"))

    file = request.files["file"]
    if file.filename == "":
        flash("Please select a valid document file.", "danger")
        return redirect(url_for("scholarship.document_vault"))

    if not allowed_file(file.filename):
        flash("Unsupported file format. Please upload PDF, JPG, or PNG files only.", "danger")
        return redirect(url_for("scholarship.document_vault"))

    # Secure file storage in private directory
    ext = file.filename.rsplit(".", 1)[1].lower()
    clean_orig_name = secure_filename(file.filename)
    unique_filename = f"{user_id}_{doc_type}_{uuid.uuid4().hex[:8]}.{ext}"

    upload_dir = os.path.join(current_app.root_path, "uploads", "documents", str(user_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_filename)

    file.save(file_path)
    file_size = os.path.getsize(file_path)

    doc_record = StudentDocument(
        user_id=user_id,
        document_type=doc_type,
        document_name=clean_orig_name,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        verification_status="UPLOADED",
        notes=notes
    )
    db.session.add(doc_record)
    db.session.commit()

    flash(f"Document '{clean_orig_name}' successfully added to your vault.", "success")
    return redirect(request.referrer or url_for("scholarship.document_vault"))


@scholarship.route("/documents/download/<int:doc_id>")
def download_document(doc_id):
    if "user_id" not in session:
        abort(401)

    doc = StudentDocument.query.get_or_404(doc_id)
    # Strict IDOR protection: only owner can access
    if doc.user_id != session["user_id"]:
        abort(403)

    if not os.path.exists(doc.file_path):
        flash("Document file not found on server.", "danger")
        return redirect(url_for("scholarship.document_vault"))

    return send_file(
        doc.file_path,
        as_attachment=True,
        download_name=doc.document_name,
        mimetype=doc.mime_type or "application/octet-stream"
    )


@scholarship.route("/documents/delete/<int:doc_id>", methods=["POST"])
def delete_document(doc_id):
    if "user_id" not in session:
        abort(401)

    doc = StudentDocument.query.get_or_404(doc_id)
    if doc.user_id != session["user_id"]:
        abort(403)

    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except OSError:
            pass

    db.session.delete(doc)
    db.session.commit()
    flash("Document removed from your vault.", "info")
    return redirect(url_for("scholarship.document_vault"))


# =========================================================================
# 9. SCHOLARSHIP CALENDAR & DEADLINES
# =========================================================================

@scholarship.route("/calendar")
def scholarship_calendar():
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()
    state = request.args.get("state", "").strip()

    query = (
        db.session.query(Scholarship, ScholarshipCycle)
        .join(ScholarshipCycle, Scholarship.id == ScholarshipCycle.scholarship_id)
    )

    if category:
        query = query.filter(Scholarship.category == category)
    if state and state != "All":
        query = query.filter(
            or_(
                Scholarship.state.ilike(f"%{state}%"),
                Scholarship.national_or_state == "National"
            )
        )
    if status:
        query = query.filter(ScholarshipCycle.status == status)

    events = query.order_by(ScholarshipCycle.application_end_date.asc().nullslast()).all()

    categories_raw = db.session.query(Scholarship.category).distinct().all()
    categories = sorted([c[0] for c in categories_raw if c[0]])

    states_raw = db.session.query(Scholarship.state).distinct().all()
    states = sorted([s[0] for s in states_raw if s[0] and s[0] != "All India"])

    return render_template(
        "scholarship/calendar.html",
        events=events,
        categories=categories,
        states=states,
        selected_category=category,
        selected_status=status,
        selected_state=state
    )


# =========================================================================
# 10. SAVED SCHOLARSHIPS
# =========================================================================

@scholarship.route("/saved")
def saved_scholarships():
    if "user_id" not in session:
        flash("Please log in to view your saved scholarships.", "info")
        return redirect(url_for("auth.login", next=request.url))

    user_saved = SavedOpportunity.query.filter_by(
        user_id=session["user_id"],
        opportunity_type="scholarship"
    ).all()
    saved_ids = [s.item_id for s in user_saved]

    scholarships = (
        Scholarship.query.filter(Scholarship.id.in_(saved_ids)).all()
        if saved_ids else []
    )

    return render_template(
        "scholarship/saved.html",
        scholarships=scholarships
    )


# =========================================================================
# 11. SIDE-BY-SIDE SCHOLARSHIP COMPARISON
# =========================================================================

@scholarship.route("/compare")
def compare_scholarships():
    ids_param = request.args.get("ids", "").strip()
    id_list = []
    if ids_param:
        for p in ids_param.split(","):
            if p.strip().isdigit():
                id_list.append(int(p.strip()))

    selected_scholarships = (
        Scholarship.query.filter(Scholarship.id.in_(id_list)).limit(3).all()
        if id_list else []
    )

    all_scholarships = Scholarship.query.order_by(Scholarship.title.asc()).all()

    return render_template(
        "scholarship/compare.html",
        scholarships=selected_scholarships,
        all_scholarships=all_scholarships
    )


# =========================================================================
# 12. NATIONAL COVERAGE DASHBOARD
# =========================================================================

@scholarship.route("/coverage")
def national_coverage():
    total_count = Scholarship.query.count()

    provider_breakdown = (
        db.session.query(Scholarship.provider_type, func.count(Scholarship.id))
        .group_by(Scholarship.provider_type)
        .order_by(func.count(Scholarship.id).desc())
        .all()
    )

    state_breakdown = (
        db.session.query(Scholarship.state, func.count(Scholarship.id))
        .filter(Scholarship.state.isnot(None), Scholarship.state != "", Scholarship.state != "All India")
        .group_by(Scholarship.state)
        .order_by(func.count(Scholarship.id).desc())
        .all()
    )

    category_breakdown = (
        db.session.query(Scholarship.category, func.count(Scholarship.id))
        .group_by(Scholarship.category)
        .order_by(func.count(Scholarship.id).desc())
        .all()
    )

    verified_count = Scholarship.query.filter_by(verification_status="VERIFIED").count()
    needs_review_count = Scholarship.query.filter_by(verification_status="NEEDS_REVIEW").count()

    return render_template(
        "scholarship/coverage.html",
        total_count=total_count,
        verified_count=verified_count,
        needs_review_count=needs_review_count,
        provider_breakdown=provider_breakdown,
        state_breakdown=state_breakdown,
        category_breakdown=category_breakdown
    )


# =========================================================================
# 13. BOOKMARK / SAVE SCHOLARSHIP TOGGLE (Preserved from existing codebase)
# =========================================================================

@scholarship.route("/save/<int:scholarship_id>")
def toggle_save(scholarship_id):
    if "user_id" not in session:
        flash("Please log in to save scholarships to your profile.", "info")
        return redirect(url_for("auth.login"))

    s_obj = Scholarship.query.get_or_404(scholarship_id)

    existing = SavedOpportunity.query.filter_by(
        user_id=session["user_id"],
        opportunity_type="scholarship",
        item_id=scholarship_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{s_obj.title} removed from saved scholarships.", "info")
    else:
        saved = SavedOpportunity(
            user_id=session["user_id"],
            opportunity_type="scholarship",
            item_id=scholarship_id,
            title=s_obj.title
        )
        db.session.add(saved)
        db.session.commit()
        flash(f"{s_obj.title} saved to your profile!", "success")

    return redirect(request.referrer or url_for("scholarship.scholarship_list"))


# =========================================================================
# 14. GROUNDED AI SCHOLARSHIP COUNSELLOR API
# =========================================================================

@scholarship.route("/api/counsellor", methods=["POST"])
def api_counsellor():
    payload = request.get_json() or {}
    query_text = (payload.get("query") or "").strip().lower()

    if not query_text:
        return jsonify({"success": False, "error": "Query cannot be empty"}), 400

    # Retrieve relevant scholarships from database matching query tokens
    tokens = [t for t in query_text.replace("?", "").replace(",", " ").split() if len(t) > 2]
    clauses = []
    for t in tokens:
        clauses.extend([
            Scholarship.title.ilike(f"%{t}%"),
            Scholarship.category.ilike(f"%{t}%"),
            Scholarship.state.ilike(f"%{t}%"),
            Scholarship.streams.ilike(f"%{t}%"),
            Scholarship.courses.ilike(f"%{t}%"),
            Scholarship.provider.ilike(f"%{t}%"),
            Scholarship.education_level.ilike(f"%{t}%")
        ])

    matched_scholarships = []
    if clauses:
        matched_scholarships = (
            Scholarship.query.filter(or_(*clauses))
            .limit(5)
            .all()
        )

    if not matched_scholarships:
        matched_scholarships = Scholarship.query.limit(4).all()

    # Build grounded, explainable response
    lines = []
    lines.append(f"Here are verified national and state scholarship pathways related to your query:")
    for s in matched_scholarships:
        limit_txt = f"income ceiling ₹{s.family_income_limit:,.0f}" if s.family_income_limit else "merit based"
        lines.append(f"\n• **{s.title}** ({s.provider_type})")
        lines.append(f"  - **Benefit:** {s.amount or 'Financial support'}")
        lines.append(f"  - **Eligibility:** {s.eligibility[:120]}... ({limit_txt})")
        lines.append(f"  - **Official Portal:** {s.official_application_url or 'scholarships.gov.in'}")

    lines.append(f"\n*Recommendation:* You can click 'Check Eligibility' on any scholarship to see your deterministic suitability score and exact required documents.")

    return jsonify({
        "success": True,
        "response": "\n".join(lines),
        "count": len(matched_scholarships)
    })