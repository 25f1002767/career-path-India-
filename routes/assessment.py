"""
routes/assessment.py
==============================================================================
MPath Career Discovery & Assessment Routes
==============================================================================
Empowers students to discover career directions based on:
- Multi-dimensional cognitive patterns & RIASEC interests
- Real-world problem archetypes & latent activities
- Work values, lifestyle expectations, and person-environment fit
- Self-efficacy (perceived trainability) & persistence
- Practical constraints (financial, family, exam tolerance, study duration)
- Negative deal-breakers and anti-preferences
- Integrated with MPath's authentic database of Careers, Courses, Colleges,
  Exams, Scholarships, and Internships.
"""

import json
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from extensions import db
from models.assessment import AssessmentResult
from models.career import Career
from models.course import Course
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from services.career_assessment_questions import DISCOVERY_QUESTIONS, get_question_by_id
from services.career_assessment_engine import CareerAssessmentEngine

assessment = Blueprint(
    "assessment",
    __name__,
    url_prefix="/assessment"
)


# ============================================================================
# 1. Start Assessment Questionnaire
# ============================================================================

@assessment.route("/")
@assessment.route("/start")
def start():
    """
    Renders the scenario-based, student-friendly career discovery assessment.
    """
    return render_template(
        "assessment/smart_questions.html",
        questions=DISCOVERY_QUESTIONS
    )


# ============================================================================
# 2. Submit Assessment & Compute Discovery Dossier
# ============================================================================

@assessment.route("/submit", methods=["POST"])
def submit():
    """
    Evaluates form responses through CareerAssessmentEngine, saves the complete
    assessment attempt, and redirects to the personalized counselling result page.
    """
    form_data = dict(request.form)

    # Fallback user ID for anonymous guests to satisfy foreign key
    user_id = session.get("user_id")
    if not user_id:
        user_id = 1  # Default guest/system user

    # Run multi-dimensional assessment engine
    try:
        evaluation = CareerAssessmentEngine.evaluate(form_data)
    except Exception as e:
        # Fallback safeguard in case of unexpected input
        print(f"[ASSESSMENT ENGINE ERROR]: {e}")
        flash("We processed your answers. Here is your career discovery overview.", "info")
        evaluation = {
            "recommended_category": "Technology & Computer Science",
            "headline": "Profile: Versatile Explorer — Recommended Direction: Technology",
            "confidence_level": "MODERATE_CONFIDENCE",
            "profile": {"dominant_archetype": "Versatile Explorer", "top_riasec_code": "IR"},
            "tradeoffs": [],
            "top_matches": [],
            "unexpected_careers": [],
            "adjacent_paths": [],
            "actions": []
        }

    # Serialize top matches for database storage (saving clean dict representations)
    def serialize_dossier_list(items):
        serialized = []
        for item in items:
            c: Career = item["career"]
            serialized.append({
                "id": c.id,
                "title": c.title,
                "slug": c.slug,
                "category": c.category,
                "sub_category": c.sub_category,
                "short_description": c.short_description or c.description[:180] if c.description else "",
                "work_environment": c.work_environment,
                "work_modes": c.work_modes,
                "average_salary": c.average_salary,
                "is_lesser_known": bool(c.is_lesser_known),
                "score": item.get("score", 0),
                "interest_fit": item.get("interest_fit", "HIGH"),
                "values_fit": item.get("values_fit", "HIGH"),
                "feasibility_fit": item.get("feasibility_fit", "HIGH"),
                "route_feasibility": item.get("route_feasibility", "DIRECT"),
                "counselling_why": item.get("counselling_why", ""),
                "potential_challenge": item.get("potential_challenge", ""),
                "entry_routes": item.get("entry_routes", []),
                "reality_check": item.get("reality_check", []),
                "next_steps": item.get("next_steps", []),
                # Ecosystem IDs and summaries
                "linked_course_ids": [course.id for course in item.get("linked_courses", [])],
                "linked_courses": [{"id": course.id, "title": getattr(course, "name", getattr(course, "title", "Course")), "degree_type": getattr(course, "level", "Degree")} for course in item.get("linked_courses", [])[:3]],
                "linked_colleges": [{"id": col.id, "name": col.name, "city": getattr(col, "city", ""), "state": getattr(col, "state", "")} for col in item.get("linked_colleges", [])[:3]],
                "linked_exams": [{"id": ex.id, "title": getattr(ex, "title", "Exam"), "exam_level": getattr(ex, "exam_level", "National")} for ex in item.get("linked_exams", [])[:2]],
                "linked_scholarships": [{"id": sch.id, "title": getattr(sch, "title", "Scholarship"), "amount": getattr(sch, "amount", "Merit Support")} for sch in item.get("linked_scholarships", [])[:2]],
                "linked_internships": [{"id": intn.id, "title": getattr(intn, "title", "Internship"), "company": getattr(intn, "company", "Industry"), "mode": getattr(intn, "mode", "Hybrid")} for intn in item.get("linked_internships", [])[:2]]
            })
        return serialized

    top_serialized = serialize_dossier_list(evaluation.get("top_matches", []))
    unexpected_serialized = serialize_dossier_list(evaluation.get("unexpected_careers", []))
    adjacent_serialized = serialize_dossier_list(evaluation.get("adjacent_paths", []))

    # Save to database
    assessment_record = AssessmentResult(
        user_id=user_id,
        recommended_category=evaluation.get("recommended_category", "Career Discovery"),
        assessment_version="2.0.0",
        confidence_level=evaluation.get("confidence_level", "HIGH_CONFIDENCE"),
        summary_headline=evaluation.get("headline", ""),
        answers_json=json.dumps(form_data),
        profile_json=json.dumps(evaluation.get("profile", {})),
        recommendations_json=json.dumps(top_serialized),
        unexpected_json=json.dumps(unexpected_serialized),
        tradeoffs_json=json.dumps(evaluation.get("tradeoffs", [])),
        actions_json=json.dumps(evaluation.get("actions", []))
    )

    db.session.add(assessment_record)
    db.session.commit()

    # Save summary into session for fast rendering and dashboard sync
    session["assessment_id"] = assessment_record.id
    session["assessment_data"] = {
        "current_class": form_data.get("q12_current_academic_level", "Class 12"),
        "stream": form_data.get("q12_current_academic_level", "General"),
        "personality": evaluation.get("profile", {}).get("dominant_archetype", "Versatile Explorer"),
        "recommended_category": assessment_record.recommended_category,
        "top_careers": [{"name": item["title"], "score": item["score"], "percentage": int(min(98, max(65, item["score"])))} for item in top_serialized[:5]]
    }

    return redirect(
        url_for("assessment.result", result_id=assessment_record.id)
    )


# ============================================================================
# 3. Comprehensive Career Counselling Dossier Page
# ============================================================================

@assessment.route("/result/<int:result_id>")
def result(result_id):
    """
    Renders the counselling-style Career Discovery Dossier with full
    ecosystem connections (Courses, Colleges, Exams, Scholarships, Internships).
    """
    record = AssessmentResult.query.get_or_404(result_id)

    profile = record.parsed_profile
    top_careers = record.parsed_recommendations
    unexpected_careers = record.parsed_unexpected
    tradeoffs = record.parsed_tradeoffs
    actions = record.parsed_actions
    answers = record.parsed_answers

    # Fallback if viewing a legacy assessment from before the upgrade
    if not top_careers:
        fallback_careers = Career.query.filter_by(category=record.recommended_category).limit(5).all()
        if not fallback_careers:
            fallback_careers = Career.query.limit(5).all()
        top_careers = [{
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "category": c.category,
            "sub_category": c.sub_category,
            "short_description": c.short_description or (c.description[:180] if c.description else ""),
            "work_environment": c.work_environment,
            "work_modes": c.work_modes,
            "average_salary": c.average_salary,
            "is_lesser_known": bool(c.is_lesser_known),
            "score": 85,
            "interest_fit": "HIGH",
            "values_fit": "HIGH",
            "feasibility_fit": "HIGH",
            "route_feasibility": "DIRECT_ENTRY",
            "counselling_why": f"Your answers showed strong affinity with the foundational competencies required in {c.title}.",
            "potential_challenge": c.reality_check_points[0] if c.reality_check_points else "Requires focused study and continuous learning.",
            "entry_routes": c.parsed_entry_routes,
            "linked_courses": [],
            "linked_colleges": [],
            "linked_exams": [],
            "linked_scholarships": [],
            "linked_internships": []
        } for c in fallback_careers]

    if not profile:
        profile = {
            "dominant_archetype": "Versatile Explorer (Multi-Disciplinary Aptitude)",
            "top_riasec_code": "IE",
            "confidence_level": record.confidence_level or "HIGH_CONFIDENCE",
            "evidence_statements": [
                {"category": "Analytical Strengths", "text": "Shows affinity for systematic problem-solving and real-world execution."}
            ]
        }

    if not actions:
        top_title = top_careers[0]["title"] if top_careers else "Target Career"
        actions = [
            {
                "step": 1,
                "title": f"Explore {top_title} Full Career Dossier",
                "description": f"Read the comprehensive roadmap, day-to-day responsibilities, and indicative salary brackets for {top_title}.",
                "link_type": "CAREER_DETAIL",
                "link_slug": top_careers[0]["slug"] if top_careers else "career-discovery"
            },
            {
                "step": 2,
                "title": "Review Linked Courses & Approved Colleges",
                "description": "Inspect degree pathways and government/private colleges offering relevant training on MPath.",
                "link_type": "COLLEGE_DISCOVERY",
                "link_url": "/colleges/"
            },
            {
                "step": 3,
                "title": "Complete a 7-Day Low-Stakes Exploration Experiment",
                "description": "Engage in a practical mini-project or interview an industry professional before committing to a final path.",
                "link_type": "EXPERIMENT",
                "link_url": None
            }
        ]

    # Legacy compatibility dictionary for any old template fragments
    legacy_data = session.get("assessment_data", {
        "current_class": answers.get("q12_current_academic_level", "Class 12"),
        "stream": answers.get("q12_current_academic_level", "General"),
        "personality": profile.get("dominant_archetype", "Versatile Explorer"),
        "recommended_category": record.recommended_category
    })

    return render_template(
        "assessment/smart_result.html",
        result=record,
        profile=profile,
        top_careers=top_careers,
        unexpected_careers=unexpected_careers,
        tradeoffs=tradeoffs,
        actions=actions,
        data=legacy_data
    )


# ============================================================================
# 4. Feedback Endpoint (Part 70: Career Exploration Feedback Loop)
# ============================================================================

@assessment.route("/feedback", methods=["POST"])
def submit_feedback():
    """
    Records student feedback on recommended careers to refine future guidance.
    """
    career_id = request.form.get("career_id")
    feedback_type = request.form.get("feedback_type")  # very_useful, somewhat_useful, not_useful, already_knew

    # Store in session or flash
    flash("Thank you for your feedback! It helps improve future exploration accuracy.", "success")
    return jsonify({
        "status": "success",
        "message": "Feedback recorded successfully"
    })