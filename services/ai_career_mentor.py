import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

from services.ai_client import client

SYSTEM_PROMPT = """You are MPath Career Counselling's AI Career Mentor.
Your mission is to help Indian students discover possibilities, explore career opportunities, understand required skills, colleges, exams, and build roadmaps.
Core ethical principle: AI does NOT decide a student's future; it informs, empowers, and guides them. The final decision always rests with the student.
Provide structured, student-friendly, actionable advice with realistic Indian context."""


def generate_fallback_guidance(question):
    """
    Intelligent rule-informed fallback guidance when external AI API is unavailable.
    """
    q_lower = question.lower()
    
    # Topic detection
    is_tech = any(k in q_lower for k in ["tech", "software", "data", "ai", "python", "developer", "coding", "computer"])
    is_govt = any(k in q_lower for k in ["upsc", "ssc", "civil", "ias", "ips", "government", "exam", "railway", "defence"])
    is_med = any(k in q_lower for k in ["doctor", "mbbs", "medical", "neet", "pharmacy", "biology", "health"])
    is_comm = any(k in q_lower for k in ["ca", "chartered", "commerce", "accounting", "mba", "finance", "business"])
    
    if is_tech:
        domain = "Technology & Computer Science"
        paths = "Software Engineering, Data Science, AI & Machine Learning, Cloud Architecture, or Cybersecurity."
        skills = "Core programming (Python/Java), Data Structures & Algorithms, SQL/Databases, Git version control, and web frameworks."
        edu = "Class 12 with PCM -> B.Tech / BCA / B.Sc Computer Science -> Certifications and portfolio projects."
        exams = "JEE Main, JEE Advanced, BITSAT, State Engineering CETs, GATE (for Masters)."
    elif is_govt:
        domain = "Government Services & Public Administration"
        paths = "UPSC Civil Services (IAS/IPS/IFS), SSC CGL, State Public Service Commissions (PSC), Banking (IBPS/SBI PO), or Defence (NDA/CDS)."
        skills = "General Awareness, Analytical reasoning, Quantitative aptitude, Indian Polity, Economics, and clear written communication."
        edu = "Class 12 in any stream -> Recognized Graduation degree in any discipline -> Targeted exam preparation."
        exams = "UPSC CSE, SSC CGL, IBPS PO, State PSCs, CDS, CAPF."
    elif is_med:
        domain = "Healthcare & Medical Sciences"
        paths = "Medicine (MBBS), Dentistry (BDS), Pharmacy (B.Pharm), Nursing, or Biotechnology."
        skills = "Deep biological science understanding, clinical patience, continuous learning, and diagnostic empathy."
        edu = "Class 12 with PCB (Physics, Chemistry, Biology) -> NEET-UG qualification -> 5.5-year MBBS including internship."
        exams = "NEET-UG, NEET-PG, AIIMS research fellowships."
    elif is_comm:
        domain = "Finance, Commerce & Business Management"
        paths = "Chartered Accountancy (CA), Investment Banking, Financial Analyst, Digital Marketing, or Corporate Management (MBA)."
        skills = "Financial accounting, Corporate taxation, Advanced Excel, Financial modeling, Strategic decision-making."
        edu = "Class 12 (Commerce/Maths preferred) -> CA Foundation / B.Com / BBA -> CA Final or CAT/GMAT for top IIMs."
        exams = "CA Foundation/Inter/Final, CAT, XAT, CMA exams."
    else:
        domain = "Interdisciplinary Career Exploration"
        paths = "Emerging roles combining domain knowledge with digital skills, design, management, or research."
        skills = "Critical thinking, problem solving, digital literacy, communication, and project execution."
        edu = "Class 12 -> Recognized undergraduate degree -> Specialization courses and skill-building projects."
        exams = "CUET for central universities, national entrance tests."

    return f"""### MPath Career Mentor Guidance

**1. Career Domain & Overview**
Your inquiry focuses on **{domain}**. Promising career tracks include {paths}

**2. Suitability & Alignment**
This path suits students who enjoy logical problem-solving, structured learning, and continuous skill refinement. 
*(Note: As an ethical guidance platform, MPath highlights possibilities to explore; your passions and personal goals guide your final choice).*

**3. Core Skills to Develop**
- **Technical Skills**: {skills}
- **Soft Skills**: Communication, teamwork, problem decomposition, and adaptability.

**4. Education & Academic Path**
{edu}

**5. Competitive & Entrance Examinations**
{exams}

**6. Step-by-Step Learning Roadmap**
- **Phase 1 (Foundation)**: Master the fundamentals of your chosen subjects and build consistent study habits.
- **Phase 2 (Skill Building)**: Practice practical skills via mini-projects, problem sets, and verified online certifications.
- **Phase 3 (Experience & Applications)**: Pursue verified internships (e.g., through AICTE internship portal) and participate in student competitions.
- **Phase 4 (Career Launch)**: Build a professional profile, prepare for target campus drives or competitive examinations.

**7. Next Steps on MPath**
Use the **Career Explorer** and **College Explorer** tabs on MPath to inspect detailed curriculums, compare options, and explore verified opportunities."""


def get_ai_guidance(question, user_id=None):
    try:
        from services.ai.reasoning_engine import CareerReasoningEngine
        result = CareerReasoningEngine.generate_response(
            user_message=question,
            user_id=user_id
        )
        return result.get("answer") or generate_fallback_guidance(question)
    except Exception as e:
        print("CareerReasoningEngine call fallback:", e)
        return generate_fallback_guidance(question)

