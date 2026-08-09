from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.assessment import AssessmentResult

assessment = Blueprint(
    "assessment",
    __name__,
    url_prefix="/assessment"
)


# ==========================================
# Start Assessment
# ==========================================

@assessment.route("/")
def start():

    return render_template(
        "assessment/smart_questions.html"
    )


# ==========================================
# Submit Assessment
# ==========================================

@assessment.route("/submit", methods=["POST"])
def submit():

    # --------------------------------------
    # Get Form Data
    # --------------------------------------

    current_class = request.form.get("current_class")
    stream = request.form.get("stream")
    preference = request.form.get("preference")
    activity = request.form.get("activity")
    strong_subject = request.form.get("strong_subject")
    personality = request.form.get("personality")
    government_exam = request.form.get("government_exam")
    technical_skill = request.form.get("technical_skill")
    long_term_goal = request.form.get("long_term_goal")
    study_hours = request.form.get("study_hours")

    # --------------------------------------
    # AI Career Scores
    # --------------------------------------

    scores = {

        "AI Engineer": 0,
        "Software Engineer": 0,
        "Data Scientist": 0,
        "Cyber Security Analyst": 0,
        "Doctor": 0,
        "Pharmacist": 0,
        "Chartered Accountant": 0,
        "Business Analyst": 0,
        "Digital Marketer": 0,
        "IAS Officer": 0,
        "SSC / Railway Officer": 0,
        "Lawyer": 0,
        "Teacher / Professor": 0,
        "UI/UX Designer": 0,
        "Graphic Designer": 0,
        "Entrepreneur": 0

    }

    # --------------------------------------
    # Stream Based
    # --------------------------------------

    if stream == "PCM":

        scores["AI Engineer"] += 4
        scores["Software Engineer"] += 4
        scores["Data Scientist"] += 3
        scores["Cyber Security Analyst"] += 3

    elif stream == "PCB":

        scores["Doctor"] += 5
        scores["Pharmacist"] += 3

    elif stream == "Commerce":

        scores["Chartered Accountant"] += 5
        scores["Business Analyst"] += 4
        scores["Digital Marketer"] += 2

    elif stream == "Arts":

        scores["Lawyer"] += 4
        scores["Teacher / Professor"] += 4
        scores["IAS Officer"] += 3

    # --------------------------------------
    # Activity Based
    # --------------------------------------

    if activity == "Coding / Building Apps":

        scores["AI Engineer"] += 5
        scores["Software Engineer"] += 5
        scores["Data Scientist"] += 3

    elif activity == "Helping Sick People":

        scores["Doctor"] += 5

    elif activity == "Managing Money / Business":

        scores["Chartered Accountant"] += 4
        scores["Business Analyst"] += 4
        scores["Entrepreneur"] += 3

    elif activity == "Teaching / Explaining":

        scores["Teacher / Professor"] += 5

    elif activity == "Drawing / Designing":

        scores["UI/UX Designer"] += 5
        scores["Graphic Designer"] += 5

    elif activity == "Leading Teams":

        scores["IAS Officer"] += 4
        scores["Entrepreneur"] += 5

    # --------------------------------------
    # Strong Subject
    # --------------------------------------

    if strong_subject == "Mathematics":

        scores["AI Engineer"] += 4
        scores["Software Engineer"] += 3
        scores["Data Scientist"] += 4

    elif strong_subject == "Biology":

        scores["Doctor"] += 5

    elif strong_subject == "Accountancy":

        scores["Chartered Accountant"] += 5

    elif strong_subject == "Economics":

        scores["Business Analyst"] += 4

    elif strong_subject == "English":

        scores["Lawyer"] += 3
        scores["Teacher / Professor"] += 3

    # --------------------------------------
    # Personality Based
    # --------------------------------------

    if personality == "Analytical Thinker":

        scores["AI Engineer"] += 4
        scores["Data Scientist"] += 4

    elif personality == "Creative Person":

        scores["UI/UX Designer"] += 4
        scores["Graphic Designer"] += 4
        scores["Digital Marketer"] += 3

    elif personality == "Leader / Organizer":

        scores["IAS Officer"] += 4
        scores["Entrepreneur"] += 4

    elif personality == "Helpful / Caring":

        scores["Doctor"] += 3
        scores["Teacher / Professor"] += 3

    # --------------------------------------
    # Job Preference
    # --------------------------------------

    if preference == "Government":

        scores["IAS Officer"] += 5
        scores["SSC / Railway Officer"] += 4

    elif preference == "Private":

        scores["Software Engineer"] += 3
        scores["Business Analyst"] += 3
        scores["Digital Marketer"] += 2

    elif preference == "Business / Startup":

        scores["Entrepreneur"] += 6

    elif preference == "Freelancing / Remote Work":

        scores["Graphic Designer"] += 5
        scores["UI/UX Designer"] += 4
        scores["Digital Marketer"] += 4

    # --------------------------------------
    # Government Exam Interest
    # --------------------------------------

    if government_exam == "Very Interested":

        scores["IAS Officer"] += 5
        scores["SSC / Railway Officer"] += 4

    # --------------------------------------
    # Technical Skills
    # --------------------------------------

    if technical_skill == "Python / Programming":

        scores["AI Engineer"] += 4
        scores["Software Engineer"] += 4
        scores["Data Scientist"] += 3

    elif technical_skill == "Web Development":

        scores["Software Engineer"] += 3

    elif technical_skill == "Canva / Design":

        scores["UI/UX Designer"] += 3
        scores["Graphic Designer"] += 4

    elif technical_skill == "Data Analysis":

        scores["Data Scientist"] += 4
        scores["Business Analyst"] += 3

    # --------------------------------------
    # Long Term Goal
    # --------------------------------------

    goal_map = {

        "Become an Engineer": "Software Engineer",
        "Become a Doctor": "Doctor",
        "Become a Chartered Accountant": "Chartered Accountant",
        "Become an IAS / IPS Officer": "IAS Officer",
        "Become a Teacher / Professor": "Teacher / Professor",
        "Become a Lawyer / Judge": "Lawyer",
        "Become a Designer / Creator": "UI/UX Designer",
        "Become a Data Scientist / AI Expert": "AI Engineer",
        "Start My Own Business": "Entrepreneur"

    }

    if long_term_goal in goal_map:

        scores[goal_map[long_term_goal]] += 6

    # --------------------------------------
    # Study Hours
    # --------------------------------------

    if study_hours in ["6-8 Hours", "More than 8 Hours"]:

        scores["IAS Officer"] += 2
        scores["Doctor"] += 2
        scores["Chartered Accountant"] += 2

    # --------------------------------------
    # Top 5 Careers
    # --------------------------------------

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_careers = sorted_scores[:5]

    max_score = top_careers[0][1] if top_careers else 1

    career_results = []

    for name, score in top_careers:

        percentage = round(
            (score / max_score) * 100
        )

        career_results.append({

            "name": name,
            "score": score,
            "percentage": percentage

        })

    # Best Career

    best_career = career_results[0]["name"]

    # --------------------------------------
    # Save to Database
    # --------------------------------------

    result = AssessmentResult(

        user_id=session.get("user_id"),

        recommended_category=best_career

    )

    db.session.add(result)

    db.session.commit()

    # --------------------------------------
    # Save Full Report in Session
    # --------------------------------------

    session["assessment_data"] = {

        "current_class": current_class,
        "stream": stream,
        "preference": preference,
        "activity": activity,
        "strong_subject": strong_subject,
        "personality": personality,
        "government_exam": government_exam,
        "technical_skill": technical_skill,
        "long_term_goal": long_term_goal,
        "study_hours": study_hours,
        "top_careers": career_results

    }

    return redirect(
        url_for(
            "assessment.result",
            result_id=result.id
        )
    )


# ==========================================
# Result Page
# ==========================================

@assessment.route("/result/<int:result_id>")
def result(result_id):

    result = AssessmentResult.query.get_or_404(
        result_id
    )

    data = session.get("assessment_data", {})

    return render_template(

        "assessment/smart_result.html",

        result=result,

        data=data,

        top_careers=data.get("top_careers", [])

    )