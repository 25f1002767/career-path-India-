"""
services/career_counselling_engine.py
==============================================================================
AI Career Counsellor Grounded in Structured Database Facts
==============================================================================
"""

import re
from sqlalchemy import or_
from extensions import db
from models.career import Career
from models.course import Course, CollegeCourse
from models.college import College
from models.exam import GovernmentExam
from models.career_course import CareerCourse
from models.career_exam import CareerExam
from models.roadmap import CareerRoadmap
from services.ai_client import client

SYSTEM_PROMPT = """You are MPath's National Career Discovery & Counselling Expert.
Your guiding ethical principle:
"AI student ka future decide nahi karega. AI student ko apne future ki possibilities discover karne mein help karega."

Core Directives:
1. STRICT ZERO BIAS: Never assume Technology = future, Engineering = success, Coding = best career, or B.Tech = default pathway.
2. EQUAL PRESTIGE & RESPECT: Treat Doctor, Teacher, Lawyer, Artist, Writer, Civil Servant, Psychologist, Nurse, Agri-professional, Designer, Chef, Pilot, Researcher, Social Worker, Electrician, and Sports Professional as deeply legitimate and noble possibilities.
3. WHEN A STUDENT DISLIKES CODING/ENGINEERING: NEVER recommend another tech role. Probe their natural affinities (helping people, biology, language, commerce, law, governance, art, sports, agriculture, trades, research).
4. MULTI-ROUTE HONESTY: Clearly distinguish Path A (Standard Route) from Path B (Alternative/Lateral Route). Explain licensing and regulatory prerequisites without casual shortcuts.
5. GROUNDING: Ground your guidance in verified Indian degrees, regulatory councils (NMC, BCI, COA, RCI, DGCA, AICTE, UGC, NCVT), and entrance examinations.
6. NO SALARY PROMISES: State that compensation ranges are indicative and depend on skill, performance, institution, and experience.
"""

def retrieve_grounding_context(query_text, career_slug=None):
    """
    Retrieves matching database facts to ground the AI counsellor.
    """
    context = {}
    target_career = None

    if career_slug:
        target_career = Career.query.filter_by(slug=career_slug).first()

    if not target_career:
        # Search careers by title and keywords
        tokens = [t.strip().lower() for t in re.split(r"[^\w]+", query_text) if len(t.strip()) > 3]
        if tokens:
            filters = []
            for t in tokens[:4]:
                filters.append(Career.title.ilike(f"%{t}%"))
                filters.append(Career.category.ilike(f"%{t}%"))
                filters.append(Career.technical_skills.ilike(f"%{t}%"))
            target_career = Career.query.filter(or_(*filters)).first()

    if target_career:
        context["career"] = {
            "title": target_career.title,
            "category": target_career.category,
            "sub_category": target_career.sub_category,
            "industry": target_career.industry,
            "what_they_do": target_career.what_they_do,
            "minimum_qualification": target_career.minimum_qualification,
            "preferred_streams": target_career.preferred_streams,
            "required_subjects": target_career.required_subjects,
            "technical_skills": target_career.technical_skills_list,
            "soft_skills": target_career.soft_skills_list,
            "tools": target_career.tools_list,
            "salary_indicative": target_career.salary_indicative or target_career.average_salary,
            "work_modes": target_career.work_modes,
            "official_source": f"{target_career.source} ({target_career.official_url})",
            "entry_routes": target_career.parsed_entry_routes,
            "progression": target_career.parsed_career_progression
        }

        # Courses linked
        c_courses = CareerCourse.query.filter_by(career_id=target_career.id).all()
        context["courses"] = []
        for cc in c_courses[:4]:
            if cc.course:
                context["courses"].append({
                    "name": cc.course.name,
                    "level": cc.course.level,
                    "duration": cc.course.duration,
                    "type": cc.relationship_type
                })

        # Exams linked
        c_exams = CareerExam.query.filter_by(career_id=target_career.id).all()
        context["exams"] = []
        for ce in c_exams[:4]:
            if ce.exam:
                context["exams"].append({
                    "name": ce.exam.name,
                    "type": ce.exam.exam_type,
                    "importance": ce.importance,
                    "conducting_body": ce.exam.conducting_body
                })

    return context

def generate_counsellor_response(user_query, career_slug=None):
    """
    Generates a structured, grounded response to the student's question.
    """
    context = retrieve_grounding_context(user_query, career_slug)

    # If client is configured and has API key, call generative model
    if client and hasattr(client, "models") and hasattr(client.models, "generate_content"):
        try:
            grounding_text = json.dumps(context, indent=2) if context else "General Indian Career Landscape"
            prompt = f"""Student Question: {user_query}

Database Verified Grounding Information:
{grounding_text}

Instructions:
1. Provide a direct, empathetic, and factual answer to the student's question.
2. If discussing a specific career, outline Path A (Standard Route) and Path B (Alternative/Lateral Route).
3. Mention verified qualifying courses and entrance exams from the grounding data.
4. Highlight technical and soft skills to cultivate.
5. Remind the student that AI helps explore possibilities, but their passions, values, and diligence shape their path."""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"system_instruction": SYSTEM_PROMPT}
            )
            if response and response.text:
                return response.text
        except Exception as e:
            # Fall back to structured DB-informed synthesis
            pass

    # High-quality factual synthesis from database records
    if context.get("career"):
        c = context["career"]
        courses_str = ", ".join([f"{item['name']} ({item['type']})" for item in context.get("courses", [])]) or c["minimum_qualification"]
        exams_str = ", ".join([f"{item['name']} ({item['importance']})" for item in context.get("exams", [])]) or "Standard institutional entrance examinations"
        tech_skills = ", ".join(c["technical_skills"][:5])
        soft_skills = ", ".join(c["soft_skills"][:3])
        routes_summary = ""
        if c.get("entry_routes"):
            for r in c["entry_routes"][:2]:
                routes_summary += f"\n- **{r.get('title', 'Pathway')}**: {r.get('steps', r.get('description', ''))}"

        return f"""### MPath Career Guidance: **{c['title']}**

**1. Possibility & Realistic Discovery**
You are inquiring about **{c['title']}** in the **{c['category']}** sector.
{c['what_they_do']}

> **Core Counselling Principle:** *MPath AI does not decide your future; our role is to reveal verified possibilities so you can make informed decisions based on your individual strengths.*

**2. Academic Eligibility & Preferred Streams**
- **Minimum Qualification:** {c['minimum_qualification']}
- **Preferred Stream(s):** {c['preferred_streams']}
- **Required / Recommended Subjects:** {c['required_subjects']}

**3. Grounded Entry Pathways**
{routes_summary if routes_summary else f"- Standard Route: Class 12 -> Recognized Degree in {courses_str} -> Entry-level position."}

**4. Key Qualifying Courses & Competitive Exams**
- **Recommended Degrees:** {courses_str}
- **Recognized Entrance / Recruitment Exams:** {exams_str}

**5. Essential Skill Toolkit**
- **Core Technical Skills:** {tech_skills}
- **Essential Soft Skills:** {soft_skills}
- **Industry Tools:** {', '.join(c['tools'][:4]) if c.get('tools') else 'Industry standard software'}

**6. Career Progression & Indicative Compensation**
- **Work Environment:** {c['work_modes']}
- **Indicative Earnings:** {c['salary_indicative']}
*(Provenance: Figures based on official benchmarks from {c['official_source']}).*

**Next Actionable Step:**
Review the required courses and entrance exams on MPath, evaluate sample syllabi, and reflect on whether daily tasks in this field align with your personal curiosity and stamina."""

    # General career counselling response
    return f"""### MPath Career Guidance

**Possibilities Exploration for:** *"{user_query}"*

> **MPath Principle:** *AI student ka future decide nahi karega. AI student ko apne future ki possibilities discover karne mein help karega.*

To explore realistic options for your inquiry:
1. **Discover by Stream & Subjects:** Check our **"Help Me Discover Careers"** tool which maps your academic stream (PCM, PCB, Commerce, Humanities) to 126+ authentic careers.
2. **Reverse Degree Discovery:** If you are already pursuing a specific degree (e.g. B.Tech, MBBS, B.Com, LLB), visit our **Explore by Course** module to view direct and lateral career opportunities.
3. **Skill Alignment:** Success in any chosen field depends on combining domain knowledge with complementary digital and communication skills.

Feel free to specify a career title (e.g., *Data Scientist, Civil Judge, Commercial Pilot, Investment Banker, Clinical Psychologist*) to view exact multi-route roadmaps, required degrees, entrance exams, and verified industry benchmarks!"""
