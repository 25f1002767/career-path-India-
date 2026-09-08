from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file
)

from functools import wraps
from io import BytesIO

from sqlalchemy import or_
from openpyxl import Workbook

from extensions import db

from models.user import User
from models.career import Career
from models.college import College
from models.scholarship import Scholarship
from models.internship import Internship
from models.exam import GovernmentExam
from models.assessment import AssessmentResult
from models.roadmap import CareerRoadmap
from models.website_visit import WebsiteVisit


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
# CAREER MANAGEMENT
# =========================================================

@admin.route("/careers")
@admin_required
def careers():

    search = request.args.get(
        "search",
        ""
    ).strip()

    if search:

        careers = Career.query.filter(
            Career.title.ilike(
                f"%{search}%"
            )
        ).order_by(
            Career.title.asc()
        ).all()

    else:

        careers = Career.query.order_by(
            Career.title.asc()
        ).all()

    return render_template(
        "admin/careers.html",
        careers=careers,
        search=search
    )


@admin.route(
    "/careers/add",
    methods=["GET", "POST"]
)
@admin_required
def add_career():

    if request.method == "POST":

        title = request.form["title"]

        category = request.form["category"]

        description = request.form["description"]

        average_salary = request.form[
            "average_salary"
        ]

        future_scope = request.form[
            "future_scope"
        ]

        education_required = request.form[
            "education_required"
        ]

        skills_required = request.form[
            "skills_required"
        ]

        slug = title.lower().replace(
            " ",
            "-"
        )

        career = Career(

            title=title,

            slug=slug,

            category=category,

            description=description,

            average_salary=average_salary,

            future_scope=future_scope,

            education_required=education_required,

            skills_required=skills_required

        )

        db.session.add(career)

        db.session.commit()

        flash(
            "Career Added Successfully!",
            "success"
        )

        return redirect(
            url_for(
                "admin.careers"
            )
        )

    return render_template(
        "admin/add_career.html"
    )


@admin.route(
    "/careers/edit/<int:id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_career(id):

    career = Career.query.get_or_404(id)

    if request.method == "POST":

        career.title = request.form[
            "title"
        ]

        career.category = request.form[
            "category"
        ]

        career.description = request.form[
            "description"
        ]

        career.average_salary = request.form[
            "average_salary"
        ]

        career.future_scope = request.form[
            "future_scope"
        ]

        career.education_required = request.form[
            "education_required"
        ]

        career.skills_required = request.form[
            "skills_required"
        ]

        db.session.commit()

        flash(
            "Career Updated Successfully!",
            "success"
        )

        return redirect(
            url_for(
                "admin.careers"
            )
        )

    return render_template(
        "admin/edit_career.html",
        career=career
    )


@admin.route(
    "/careers/delete/<int:id>"
)
@admin_required
def delete_career(id):

    career = Career.query.get_or_404(id)

    db.session.delete(career)

    db.session.commit()

    flash(
        "Career Deleted Successfully!",
        "warning"
    )

    return redirect(
        url_for(
            "admin.careers"
        )
    )


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