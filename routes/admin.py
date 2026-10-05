from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file,
    Response,
    jsonify
)

import csv
import json
import re
from datetime import datetime, date
from functools import wraps
from io import BytesIO, StringIO

from sqlalchemy import or_, func
try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

from extensions import db


from models.user import User
from models.career import Career
from models.college import College
from models.scholarship import Scholarship, ScholarshipCycle, ScholarshipApplication, ScholarshipField
from models.internship import Internship
from models.exam import GovernmentExam
from models.assessment import AssessmentResult
from models.roadmap import CareerRoadmap
from models.website_visit import WebsiteVisit
from models.course import Course, CollegeCourse


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# ADMIN ACCESS PROTECTION
# =========================================================

def admin_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        user_id = session.get("user_id")

        # Not logged in
        if not user_id:

            flash(
                "Please login to access the admin panel.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        # Get actual user from database
        user = User.query.get(user_id)

        # User doesn't exist
        if not user:

            session.clear()

            flash(
                "Your account could not be found.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # User is not admin
        if user.role != "admin":

            flash(
                "You do not have permission to access the admin panel.",
                "danger"
            )

            return redirect(
                url_for("main.index")
            )

        # Admin account inactive
        if not user.is_active:

            session.clear()

            flash(
                "Your admin account is inactive.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        return view(*args, **kwargs)

    return wrapped_view


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin.route("/")
@admin_required
def dashboard():

    total_students = User.query.filter_by(
        role="student"
    ).count()

    active_students = User.query.filter_by(
        role="student",
        is_active=True
    ).count()

    inactive_students = User.query.filter_by(
        role="student",
        is_active=False
    ).count()

    total_visits = WebsiteVisit.query.count()

    stats = {

        "users": User.query.count(),

        "students": total_students,

        "active_students": active_students,

        "inactive_students": inactive_students,

        "careers": Career.query.count(),

        "colleges": College.query.count(),

        "scholarships": Scholarship.query.count(),

        "internships": Internship.query.count(),

        "exams": GovernmentExam.query.count(),

        "assessments": AssessmentResult.query.count(),

        "visits": total_visits

    }

    recent_users = User.query.filter_by(
        role="student"
    ).order_by(
        User.created_at.desc()
    ).limit(5).all()

    recent_careers = Career.query.order_by(
        Career.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_users=recent_users,
        recent_careers=recent_careers
    )


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

@admin.route("/students")
@admin_required
def students():

    search = request.args.get(
        "search",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    ).strip().lower()

    stream = request.args.get(
        "stream",
        ""
    ).strip()

    query = User.query.filter_by(
        role="student"
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search:

        search_pattern = f"%{search}%"

        query = query.filter(
            or_(
                User.full_name.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.contact_number.ilike(search_pattern),
                User.college_name.ilike(search_pattern),
                User.course.ilike(search_pattern),
                User.state.ilike(search_pattern),
                User.district.ilike(search_pattern)
            )
        )

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    if status == "active":

        query = query.filter(
            User.is_active == True
        )

    elif status == "inactive":

        query = query.filter(
            User.is_active == False
        )

    # -----------------------------------------------------
    # STREAM FILTER
    # -----------------------------------------------------

    if stream:

        query = query.filter(
            User.stream.ilike(
                f"%{stream}%"
            )
        )

    students = query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/students.html",
        students=students,
        search=search,
        status=status,
        stream=stream
    )


# =========================================================
# VIEW STUDENT
# =========================================================

@admin.route("/students/<int:id>")
@admin_required
def student_detail(id):

    student = User.query.filter_by(
        id=id,
        role="student"
    ).first_or_404()

    return render_template(
        "admin/student_detail.html",
        student=student
    )


# =========================================================
# ACTIVATE STUDENT
# =========================================================

@admin.route("/students/<int:id>/activate")
@admin_required
def activate_student(id):

    student = User.query.filter_by(
        id=id,
        role="student"
    ).first_or_404()

    student.is_active = True

    db.session.commit()

    flash(
        f"{student.full_name}'s account has been activated.",
        "success"
    )

    return redirect(
        url_for(
            "admin.students"
        )
    )


# =========================================================
# DEACTIVATE STUDENT
# =========================================================

@admin.route("/students/<int:id>/deactivate")
@admin_required
def deactivate_student(id):

    student = User.query.filter_by(
        id=id,
        role="student"
    ).first_or_404()

    student.is_active = False

    db.session.commit()

    flash(
        f"{student.full_name}'s account has been deactivated.",
        "warning"
    )

    return redirect(
        url_for(
            "admin.students"
        )
    )


# =========================================================
# EXPORT STUDENTS TO EXCEL
# =========================================================

@admin.route("/students/export")
@admin_required
def export_students():

    students = User.query.filter_by(
        role="student"
    ).order_by(
        User.created_at.desc()
    ).all()

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Students"

    # Excel headers
    headers = [

        "Student ID",

        "Full Name",

        "Email",

        "Contact Number",

        "Class / Grade",

        "Stream",

        "College / University",

        "Course",

        "Passing Year",

        "State",

        "District",

        "Career Interest",

        "Account Status",

        "Registration Date"

    ]

    worksheet.append(headers)

    # Student data
    for student in students:

        account_status = (
            "Active"
            if student.is_active
            else "Inactive"
        )

        registration_date = ""

        if student.created_at:

            registration_date = (
                student.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

        worksheet.append([

            student.id,

            student.full_name,

            student.email,

            student.contact_number or "",

            student.class_grade or "",

            student.stream or "",

            student.college_name or "",

            student.course or "",

            student.passing_year or "",

            student.state or "",

            student.district or "",

            student.career_interest or "",

            account_status,

            registration_date

        ])

    # -----------------------------------------------------
    # COLUMN WIDTHS
    # -----------------------------------------------------

    column_widths = {

        "A": 12,

        "B": 25,

        "C": 30,

        "D": 20,

        "E": 18,

        "F": 18,

        "G": 32,

        "H": 25,

        "I": 18,

        "J": 20,

        "K": 20,

        "L": 30,

        "M": 18,

        "N": 24

    }

    for column, width in column_widths.items():

        worksheet.column_dimensions[
            column
        ].width = width

    # Freeze first row
    worksheet.freeze_panes = "A2"

    # Auto filter
    worksheet.auto_filter.ref = (
        worksheet.dimensions
    )

    # -----------------------------------------------------
    # SAVE EXCEL IN MEMORY
    # -----------------------------------------------------

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return send_file(

        output,

        as_attachment=True,

        download_name=(
            "careerpath_india_students.xlsx"
        ),

        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )

    )


# =========================================================
# CAREER MANAGEMENT & BULK IMPORT
# =========================================================

@admin.route("/careers")
@admin_required
def careers():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 20

    query = Career.query

    if search:
        query = query.filter(
            or_(
                Career.title.ilike(f"%{search}%"),
                Career.description.ilike(f"%{search}%"),
                Career.industry.ilike(f"%{search}%")
            )
        )

    if category:
        query = query.filter(Career.category == category)

    if status:
        query = query.filter(Career.verification_status == status)

    pagination = query.order_by(Career.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = [
        c[0] for c in db.session.query(Career.category).distinct().order_by(Career.category.asc()).all() if c[0]
    ]

    total_careers = Career.query.count()
    verified_careers = Career.query.filter_by(verification_status="VERIFIED").count()

    return render_template(
        "admin/careers.html",
        careers=pagination.items,
        pagination=pagination,
        categories=categories,
        search=search,
        selected_category=category,
        selected_status=status,
        total_careers=total_careers,
        verified_careers=verified_careers
    )


@admin.route("/careers/add", methods=["GET", "POST"])
@admin_required
def add_career():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip() or title.lower().replace(" ", "-").replace("/", "-")
        category = request.form.get("category", "").strip()
        sub_category = request.form.get("sub_category", "").strip()
        industry = request.form.get("industry", "").strip()
        short_description = request.form.get("short_description", "").strip()
        description = request.form.get("description", "").strip()
        what_they_do = request.form.get("what_they_do", "").strip()
        day_to_day_work = request.form.get("day_to_day_work", "").strip()
        minimum_qualification = request.form.get("minimum_qualification", "").strip()
        preferred_streams = request.form.get("preferred_streams", "").strip()
        required_subjects = request.form.get("required_subjects", "").strip()
        technical_skills = request.form.get("technical_skills", "").strip()
        soft_skills = request.form.get("soft_skills", "").strip()
        tools = request.form.get("tools", "").strip()
        work_modes = request.form.get("work_modes", "Hybrid / Office").strip()
        average_salary = request.form.get("average_salary", "").strip()
        salary_indicative = request.form.get("salary_indicative", "").strip()
        source = request.form.get("source", "National Career Service (NCS)").strip()
        official_url = request.form.get("official_url", "https://www.ncs.gov.in").strip()
        verification_status = request.form.get("verification_status", "VERIFIED").strip()

        if not title or not category:
            flash("Title and Category are required.", "danger")
            return redirect(url_for("admin.add_career"))

        career = Career(
            title=title,
            slug=slug,
            short_name=title,
            category=category,
            sub_category=sub_category,
            industry=industry,
            short_description=short_description,
            description=description,
            what_they_do=what_they_do,
            day_to_day_work=day_to_day_work,
            minimum_qualification=minimum_qualification,
            education_required=minimum_qualification,
            preferred_streams=preferred_streams,
            required_subjects=required_subjects,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            tools=tools,
            skills_required=f"{technical_skills}, {soft_skills}".strip(", "),
            work_modes=work_modes,
            average_salary=average_salary,
            salary_indicative=salary_indicative,
            source=source,
            official_url=official_url,
            verification_status=verification_status
        )
        db.session.add(career)
        db.session.commit()
        flash("Career Added Successfully!", "success")
        return redirect(url_for("admin.careers"))

    categories = [
        "Technology & Computer Science", "Healthcare & Medical Sciences", "Finance, Banking & Accounting",
        "Engineering & Manufacturing", "Law & Legal Services", "Government, Defence & Civil Services",
        "Business, Management & Consulting", "Science, Research & Mathematics", "Education, Teaching & Academia",
        "Media, Journalism & Digital Marketing", "Design, Animation & Creative Arts",
        "Agriculture, Food Technology & Environment", "Aviation, Logistics & Supply Chain",
        "Social Sciences, Psychology & Public Policy"
    ]
    return render_template("admin/add_career.html", categories=categories)


@admin.route("/careers/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_career(id):
    career = Career.query.get_or_404(id)

    if request.method == "POST":
        career.title = request.form.get("title", "").strip()
        career.slug = request.form.get("slug", "").strip() or career.slug
        career.category = request.form.get("category", "").strip()
        career.sub_category = request.form.get("sub_category", "").strip()
        career.industry = request.form.get("industry", "").strip()
        career.short_description = request.form.get("short_description", "").strip()
        career.description = request.form.get("description", "").strip()
        career.what_they_do = request.form.get("what_they_do", "").strip()
        career.day_to_day_work = request.form.get("day_to_day_work", "").strip()
        career.minimum_qualification = request.form.get("minimum_qualification", "").strip()
        career.education_required = career.minimum_qualification
        career.preferred_streams = request.form.get("preferred_streams", "").strip()
        career.required_subjects = request.form.get("required_subjects", "").strip()
        career.technical_skills = request.form.get("technical_skills", "").strip()
        career.soft_skills = request.form.get("soft_skills", "").strip()
        career.tools = request.form.get("tools", "").strip()
        career.skills_required = f"{career.technical_skills}, {career.soft_skills}".strip(", ")
        career.work_modes = request.form.get("work_modes", "Hybrid / Office").strip()
        career.average_salary = request.form.get("average_salary", "").strip()
        career.salary_indicative = request.form.get("salary_indicative", "").strip()
        career.source = request.form.get("source", "").strip()
        career.official_url = request.form.get("official_url", "").strip()
        career.verification_status = request.form.get("verification_status", "VERIFIED").strip()

        db.session.commit()
        flash("Career Updated Successfully!", "success")
        return redirect(url_for("admin.careers"))

    categories = [
        "Technology & Computer Science", "Healthcare & Medical Sciences", "Finance, Banking & Accounting",
        "Engineering & Manufacturing", "Law & Legal Services", "Government, Defence & Civil Services",
        "Business, Management & Consulting", "Science, Research & Mathematics", "Education, Teaching & Academia",
        "Media, Journalism & Digital Marketing", "Design, Animation & Creative Arts",
        "Agriculture, Food Technology & Environment", "Aviation, Logistics & Supply Chain",
        "Social Sciences, Psychology & Public Policy"
    ]
    return render_template("admin/edit_career.html", career=career, categories=categories)


@admin.route("/careers/delete/<int:id>", methods=["GET", "POST"])
@admin_required
def delete_career(id):
    career = Career.query.get_or_404(id)
    db.session.delete(career)
    db.session.commit()
    flash("Career Deleted Successfully!", "warning")
    return redirect(url_for("admin.careers"))


@admin.route("/careers/bulk-import", methods=["POST"])
@admin_required
def career_bulk_import():
    file = request.files.get("file")
    if not file or not file.filename:
        flash("Please upload a valid JSON file.", "warning")
        return redirect(url_for("admin.careers"))

    imported_count = 0
    updated_count = 0

    try:
        content = file.read().decode("utf-8")
        records = json.loads(content)
        if not isinstance(records, list):
            records = [records]

        for item in records:
            title = item.get("title", "").strip()
            slug = item.get("slug", "").strip() or title.lower().replace(" ", "-")
            if not title or not item.get("category"):
                continue

            existing = Career.query.filter_by(slug=slug).first()
            if existing:
                existing.title = title
                existing.category = item.get("category")
                existing.sub_category = item.get("sub_category", existing.sub_category)
                existing.industry = item.get("industry", existing.industry)
                existing.short_description = item.get("short_description", existing.short_description)
                existing.description = item.get("description", existing.description)
                existing.what_they_do = item.get("what_they_do", existing.what_they_do)
                existing.day_to_day_work = item.get("day_to_day_work", existing.day_to_day_work)
                existing.minimum_qualification = item.get("minimum_qualification", existing.minimum_qualification)
                existing.education_required = existing.minimum_qualification
                existing.preferred_streams = item.get("preferred_streams", existing.preferred_streams)
                existing.required_subjects = item.get("required_subjects", existing.required_subjects)
                existing.technical_skills = item.get("technical_skills", existing.technical_skills)
                existing.soft_skills = item.get("soft_skills", existing.soft_skills)
                existing.tools = item.get("tools", existing.tools)
                existing.skills_required = f"{existing.technical_skills}, {existing.soft_skills}".strip(", ")
                existing.average_salary = item.get("average_salary", existing.average_salary)
                existing.salary_indicative = item.get("salary_indicative", existing.salary_indicative)
                existing.verification_status = item.get("verification_status", "VERIFIED")
                updated_count += 1
            else:
                new_c = Career(
                    title=title,
                    slug=slug,
                    short_name=item.get("short_name", title),
                    category=item.get("category"),
                    sub_category=item.get("sub_category", ""),
                    industry=item.get("industry", ""),
                    short_description=item.get("short_description", ""),
                    description=item.get("description", ""),
                    what_they_do=item.get("what_they_do", ""),
                    day_to_day_work=item.get("day_to_day_work", ""),
                    minimum_qualification=item.get("minimum_qualification", "Undergraduate Degree"),
                    education_required=item.get("minimum_qualification", "Undergraduate Degree"),
                    preferred_streams=item.get("preferred_streams", ""),
                    required_subjects=item.get("required_subjects", ""),
                    technical_skills=item.get("technical_skills", ""),
                    soft_skills=item.get("soft_skills", ""),
                    tools=item.get("tools", ""),
                    skills_required=f"{item.get('technical_skills', '')}, {item.get('soft_skills', '')}".strip(", "),
                    work_modes=item.get("work_modes", "Hybrid / Office"),
                    average_salary=item.get("average_salary", "₹4 - ₹12 LPA"),
                    salary_indicative=item.get("salary_indicative", ""),
                    source=item.get("source", "National Career Service (NCS)"),
                    official_url=item.get("official_url", "https://www.ncs.gov.in"),
                    verification_status=item.get("verification_status", "VERIFIED")
                )
                db.session.add(new_c)
                imported_count += 1
        db.session.commit()
        flash(f"Bulk Import Complete! Added: {imported_count}, Updated: {updated_count}", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Bulk import error: {str(e)}", "danger")

    return redirect(url_for("admin.careers"))



# =========================================================
# ROADMAP MANAGEMENT
# =========================================================

@admin.route("/roadmaps")
@admin_required
def roadmaps():

    roadmaps = CareerRoadmap.query.all()

    return render_template(
        "admin/roadmaps.html",
        roadmaps=roadmaps
    )


@admin.route(
    "/roadmaps/add",
    methods=["GET", "POST"]
)
@admin_required
def add_roadmap():

    careers = Career.query.order_by(
        Career.title
    ).all()

    if request.method == "POST":

        roadmap = CareerRoadmap(

            career_id=request.form[
                "career_id"
            ],

            overview=request.form[
                "overview"
            ],

            required_skills=request.form[
                "required_skills"
            ],

            best_colleges=request.form[
                "best_colleges"
            ],

            recommended_courses=request.form[
                "recommended_courses"
            ],

            projects=request.form[
                "projects"
            ],

            internships=request.form[
                "internships"
            ],

            salary=request.form[
                "salary"
            ],

            future_scope=request.form[
                "future_scope"
            ],

            top_companies=request.form[
                "top_companies"
            ],

            roadmap_steps=request.form[
                "roadmap_steps"
            ]

        )

        db.session.add(roadmap)

        db.session.commit()

        flash(
            "Roadmap Added Successfully!",
            "success"
        )

        return redirect(
            url_for(
                "admin.roadmaps"
            )
        )

    return render_template(
        "admin/add_roadmap.html",
        careers=careers
    )


# =========================================================
# COLLEGE MANAGEMENT
# =========================================================

@admin.route("/colleges")
@admin_required
def colleges():

    colleges = College.query.order_by(
        College.name
    ).all()

    return render_template(
        "admin/colleges.html",
        colleges=colleges
    )


@admin.route("/aishe-importer", methods=["GET", "POST"])
@admin_required
def aishe_importer_dashboard():
    from scripts.aishe_importer import AisheImporter

    if request.method == "POST":
        scope = request.form.get("import_scope", "all_premier")
        importer = AisheImporter()

        inc_pm = scope in ["pm_vidyalaxmi", "all_premier"]
        inc_rnd = scope in ["rnd", "all_premier"]
        states = [(23, "Madhya Pradesh")] if scope in ["state_mp", "all_premier"] else None
        districts = [(418, "Guna")] if scope in ["state_mp", "all_premier"] else None

        stats = importer.run_import(
            include_pm_vidyalaxmi=inc_pm,
            include_rnd=inc_rnd,
            states_to_import=states,
            sample_districts=districts
        )
        flash(f"AISHE Sync Completed: {stats['total_fetched']} records fetched, {stats['total_new']} new, {stats['total_updated']} updated.", "success")
        return redirect(url_for("admin.aishe_importer_dashboard"))

    total = College.query.count()
    with_aishe = College.query.filter(College.aishe_code != None).count()
    with_website = College.query.filter(College.official_website != None, func.length(College.official_website) > 3).count()
    universities = College.query.filter(
        or_(
            College.institution_category == "University",
            College.institution_type.ilike("%university%")
        )
    ).count()

    state_counts = db.session.query(College.state, func.count(College.id)).group_by(College.state).order_by(func.count(College.id).desc()).limit(20).all()

    return render_template(
        "admin/aishe_importer.html",
        stats={
            "total": total,
            "with_aishe": with_aishe,
            "with_website": with_website,
            "universities": universities,
            "state_counts": state_counts
        }
    )


@admin.route(
    "/colleges/add",
    methods=["GET", "POST"]
)
@admin_required
def add_college():

    if request.method == "POST":

        college = College(

            name=request.form[
                "name"
            ],

            city=request.form[
                "city"
            ],

            state=request.form[
                "state"
            ],

            college_type=request.form[
                "college_type"
            ],

            course=request.form[
                "course"
            ],

            fees=request.form[
                "fees"
            ],

            placement=request.form[
                "placement"
            ],

            highest_package=request.form[
                "highest_package"
            ],

            average_package=request.form[
                "average_package"
            ],

            website=request.form[
                "website"
            ],

            description=request.form[
                "description"
            ]

        )

        db.session.add(college)

        db.session.commit()

        flash(
            "College Added Successfully",
            "success"
        )

        return redirect(
            url_for(
                "admin.colleges"
            )
        )

    return render_template(
        "admin/add_college.html"
    )


@admin.route(
    "/colleges/delete/<int:id>"
)
@admin_required
def delete_college(id):

    college = College.query.get_or_404(id)

    db.session.delete(college)

    db.session.commit()

    flash(
        "College Deleted",
        "success"
    )

    return redirect(
        url_for(
            "admin.colleges"
        )
    )


# =========================================================
# EXAMS MANAGEMENT
# =========================================================

@admin.route("/exams")
@admin_required
def exams():
    exams_list = GovernmentExam.query.order_by(GovernmentExam.exam_name.asc()).all()
    return render_template("admin/exams.html", exams=exams_list)


@admin.route("/exams/delete/<int:id>")
@admin_required
def delete_exam(id):
    item = GovernmentExam.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f"{item.exam_name} deleted.", "success")
    return redirect(url_for("admin.exams"))


# =========================================================
# SCHOLARSHIPS MANAGEMENT & DATA QUALITY SUITE
# =========================================================

def _compute_scholarship_health():
    total = Scholarship.query.count()
    verified = Scholarship.query.filter_by(verification_status="VERIFIED").count()
    needs_review = Scholarship.query.filter_by(verification_status="NEEDS_REVIEW").count()
    archived = Scholarship.query.filter_by(verification_status="ARCHIVED").count()
    
    open_cycles = ScholarshipCycle.query.filter_by(status="OPEN").count()
    closing_soon = ScholarshipCycle.query.filter_by(status="CLOSING_SOON").count()
    
    missing_official_url = Scholarship.query.filter(
        or_(Scholarship.official_url.is_(None), Scholarship.official_url == "",
            Scholarship.website.is_(None), Scholarship.website == "")
    ).count()
    
    missing_app_url = Scholarship.query.filter(
        or_(Scholarship.official_application_url.is_(None), Scholarship.official_application_url == "")
    ).count()
    
    missing_eligibility = Scholarship.query.filter(
        or_(Scholarship.eligibility.is_(None), Scholarship.eligibility == "")
    ).count()
    
    missing_documents = Scholarship.query.filter(
        or_(Scholarship.documents_required.is_(None), Scholarship.documents_required == "")
    ).count()
    
    missing_source = Scholarship.query.filter(
        or_(Scholarship.source.is_(None), Scholarship.source == "")
    ).count()
    
    all_titles = db.session.query(Scholarship.id, Scholarship.title).all()
    seen = {}
    duplicates = []
    for s_id, title in all_titles:
        norm = re.sub(r'[^a-z0-9]', '', (title or "").lower())
        if norm in seen:
            duplicates.append((s_id, seen[norm]))
        else:
            seen[norm] = s_id
    duplicate_count = len(duplicates)
    
    return {
        "total": total,
        "verified": verified,
        "needs_review": needs_review,
        "archived": archived,
        "open_cycles": open_cycles,
        "closing_soon": closing_soon,
        "missing_official_url": missing_official_url,
        "missing_app_url": missing_app_url,
        "missing_eligibility": missing_eligibility,
        "missing_documents": missing_documents,
        "missing_source": missing_source,
        "duplicate_count": duplicate_count
    }


@admin.route("/scholarships")
@admin_required
def scholarships():
    q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()
    provider_type = request.args.get("provider_type", "").strip()
    health_filter = request.args.get("health_filter", "").strip()

    query = Scholarship.query

    if q:
        query = query.filter(
            or_(
                Scholarship.title.ilike(f"%{q}%"),
                Scholarship.provider.ilike(f"%{q}%"),
                Scholarship.provider_name.ilike(f"%{q}%"),
                Scholarship.state.ilike(f"%{q}%"),
                Scholarship.category.ilike(f"%{q}%")
            )
        )

    if status_filter:
        query = query.filter(Scholarship.verification_status == status_filter)

    if provider_type:
        query = query.filter(Scholarship.provider_type == provider_type)

    if health_filter == "missing_official_url":
        query = query.filter(or_(Scholarship.official_url.is_(None), Scholarship.official_url == "", Scholarship.website.is_(None), Scholarship.website == ""))
    elif health_filter == "missing_app_url":
        query = query.filter(or_(Scholarship.official_application_url.is_(None), Scholarship.official_application_url == ""))
    elif health_filter == "missing_eligibility":
        query = query.filter(or_(Scholarship.eligibility.is_(None), Scholarship.eligibility == ""))
    elif health_filter == "missing_documents":
        query = query.filter(or_(Scholarship.documents_required.is_(None), Scholarship.documents_required == ""))
    elif health_filter == "missing_source":
        query = query.filter(or_(Scholarship.source.is_(None), Scholarship.source == ""))

    scholarships_list = query.order_by(Scholarship.id.desc()).all()
    health = _compute_scholarship_health()

    return render_template(
        "admin/scholarships.html",
        scholarships=scholarships_list,
        health=health,
        q=q,
        status_filter=status_filter,
        provider_type=provider_type,
        health_filter=health_filter
    )


@admin.route("/scholarships/add", methods=["POST"])
@admin_required
def add_scholarship():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Scholarship title is required.", "danger")
        return redirect(url_for("admin.scholarships"))

    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    # ensure unique slug
    base_slug = slug
    counter = 1
    while Scholarship.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    income_limit_val = None
    inc_raw = request.form.get("family_income_limit", "").strip()
    if inc_raw:
        try:
            income_limit_val = float(inc_raw)
        except ValueError:
            pass

    perc_val = None
    perc_raw = request.form.get("percentage_requirement", "").strip()
    if perc_raw:
        try:
            perc_val = float(perc_raw)
        except ValueError:
            pass

    new_sch = Scholarship(
        title=title,
        slug=slug,
        provider=request.form.get("provider", "Government of India").strip(),
        provider_name=request.form.get("provider_name", "").strip() or request.form.get("provider", "").strip(),
        provider_type=request.form.get("provider_type", "Central Government").strip(),
        ministry=request.form.get("ministry", "").strip(),
        category=request.form.get("category", "General").strip(),
        national_or_state=request.form.get("national_or_state", "National").strip(),
        state=request.form.get("state", "All India").strip(),
        education_level=request.form.get("education_level", "UG / PG").strip(),
        amount=request.form.get("amount", "As per scheme norms").strip(),
        eligibility=request.form.get("eligibility", "").strip(),
        family_income_limit=income_limit_val,
        percentage_requirement=perc_val,
        documents_required=request.form.get("documents_required", "").strip(),
        official_website=request.form.get("official_website", "").strip(),
        website=request.form.get("official_website", "").strip() or request.form.get("official_url", "").strip(),
        official_url=request.form.get("official_url", "").strip() or request.form.get("official_website", "").strip(),
        official_application_url=request.form.get("official_application_url", "").strip(),
        notification_url=request.form.get("notification_url", "").strip(),
        guidelines_url=request.form.get("guidelines_url", "").strip(),
        faq_url=request.form.get("faq_url", "").strip(),
        application_url_status=request.form.get("application_url_status", "VALID").strip(),
        source=request.form.get("source_url", "").strip() or request.form.get("source_name", "Official Gazette").strip(),
        source_name=request.form.get("source_name", "Official Portal").strip(),
        source_url=request.form.get("source_url", "").strip(),
        verification_status=request.form.get("verification_status", "VERIFIED").strip(),
        last_verified_at=datetime.now(),
        application_url_verified_at=datetime.now(),
        application_url_verified_by=session.get("user_name", "Admin")
    )
    db.session.add(new_sch)
    db.session.flush()

    # Optional initial cycle
    acad_year = request.form.get("academic_year", "2026-27").strip()
    cycle_status = request.form.get("cycle_status", "OPEN").strip()
    if acad_year:
        cycle = ScholarshipCycle(
            scholarship_id=new_sch.id,
            academic_year=acad_year,
            status=cycle_status,
            official_application_url=new_sch.official_application_url,
            official_website=new_sch.official_website,
            faq_url=new_sch.faq_url,
            application_url_status=new_sch.application_url_status,
            verification_status="VERIFIED"
        )
        db.session.add(cycle)

    db.session.commit()
    flash(f"Scholarship '{new_sch.title}' created successfully!", "success")
    return redirect(url_for("admin.scholarships"))


@admin.route("/scholarships/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_scholarship(id):
    sch = Scholarship.query.get_or_404(id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            sch.title = title
        sch.provider = request.form.get("provider", sch.provider).strip()
        sch.provider_name = request.form.get("provider_name", sch.provider_name).strip()
        sch.provider_type = request.form.get("provider_type", sch.provider_type).strip()
        sch.ministry = request.form.get("ministry", sch.ministry).strip()
        sch.category = request.form.get("category", sch.category).strip()
        sch.national_or_state = request.form.get("national_or_state", sch.national_or_state).strip()
        sch.state = request.form.get("state", sch.state).strip()
        sch.education_level = request.form.get("education_level", sch.education_level).strip()
        sch.amount = request.form.get("amount", sch.amount).strip()
        sch.eligibility = request.form.get("eligibility", sch.eligibility).strip()

        inc_raw = request.form.get("family_income_limit", "").strip()
        sch.family_income_limit = float(inc_raw) if inc_raw else None

        perc_raw = request.form.get("percentage_requirement", "").strip()
        sch.percentage_requirement = float(perc_raw) if perc_raw else None

        sch.documents_required = request.form.get("documents_required", sch.documents_required).strip()
        
        # Dedicated segregated URLs (SECTIONS 2 & 15)
        sch.official_website = request.form.get("official_website", sch.official_website).strip()
        sch.website = sch.official_website or sch.website
        sch.official_url = sch.official_website or sch.official_url
        sch.official_application_url = request.form.get("official_application_url", sch.official_application_url).strip()
        sch.notification_url = request.form.get("notification_url", sch.notification_url).strip()
        sch.guidelines_url = request.form.get("guidelines_url", sch.guidelines_url).strip()
        sch.faq_url = request.form.get("faq_url", sch.faq_url).strip()

        # URL status (SECTION 17)
        sch.application_url_status = request.form.get("application_url_status", sch.application_url_status or "VALID").strip()

        sch.source_name = request.form.get("source_name", sch.source_name or "Official Source").strip()
        sch.source_url = request.form.get("source_url", sch.source_url or "").strip()
        sch.source = sch.source_url or sch.source_name
        sch.verification_status = request.form.get("verification_status", sch.verification_status).strip()
        sch.last_verified_at = datetime.now()

        # Update active cycle if exists
        if sch.active_cycle:
            sch.active_cycle.official_application_url = sch.official_application_url
            sch.active_cycle.official_website = sch.official_website
            sch.active_cycle.faq_url = sch.faq_url
            sch.active_cycle.application_url_status = sch.application_url_status

        db.session.commit()
        flash(f"Scholarship '{sch.title}' updated successfully.", "success")
        return redirect(url_for("admin.scholarships"))

    return jsonify({
        "id": sch.id,
        "title": sch.title,
        "provider": sch.provider,
        "provider_name": sch.provider_name,
        "provider_type": sch.provider_type,
        "ministry": sch.ministry,
        "category": sch.category,
        "national_or_state": sch.national_or_state,
        "state": sch.state,
        "education_level": sch.education_level,
        "amount": sch.amount,
        "eligibility": sch.eligibility,
        "family_income_limit": sch.family_income_limit,
        "percentage_requirement": sch.percentage_requirement,
        "documents_required": sch.documents_required,
        "official_website": sch.official_website or sch.website or sch.official_url,
        "official_application_url": sch.official_application_url,
        "notification_url": sch.notification_url,
        "guidelines_url": sch.guidelines_url,
        "faq_url": sch.faq_url,
        "application_url_status": sch.application_url_status or "VALID",
        "is_homepage_as_app_url": sch.is_homepage_as_app_url,
        "homepage_duplication_warning": sch.homepage_duplication_warning,
        "source_name": sch.source_name,
        "source_url": sch.source_url,
        "verification_status": sch.verification_status
    })


@admin.route("/scholarships/<int:id>/test-url")
@admin_required
def test_scholarship_url(id):
    """Admin URL Test (SECTIONS 14, 15, 16 & 19)"""
    from services.scholarship_url_verifier import verify_scholarship_url
    sch = Scholarship.query.get_or_404(id)
    target = sch.resolved_application_url
    if not target:
        flash(f"Scholarship #{id} has no application URL configured.", "warning")
        return redirect(url_for("admin.scholarships"))

    verification = verify_scholarship_url(target, sch.resolved_official_website, timeout=6)
    sch.application_url_last_checked = datetime.now()
    sch.final_application_url = verification.get("final_url") or target

    status = verification["status"]
    if status in ("VALID", "REDIRECTED"):
        sch.application_url_status = "VALID"
        sch.application_url_verified_at = datetime.now()
        sch.application_url_verified_by = "Admin URL Tester"
        flash(f"URL Verified! Status: {status} (HTTP {verification.get('status_code')}). Destination: {verification.get('final_url')}", "success")
    elif status == "HOMEPAGE_ONLY":
        sch.application_url_status = "HOMEPAGE_ONLY"
        flash(f"Warning: URL points to a provider root homepage, not an application portal! Destination: {verification.get('final_url')}", "warning")
    else:
        sch.application_url_status = "BROKEN" if status in ("BROKEN", "UNREACHABLE") else "NEEDS_VERIFICATION"
        flash(f"URL Check Alert: {verification.get('error') or status} (Status: {sch.application_url_status})", "danger")

    db.session.commit()
    return redirect(url_for("admin.scholarships"))


@admin.route("/scholarships/<int:id>/verify-url", methods=["POST"])
@admin_required
def verify_scholarship_url(id):
    """Admin Mark as Verified (SECTION 16 & 17)"""
    sch = Scholarship.query.get_or_404(id)
    new_status = request.form.get("application_url_status", "VALID").strip()
    admin_user = User.query.get(session.get("user_id"))
    admin_name = admin_user.full_name if admin_user else "Admin"

    sch.application_url_status = new_status
    sch.application_url_verified_at = datetime.now()
    sch.application_url_verified_by = admin_name
    if sch.active_cycle:
        sch.active_cycle.application_url_status = new_status

    db.session.commit()
    flash(f"Scholarship #{sch.id} application URL marked as '{new_status}' by {admin_name}.", "success")
    return redirect(request.referrer or url_for("admin.scholarships"))


@admin.route("/scholarships/delete/<int:id>", methods=["GET", "POST"])
@admin_required
def delete_scholarship(id):
    item = Scholarship.query.get_or_404(id)
    # clean up cycles and fields
    ScholarshipCycle.query.filter_by(scholarship_id=id).delete()
    ScholarshipField.query.filter_by(scholarship_id=id).delete()
    db.session.delete(item)
    db.session.commit()
    flash(f"Scholarship #{id} '{item.title}' deleted successfully.", "success")
    return redirect(url_for("admin.scholarships"))


@admin.route("/scholarships/duplicate-check")
@admin_required
def duplicate_check_scholarships():
    all_schs = Scholarship.query.all()
    grouped = {}
    for s in all_schs:
        # Normalized key without special characters
        norm = re.sub(r'[^a-z0-9]', '', (s.title or "").lower())
        grouped.setdefault(norm, []).append(s)

    duplicate_groups = [items for norm, items in grouped.items() if len(items) > 1]
    return jsonify({
        "duplicate_groups_count": len(duplicate_groups),
        "groups": [
            [{"id": s.id, "title": s.title, "provider": s.provider, "state": s.state} for s in group]
            for group in duplicate_groups
        ]
    })


@admin.route("/scholarships/export/<string:fmt>")
@admin_required
def export_scholarships(fmt):
    schs = Scholarship.query.order_by(Scholarship.id.asc()).all()
    if fmt == "json":
        data = []
        for s in schs:
            data.append({
                "id": s.id,
                "title": s.title,
                "provider": s.provider,
                "provider_type": s.provider_type,
                "ministry": s.ministry,
                "state": s.state,
                "category": s.category,
                "amount": s.amount,
                "eligibility": s.eligibility,
                "family_income_limit": s.family_income_limit,
                "percentage_requirement": s.percentage_requirement,
                "documents_required": s.documents_required,
                "official_website": s.official_website,
                "official_application_url": s.official_application_url,
                "source_name": s.source_name,
                "source_url": s.source_url,
                "verification_status": s.verification_status
            })
        return Response(
            json.dumps(data, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=scholarships_export.json"}
        )
    elif fmt == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Title", "Provider", "Provider Type", "Ministry", "State", "Category",
            "Amount", "Income Limit", "Percentage Req", "Official URL", "Application URL", "Source URL", "Verification Status"
        ])
        for s in schs:
            writer.writerow([
                s.id, s.title, s.provider, s.provider_type, s.ministry, s.state, s.category,
                s.amount, s.family_income_limit or "", s.percentage_requirement or "",
                s.official_website or s.official_url or "", s.official_application_url or "",
                s.source_url or "", s.verification_status
            ])
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=scholarships_export.csv"}
        )
    return redirect(url_for("admin.scholarships"))


@admin.route("/scholarships/import", methods=["POST"])
@admin_required
def import_scholarships():
    uploaded_file = request.files.get("file")
    raw_json = request.form.get("raw_json", "").strip()
    items = []

    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()
        if filename.endswith(".json"):
            try:
                items = json.load(uploaded_file)
            except Exception as e:
                flash(f"Error parsing JSON: {e}", "danger")
                return redirect(url_for("admin.scholarships"))
        elif filename.endswith(".csv"):
            try:
                stream = StringIO(uploaded_file.stream.read().decode("UTF-8"), newline=None)
                reader = csv.DictReader(stream)
                items = [row for row in reader]
            except Exception as e:
                flash(f"Error parsing CSV: {e}", "danger")
                return redirect(url_for("admin.scholarships"))
    elif raw_json:
        try:
            items = json.loads(raw_json)
        except Exception as e:
            flash(f"Error parsing JSON text: {e}", "danger")
            return redirect(url_for("admin.scholarships"))

    if not items:
        flash("No valid records found in the uploaded file.", "warning")
        return redirect(url_for("admin.scholarships"))

    if isinstance(items, dict):
        items = [items]

    imported_count = 0
    updated_count = 0
    skipped_duplicates = 0
    missing_source_count = 0
    errors = []

    for idx, item in enumerate(items, 1):
        title = (item.get("title") or item.get("name") or "").strip()
        if not title:
            errors.append(f"Row #{idx}: Missing title.")
            continue

        source_url = item.get("source_url") or item.get("source") or ""
        if not source_url:
            missing_source_count += 1

        norm_title = re.sub(r'[^a-z0-9]', '', title.lower())
        existing = Scholarship.query.filter(
            func.lower(Scholarship.title) == title.lower()
        ).first()

        if existing:
            # Update existing record
            existing.provider = item.get("provider", existing.provider)
            existing.provider_type = item.get("provider_type", existing.provider_type)
            existing.amount = item.get("amount", existing.amount)
            existing.eligibility = item.get("eligibility", existing.eligibility)
            existing.state = item.get("state", existing.state)
            existing.category = item.get("category", existing.category)
            existing.official_application_url = item.get("official_application_url", existing.official_application_url)
            existing.source = source_url or existing.source
            existing.verification_status = item.get("verification_status", existing.verification_status)
            existing.last_verified_at = datetime.now()
            updated_count += 1
            skipped_duplicates += 1
            continue

        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        base_slug = slug
        c = 1
        while Scholarship.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{c}"
            c += 1

        new_item = Scholarship(
            title=title,
            slug=slug,
            provider=item.get("provider", "Government / Institutional"),
            provider_name=item.get("provider_name") or item.get("provider", "Government / Institutional"),
            provider_type=item.get("provider_type", "Central Government"),
            ministry=item.get("ministry", ""),
            category=item.get("category", "General"),
            national_or_state=item.get("national_or_state", "National"),
            state=item.get("state", "All India"),
            education_level=item.get("education_level", "UG / PG"),
            amount=item.get("amount", "Financial Support"),
            eligibility=item.get("eligibility", "Recognized course enrollment"),
            documents_required=item.get("documents_required", "Marksheet, Income Certificate, ID Proof"),
            website=item.get("official_website") or item.get("official_url", ""),
            official_url=item.get("official_url") or item.get("official_website", ""),
            official_application_url=item.get("official_application_url", ""),
            source=source_url or item.get("source_name", "Imported Feed"),
            verification_status=item.get("verification_status", "VERIFIED"),
            last_verified_at=datetime.now()
        )
        db.session.add(new_item)
        imported_count += 1

    db.session.commit()
    report_msg = (
        f"Import complete: {imported_count} new schemes added, {updated_count} existing schemes refreshed. "
        f"{skipped_duplicates} duplicate titles matched. {missing_source_count} records lacked source URL."
    )
    flash(report_msg, "success" if imported_count > 0 or updated_count > 0 else "info")
    return redirect(url_for("admin.scholarships"))


# =========================================================
# INTERNSHIPS MANAGEMENT
# =========================================================

@admin.route("/internships")
@admin_required
def internships():
    internships_list = Internship.query.order_by(Internship.id.desc()).limit(150).all()
    return render_template("admin/internships.html", internships=internships_list)


@admin.route("/internships/delete/<int:id>")
@admin_required
def delete_internship(id):
    item = Internship.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f"{item.title} deleted.", "success")
    return redirect(url_for("admin.internships"))


# =========================================================
# DATA QUALITY & VERIFICATION STATUS TOGGLE
# =========================================================

@admin.route("/verify/<string:entity>/<int:id>")
@admin_required
def toggle_verification(entity, id):
    model_map = {
        "career": Career,
        "college": College,
        "exam": GovernmentExam,
        "scholarship": Scholarship,
        "internship": Internship
    }

    model = model_map.get(entity.lower())
    if not model:
        flash("Invalid entity type.", "danger")
        return redirect(url_for("admin.dashboard"))

    item = model.query.get_or_404(id)
    current_status = getattr(item, "verification_status", "VERIFIED") or "VERIFIED"

    # Cycle statuses: VERIFIED -> NEEDS_REVIEW -> ARCHIVED -> VERIFIED
    next_status = {
        "VERIFIED": "NEEDS_REVIEW",
        "NEEDS_REVIEW": "ARCHIVED",
        "ARCHIVED": "VERIFIED"
    }.get(current_status, "VERIFIED")

    item.verification_status = next_status
    db.session.commit()

    flash(f"Status for #{item.id} updated to {next_status}.", "success")
    return redirect(request.referrer or url_for("admin.dashboard"))


# =========================================================
# SCALABLE BULK DATA IMPORT SYSTEM
# =========================================================

@admin.route("/import", methods=["GET", "POST"])
@admin_required
def data_import():
    import json
    report = None

    if request.method == "POST":
        dataset_type = request.form.get("dataset_type", "").strip().lower()
        raw_json = request.form.get("raw_json", "").strip()
        uploaded_file = request.files.get("file")

        content = None
        if uploaded_file and uploaded_file.filename:
            try:
                content = json.load(uploaded_file)
            except Exception as e:
                flash(f"Failed to parse uploaded JSON file: {e}", "danger")
        elif raw_json:
            try:
                content = json.loads(raw_json)
            except Exception as e:
                flash(f"Failed to parse raw JSON: {e}", "danger")

        if not content:
            flash("Please upload a valid JSON file or paste JSON content.", "warning")
            return render_template("admin/import.html")

        if isinstance(content, dict):
            content = [content]

        imported_count = 0
        errors = []

        if dataset_type == "careers":
            for idx, item in enumerate(content, 1):
                title = item.get("title")
                if not title:
                    errors.append(f"Row {idx}: Missing 'title'")
                    continue
                slug = item.get("slug") or title.lower().replace(" ", "-")
                if Career.query.filter_by(slug=slug).first():
                    errors.append(f"Row {idx}: Career '{title}' already exists (Duplicate).")
                    continue

                obj = Career(
                    title=title,
                    slug=slug,
                    category=item.get("category", "General"),
                    description=item.get("description", "Career profile"),
                    average_salary=item.get("average_salary", "As per industry scale"),
                    future_scope=item.get("future_scope", "Growth opportunities"),
                    education_required=item.get("education_required", "Graduation"),
                    skills_required=item.get("skills_required", "Communication"),
                    official_url=item.get("official_url"),
                    source=item.get("source", "Admin Bulk Import"),
                    verification_status=item.get("verification_status", "VERIFIED")
                )
                db.session.add(obj)
                imported_count += 1

        elif dataset_type == "colleges":
            for idx, item in enumerate(content, 1):
                name = (item.get("name") or "").strip()
                if not name:
                    errors.append(f"Row {idx}: Missing 'name'")
                    continue

                state = (item.get("state") or "").strip()
                city = (item.get("city") or "").strip()
                short_name = (item.get("short_name") or "").strip()

                # Duplicate detection: check by exact/normalized name + state/city
                existing = College.query.filter(
                    func.lower(College.name) == name.lower()
                ).first()

                if not existing and short_name:
                    existing = College.query.filter(
                        func.lower(College.short_name) == short_name.lower()
                    ).first()

                if existing:
                    # Update existing record
                    existing.city = city or existing.city
                    existing.state = state or existing.state
                    existing.institution_type = item.get("institution_type") or item.get("college_type") or existing.institution_type
                    existing.government_private = item.get("government_private") or existing.government_private
                    existing.course = item.get("course") or existing.course
                    existing.official_website = item.get("official_website") or item.get("official_url") or existing.official_website
                    existing.source = item.get("source") or existing.source
                    existing.verification_status = item.get("verification_status") or existing.verification_status
                    existing.last_verified_at = datetime.utcnow()
                    updated_count += 1
                else:
                    obj = College(
                        name=name,
                        short_name=short_name,
                        city=city or "India",
                        state=state or "India",
                        institution_type=item.get("institution_type") or item.get("college_type", "Affiliated College"),
                        institution_category=item.get("institution_category", "College"),
                        government_private=item.get("government_private", "Government"),
                        course=item.get("course", "Degree programs"),
                        official_website=item.get("official_website") or item.get("official_url") or item.get("website", ""),
                        website=item.get("official_website") or item.get("official_url") or item.get("website", ""),
                        official_url=item.get("official_website") or item.get("official_url") or item.get("website", ""),
                        description=item.get("description", ""),
                        source=item.get("source", "Admin Bulk Import"),
                        verification_status=item.get("verification_status", "VERIFIED")
                    )
                    db.session.add(obj)
                    imported_count += 1

        elif dataset_type == "exams":
            for idx, item in enumerate(content, 1):
                exam_name = (item.get("exam_name") or item.get("name") or "").strip()
                if not exam_name:
                    errors.append(f"Row {idx}: Missing 'exam_name'")
                    continue

                short_name = (item.get("short_name") or "").strip()

                # Duplicate detection: check by exact or normalized name / short_name
                existing = GovernmentExam.query.filter(
                    (func.lower(GovernmentExam.exam_name) == exam_name.lower()) |
                    ((GovernmentExam.short_name != None) & (GovernmentExam.short_name != "") & (func.lower(GovernmentExam.short_name) == short_name.lower()) if short_name else False)
                ).first()

                if existing:
                    # Update existing record
                    existing.exam_name = exam_name
                    if short_name:
                        existing.short_name = short_name
                    existing.conducted_by = item.get("conducted_by") or existing.conducted_by
                    existing.category = item.get("category") or existing.category
                    existing.exam_type = item.get("exam_type") or existing.exam_type
                    existing.sub_category = item.get("sub_category") or existing.sub_category
                    existing.qualification = item.get("qualification") or existing.qualification
                    existing.streams = item.get("streams") or existing.streams
                    existing.age_limit = item.get("age_limit") or existing.age_limit
                    existing.state = item.get("state") or existing.state
                    existing.description = item.get("description") or existing.description
                    existing.selection_process = item.get("selection_process") or existing.selection_process
                    existing.career_opportunities = item.get("career_opportunities") or existing.career_opportunities
                    existing.official_website = item.get("official_url") or item.get("official_website") or existing.official_website
                    existing.official_url = item.get("official_url") or item.get("official_website") or existing.official_url
                    existing.status = item.get("status") or existing.status
                    existing.verification_status = item.get("verification_status") or "VERIFIED"
                    imported_count += 1
                else:
                    obj = GovernmentExam(
                        exam_name=exam_name,
                        short_name=short_name,
                        conducted_by=item.get("conducted_by", "Statutory Board"),
                        category=item.get("category", "General"),
                        exam_type=item.get("exam_type", "Recruitment"),
                        sub_category=item.get("sub_category", ""),
                        qualification=item.get("qualification") or item.get("eligibility", "Graduation"),
                        streams=item.get("streams", "Any Stream"),
                        age_limit=item.get("age_limit", "18-32 Years"),
                        state=item.get("state", "All India"),
                        national_or_state=item.get("national_or_state", "National"),
                        description=item.get("description", ""),
                        selection_process=item.get("selection_process", ""),
                        career_opportunities=item.get("career_opportunities", ""),
                        official_website=item.get("official_url") or item.get("official_website", ""),
                        official_url=item.get("official_url") or item.get("official_website", ""),
                        status=item.get("status", "GENERAL_INFORMATION"),
                        source=item.get("source", "Admin Bulk Import"),
                        verification_status=item.get("verification_status", "VERIFIED")
                    )
                    db.session.add(obj)
                    imported_count += 1

        elif dataset_type == "scholarships":
            for idx, item in enumerate(content, 1):
                title = item.get("title") or item.get("name")
                if not title:
                    errors.append(f"Row {idx}: Missing 'title'")
                    continue
                obj = Scholarship(
                    title=title,
                    provider=item.get("provider", "Government / Institutional"),
                    category=item.get("category", "General"),
                    eligibility=item.get("eligibility", "Recognized course enrollment"),
                    amount=item.get("amount", "Financial Support"),
                    website=item.get("official_url") or item.get("official_website", ""),
                    official_url=item.get("official_url") or item.get("official_website", ""),
                    source=item.get("source", "Admin Bulk Import"),
                    verification_status=item.get("verification_status", "VERIFIED")
                )
                db.session.add(obj)
                imported_count += 1

        elif dataset_type == "internships":
            for idx, item in enumerate(content, 1):
                title = item.get("title")
                if not title:
                    errors.append(f"Row {idx}: Missing 'title'")
                    continue
                raw_skills = item.get("skills", "")
                skills_str = ", ".join(raw_skills) if isinstance(raw_skills, list) else str(raw_skills)

                obj = Internship(
                    title=title,
                    company=item.get("company", "Organization"),
                    location=item.get("location", "India"),
                    mode=item.get("mode", "Hybrid"),
                    stipend=item.get("stipend", "Provided"),
                    duration=item.get("duration", "2-6 Months"),
                    skills=skills_str,
                    apply_link=item.get("official_url") or item.get("apply_link", ""),
                    official_url=item.get("official_url") or item.get("apply_link", ""),
                    domain=item.get("domain") or title.split()[0],
                    description=item.get("description", "Practical training opportunity"),
                    source=item.get("source", "Admin Bulk Import"),
                    verification_status=item.get("verification_status", "VERIFIED")
                )
                db.session.add(obj)
                imported_count += 1

        db.session.commit()
        flash(f"Import process complete: Successfully imported {imported_count} record(s).", "success")
        report = {
            "imported_count": imported_count,
            "errors": errors
        }

    return render_template("admin/import.html", report=report)


# =========================================================================
# COURSE MANAGEMENT & CURRICULUM CONTROLLER
# =========================================================================

@admin.route("/courses")
@admin_required
def admin_courses():
    search = request.args.get("search", "").strip()
    level = request.args.get("level", "").strip()
    discipline = request.args.get("discipline", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Course.query

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Course.name.ilike(pattern),
                Course.short_name.ilike(pattern),
                Course.aliases.ilike(pattern),
                Course.discipline.ilike(pattern)
            )
        )

    if level and level != "All":
        query = query.filter(Course.level == level)

    if discipline and discipline != "All":
        query = query.filter(Course.discipline.ilike(f"%{discipline}%"))

    query = query.order_by(Course.name.asc())
    pagination = query.paginate(page=page, per_page=20, error_out=False)

    levels_raw = db.session.query(Course.level).distinct().all()
    levels = sorted([l[0] for l in levels_raw if l[0]])

    disciplines_raw = db.session.query(Course.discipline).distinct().all()
    disciplines = sorted([d[0] for d in disciplines_raw if d[0]])

    # Count of offerings per course
    offering_counts = dict(
        db.session.query(
            CollegeCourse.course_id,
            func.count(CollegeCourse.id)
        )
        .group_by(CollegeCourse.course_id)
        .all()
    )

    return render_template(
        "admin/courses.html",
        courses=pagination.items,
        pagination=pagination,
        search=search,
        selected_level=level,
        selected_discipline=discipline,
        levels=levels,
        disciplines=disciplines,
        offering_counts=offering_counts
    )


@admin.route("/courses/create", methods=["POST"])
@admin_required
def admin_create_course():
    name = request.form.get("name", "").strip()
    short_name = request.form.get("short_name", "").strip()
    level = request.form.get("level", "UG").strip()
    discipline = request.form.get("discipline", "").strip()
    stream = request.form.get("stream", "").strip()
    duration = request.form.get("duration", "3 Years").strip()
    description = request.form.get("description", "").strip()
    aliases = request.form.get("aliases", "").strip()
    specialization = request.form.get("specialization", "").strip()
    eligibility_summary = request.form.get("eligibility_summary", "").strip()
    admission_modes = request.form.get("admission_modes", "").strip()

    if not name:
        flash("Course name is required.", "danger")
        return redirect(url_for("admin.admin_courses"))

    existing = Course.query.filter(func.lower(Course.name) == name.lower()).first()
    if existing:
        flash(f"Course '{name}' already exists in registry.", "warning")
        return redirect(url_for("admin.admin_courses"))

    new_course = Course(
        name=name,
        short_name=short_name or None,
        level=level,
        discipline=discipline or None,
        stream=stream or None,
        duration=duration or None,
        description=description or None,
        aliases=aliases or None,
        specialization=specialization or None,
        eligibility_summary=eligibility_summary or None,
        admission_modes=admission_modes or None
    )
    db.session.add(new_course)
    db.session.commit()
    flash(f"Canonical course '{name}' added successfully.", "success")
    return redirect(url_for("admin.admin_courses"))


@admin.route("/courses/<int:course_id>/edit", methods=["POST"])
@admin_required
def admin_edit_course(course_id):
    c = Course.query.get_or_404(course_id)
    c.name = request.form.get("name", c.name).strip()
    c.short_name = request.form.get("short_name", "").strip() or None
    c.level = request.form.get("level", c.level).strip()
    c.discipline = request.form.get("discipline", "").strip() or None
    c.stream = request.form.get("stream", "").strip() or None
    c.duration = request.form.get("duration", "").strip() or None
    c.description = request.form.get("description", "").strip() or None
    c.aliases = request.form.get("aliases", "").strip() or None
    c.specialization = request.form.get("specialization", "").strip() or None
    c.eligibility_summary = request.form.get("eligibility_summary", "").strip() or None
    c.admission_modes = request.form.get("admission_modes", "").strip() or None

    db.session.commit()
    flash(f"Course '{c.name}' updated successfully.", "success")
    return redirect(url_for("admin.admin_courses"))


@admin.route("/courses/<int:course_id>/delete", methods=["POST"])
@admin_required
def admin_delete_course(course_id):
    c = Course.query.get_or_404(course_id)
    name = c.name
    db.session.delete(c)
    db.session.commit()
    flash(f"Course '{name}' and associated mappings deleted.", "info")
    return redirect(url_for("admin.admin_courses"))


@admin.route("/courses/<int:course_id>/institutions")
@admin_required
def admin_course_institutions(course_id):
    c = Course.query.get_or_404(course_id)
    page = request.args.get("page", 1, type=int)

    query = (
        db.session.query(CollegeCourse, College)
        .join(College, CollegeCourse.college_id == College.id)
        .filter(CollegeCourse.course_id == c.id)
        .order_by(College.name.asc())
    )
    pagination = query.paginate(page=page, per_page=25, error_out=False)

    # All colleges for quick add dropdown
    colleges = College.query.with_entities(College.id, College.name, College.city, College.state).order_by(College.name.asc()).all()

    return render_template(
        "admin/course_colleges.html",
        course=c,
        mappings=pagination.items,
        pagination=pagination,
        colleges=colleges
    )


@admin.route("/courses/<int:course_id>/institutions/add", methods=["POST"])
@admin_required
def admin_add_course_institution(course_id):
    course_obj = Course.query.get_or_404(course_id)
    college_id = request.form.get("college_id", type=int)
    program_name = request.form.get("program_name", "").strip() or course_obj.name
    specialization = request.form.get("specialization", "").strip() or None
    admission_mode = request.form.get("admission_mode", "Merit-Based / State Counseling").strip()
    seats = request.form.get("seats", type=int)
    status = request.form.get("verification_status", "VERIFIED").strip()

    if not college_id:
        flash("Please select a college.", "danger")
        return redirect(url_for("admin.admin_course_institutions", course_id=course_id))

    existing = CollegeCourse.query.filter_by(college_id=college_id, course_id=course_id).first()
    if existing:
        flash("This institution is already mapped to this course.", "warning")
        return redirect(url_for("admin.admin_course_institutions", course_id=course_id))

    cc = CollegeCourse(
        college_id=college_id,
        course_id=course_id,
        program_name=program_name,
        specialization=specialization,
        level=course_obj.level,
        duration=course_obj.duration,
        admission_mode=admission_mode,
        seats=seats,
        source="Admin Manual Verification",
        verification_status=status
    )
    db.session.add(cc)
    db.session.commit()
    flash("Institution successfully mapped to course.", "success")
    return redirect(url_for("admin.admin_course_institutions", course_id=course_id))


@admin.route("/courses/mapping/<int:mapping_id>/status", methods=["POST"])
@admin_required
def admin_update_mapping_status(mapping_id):
    cc = CollegeCourse.query.get_or_404(mapping_id)
    new_status = request.form.get("status", "VERIFIED").strip()
    if new_status in ["VERIFIED", "NEEDS_REVIEW", "ARCHIVED"]:
        cc.verification_status = new_status
        db.session.commit()
        flash(f"Mapping status updated to {new_status}.", "success")
    return redirect(request.referrer or url_for("admin.admin_courses"))


@admin.route("/courses/mapping/<int:mapping_id>/delete", methods=["POST"])
@admin_required
def admin_delete_mapping(mapping_id):
    cc = CollegeCourse.query.get_or_404(mapping_id)
    course_id = cc.course_id
    db.session.delete(cc)
    db.session.commit()
    flash("Course offering relationship removed.", "info")
    return redirect(request.referrer or url_for("admin.admin_course_institutions", course_id=course_id))


# =========================================================================
# DATA QUALITY AUDIT DASHBOARD (Section 29)
# =========================================================================

@admin.route("/data-quality")
@admin_required
def admin_data_quality():
    total_institutions = College.query.count()
    total_courses = Course.query.count()
    total_relationships = CollegeCourse.query.count()
    verified_relationships = CollegeCourse.query.filter_by(verification_status="VERIFIED").count()
    needs_review = CollegeCourse.query.filter_by(verification_status="NEEDS_REVIEW").count()
    archived = CollegeCourse.query.filter_by(verification_status="ARCHIVED").count()

    institutions_with_courses = (
        db.session.query(func.count(func.distinct(CollegeCourse.college_id)))
        .scalar() or 0
    )
    institutions_without_courses = total_institutions - institutions_with_courses

    # Top courses by verified coverage
    top_courses = (
        db.session.query(
            Course.name,
            Course.level,
            Course.discipline,
            func.count(CollegeCourse.id).label("c_count")
        )
        .join(CollegeCourse, Course.id == CollegeCourse.course_id)
        .filter(CollegeCourse.verification_status == "VERIFIED")
        .group_by(Course.id)
        .order_by(func.count(CollegeCourse.id).desc())
        .limit(10)
        .all()
    )

    # State coverage breakdown
    state_coverage = (
        db.session.query(
            College.state,
            func.count(func.distinct(College.id)).label("total_inst"),
            func.count(func.distinct(CollegeCourse.college_id)).label("inst_with_courses")
        )
        .outerjoin(CollegeCourse, College.id == CollegeCourse.college_id)
        .group_by(College.state)
        .order_by(func.count(func.distinct(College.id)).desc())
        .limit(12)
        .all()
    )

    # ---------------------------------------------------------
    # Career Coverage & Domain Balance Audit (Sections 26 & 27)
    # ---------------------------------------------------------
    from models.career_course import CareerCourse
    from models.career_exam import CareerExam
    from models.career_skill import CareerSkill

    total_careers = Career.query.count()
    total_career_courses = CareerCourse.query.count()
    total_career_exams = CareerExam.query.count()
    total_career_skills = CareerSkill.query.count()
    total_career_roadmaps = CareerRoadmap.query.count()

    verified_careers = Career.query.filter(Career.verification_status == "VERIFIED").count()
    review_careers = total_careers - verified_careers
    lesser_known_careers = Career.query.filter(Career.is_lesser_known == True).count()

    # Category breakdown with balance percentage
    category_counts = (
        db.session.query(Career.category, func.count(Career.id))
        .group_by(Career.category)
        .order_by(func.count(Career.id).desc())
        .all()
    )
    category_distribution = []
    for cat_name, cnt in category_counts:
        pct = round((cnt / total_careers * 100), 1) if total_careers else 0
        category_distribution.append({
            "category": cat_name,
            "count": cnt,
            "percentage": pct
        })

    # Tech vs Non-Tech balance ratio
    tech_count = Career.query.filter(Career.category.in_(["Technology & Computer Science", "Engineering & Manufacturing"])).count()
    non_tech_count = total_careers - tech_count
    tech_pct = round((tech_count / total_careers * 100), 1) if total_careers else 0
    non_tech_pct = round((non_tech_count / total_careers * 100), 1) if total_careers else 0

    return render_template(
        "admin/data_quality.html",
        stats={
            "total_institutions": total_institutions,
            "total_courses": total_courses,
            "total_relationships": total_relationships,
            "verified_relationships": verified_relationships,
            "needs_review": needs_review,
            "archived": archived,
            "institutions_with_courses": institutions_with_courses,
            "institutions_without_courses": institutions_without_courses,
            "coverage_pct": round((institutions_with_courses / total_institutions * 100), 1) if total_institutions else 0
        },
        top_courses=top_courses,
        state_coverage=state_coverage,
        career_audit={
            "total_careers": total_careers,
            "verified_careers": verified_careers,
            "review_careers": review_careers,
            "lesser_known_careers": lesser_known_careers,
            "total_career_courses": total_career_courses,
            "total_career_exams": total_career_exams,
            "total_career_skills": total_career_skills,
            "total_career_roadmaps": total_career_roadmaps,
            "tech_count": tech_count,
            "non_tech_count": non_tech_count,
            "tech_pct": tech_pct,
            "non_tech_pct": non_tech_pct,
            "category_distribution": category_distribution
        }
    )

