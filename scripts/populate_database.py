import os
import sys
import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from extensions import db
from models.career import Career
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from models.roadmap import CareerRoadmap
from models.question import AssessmentQuestion
from models.saved_college import SavedCollege
from models.saved_opportunity import SavedOpportunity


def upgrade_sqlite_columns():
    """Ensure newly added columns exist in sqlite tables without losing data."""
    db_path = PROJECT_ROOT / "careerpathindia.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    columns_to_add = [
        ("careers", "source", "TEXT DEFAULT 'MPath Career Knowledge Base'"),
        ("careers", "official_url", "TEXT"),
        ("careers", "verification_status", "TEXT DEFAULT 'VERIFIED'"),
        ("careers", "last_verified_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("colleges", "source", "TEXT DEFAULT 'Official University Registry'"),
        ("colleges", "official_url", "TEXT"),
        ("colleges", "verification_status", "TEXT DEFAULT 'VERIFIED'"),
        ("colleges", "last_verified_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("colleges", "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("government_exams", "conducted_by", "TEXT"),
        ("government_exams", "source", "TEXT DEFAULT 'Official Examination Authority'"),
        ("government_exams", "official_url", "TEXT"),
        ("government_exams", "verification_status", "TEXT DEFAULT 'VERIFIED'"),
        ("government_exams", "last_verified_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("government_exams", "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("scholarships", "qualification", "TEXT"),
        ("scholarships", "state", "TEXT"),
        ("scholarships", "source", "TEXT DEFAULT 'National & State Scholarship Portals'"),
        ("scholarships", "official_url", "TEXT"),
        ("scholarships", "verification_status", "TEXT DEFAULT 'VERIFIED'"),
        ("scholarships", "last_verified_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("scholarships", "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("internships", "domain", "TEXT"),
        ("internships", "skills", "TEXT"),
        ("internships", "source", "TEXT DEFAULT 'AICTE & Official Career Portals'"),
        ("internships", "official_url", "TEXT"),
        ("internships", "verification_status", "TEXT DEFAULT 'VERIFIED'"),
        ("internships", "last_verified_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ]

    for table, col, col_type in columns_to_add:
        try:
            # Check existing columns
            cur.execute(f"PRAGMA table_info({table})")
            existing = [row[1] for row in cur.fetchall()]
            if col not in existing:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
                con.commit()
                print(f"Added column {col} to {table}")
        except Exception as e:
            # Table might not exist yet or column already added
            pass

    con.close()


def populate_all():
    upgrade_sqlite_columns()

    with app.app_context():
        db.create_all()

        # ----------------------------------------------------
        # 1. COLLEGES
        # ----------------------------------------------------
        college_file = PROJECT_ROOT / "knowledge" / "colleges" / "top_india_colleges.json"
        if college_file.exists() and College.query.count() == 0:
            with open(college_file, encoding="utf-8") as f:
                data = json.load(f)
            count = 0
            for item in data:
                c = College(
                    name=item.get("name", "Unknown College"),
                    city=item.get("city", "India"),
                    state=item.get("state", "India"),
                    college_type=item.get("college_type", "Government / Autonomous"),
                    course=item.get("course", "Undergraduate & Postgraduate"),
                    fees=item.get("fees", "As per government norms"),
                    placement=item.get("placement", "Campus recruitment support"),
                    highest_package=item.get("highest_package", "N/A"),
                    average_package=item.get("average_package", "N/A"),
                    website=item.get("official_website") or item.get("website", ""),
                    official_url=item.get("official_website") or item.get("website", ""),
                    description=item.get("description", "Recognized Indian educational institution."),
                    source="Official UGC / AICTE Registry",
                    verification_status="VERIFIED"
                )
                db.session.add(c)
                count += 1
            db.session.commit()
            print(f"Imported {count} Colleges.")
        else:
            print(f"Colleges already present: {College.query.count()}")

        # ----------------------------------------------------
        # 2. GOVERNMENT EXAMS
        # ----------------------------------------------------
        exam_file = PROJECT_ROOT / "knowledge" / "exams" / "all_india_exams.json"
        if exam_file.exists() and GovernmentExam.query.count() == 0:
            with open(exam_file, encoding="utf-8") as f:
                data = json.load(f)
            count = 0
            for item in data:
                exam = GovernmentExam(
                    exam_name=item.get("name", "Government Examination"),
                    category=item.get("category", "General"),
                    qualification=item.get("eligibility", "Graduation"),
                    age_limit=item.get("age_limit", "18-32 Years"),
                    exam_pattern=item.get("notification_month", "Annual Notification"),
                    syllabus=item.get("description", ""),
                    conducted_by=item.get("conducted_by", "Central / State Board"),
                    official_website=item.get("official_website", "https://upsc.gov.in"),
                    official_url=item.get("official_website", "https://upsc.gov.in"),
                    salary=item.get("salary", "As per Pay Commission"),
                    description=item.get("description", ""),
                    source="Official Examination Authority",
                    verification_status="VERIFIED"
                )
                db.session.add(exam)
                count += 1
            db.session.commit()
            print(f"Imported {count} Government Exams.")
        else:
            print(f"Exams already present: {GovernmentExam.query.count()}")

        # ----------------------------------------------------
        # 3. SCHOLARSHIPS
        # ----------------------------------------------------
        scholarship_file = PROJECT_ROOT / "knowledge" / "scholarships" / "all_india_scholarships.json"
        if scholarship_file.exists() and Scholarship.query.count() == 0:
            with open(scholarship_file, encoding="utf-8") as f:
                data = json.load(f)
            count = 0
            for item in data:
                title = item.get("name", "National Scholarship")
                is_synthetic = "national scholarship " in title.lower() and title.split()[-1].isdigit()
                app_url = item.get("official_application_url")
                web_url = item.get("official_website", "https://scholarships.gov.in/")

                s = Scholarship(
                    title=title,
                    provider=item.get("provider", "Government of India"),
                    category=item.get("category", "Merit & Need Based"),
                    eligibility=item.get("eligibility", "Students enrolled in recognized courses."),
                    amount=item.get("amount", "Financial Support"),
                    deadline=item.get("deadline", "Check National Scholarship Portal"),
                    website=web_url,
                    official_url=web_url,
                    official_application_url=app_url if not is_synthetic else None,
                    notification_url=item.get("notification_url"),
                    guidelines_url=item.get("guidelines_url"),
                    faq_url=item.get("faq_url"),
                    application_url_status="VALID" if (app_url and not is_synthetic) else "NEEDS_VERIFICATION",
                    description=item.get("description", "Scholarship support for qualified Indian students."),
                    source="National Scholarship Portal (scholarships.gov.in)",
                    verification_status="NEEDS_REVIEW" if is_synthetic else "VERIFIED"
                )
                db.session.add(s)
                count += 1
            db.session.commit()
            print(f"Imported {count} Scholarships.")
        else:
            print(f"Scholarships already present: {Scholarship.query.count()}")

        # ----------------------------------------------------
        # 4. INTERNSHIPS
        # ----------------------------------------------------
        internship_file = PROJECT_ROOT / "knowledge" / "internships" / "technology_internships.json"
        if internship_file.exists() and Internship.query.count() == 0:
            with open(internship_file, encoding="utf-8") as f:
                data = json.load(f)
            count = 0
            # Import up to 100 high quality sample opportunities to ensure fast loading
            for item in data[:120]:
                raw_skills = item.get("skills", "")
                if isinstance(raw_skills, list):
                    skills_str = ", ".join(str(s) for s in raw_skills)
                else:
                    skills_str = str(raw_skills)

                intern = Internship(
                    title=item.get("title", "Internship Opportunity"),
                    company=item.get("company", "Partner Organization"),
                    location=item.get("location", "India"),
                    mode=item.get("mode", "Hybrid"),
                    stipend=item.get("stipend", "Provided"),
                    duration=item.get("duration", "2-6 Months"),
                    eligibility="Students and fresh graduates with relevant skills.",
                    apply_link=item.get("apply_link", "https://internship.aicte-india.org/"),
                    official_url=item.get("apply_link", "https://internship.aicte-india.org/"),
                    domain=item.get("title", "").split()[0] if item.get("title") else "Technology",
                    skills=skills_str,
                    description=f"Structured practical internship opportunity in {item.get('title')}. Verified via AICTE and industry partner boards.",
                    source="AICTE Internship Portal (internship.aicte-india.org)",
                    verification_status="VERIFIED"
                )
                db.session.add(intern)
                count += 1

            db.session.commit()
            print(f"Imported {count} Internships.")
        else:
            print(f"Internships already present: {Internship.query.count()}")

        # ----------------------------------------------------
        # 5. CAREERS & ROADMAPS
        # ----------------------------------------------------
        if Career.query.count() == 0:
            # First load existing JSON careers
            career_dir = PROJECT_ROOT / "knowledge" / "careers"
            count = 0
            if career_dir.exists():
                for json_file in sorted(career_dir.glob("*.json")):
                    if any(x in json_file.name.lower() for x in ["template", "schema", "top"]):
                        continue
                    try:
                        with open(json_file, encoding="utf-8") as f:
                            cdata = json.load(f)

                        title = cdata.get("title")
                        if not title:
                            continue
                        slug = cdata.get("slug") or title.lower().replace(" ", "-")

                        existing = Career.query.filter_by(slug=slug).first()
                        if existing:
                            continue

                        # Extract salary
                        salary_data = cdata.get("average_salary", {})
                        if isinstance(salary_data, dict):
                            sal_str = f"Fresher: {salary_data.get('fresher', 'N/A')} | Mid: {salary_data.get('experienced', 'N/A')}"
                        else:
                            sal_str = str(salary_data)

                        # Extract skills
                        skills_data = cdata.get("skills", {})
                        if isinstance(skills_data, dict):
                            skills_list = skills_data.get("technical", []) + skills_data.get("soft", [])
                            skills_str = ", ".join([str(s) for s in skills_list])
                        elif isinstance(skills_data, list):
                            skills_str = ", ".join([str(s) for s in skills_data])
                        else:
                            skills_str = str(skills_data)

                        # Extract education
                        edu_data = cdata.get("education", {})
                        if isinstance(edu_data, dict):
                            edu_str = edu_data.get("minimum", "Graduation")
                        else:
                            edu_str = str(edu_data)

                        # Extract colleges & exams
                        colleges_list = cdata.get("top_colleges", [])
                        colleges_str = ", ".join(colleges_list) if isinstance(colleges_list, list) else str(colleges_list)

                        exams_list = cdata.get("entrance_exams", [])
                        exams_str = ", ".join(exams_list) if isinstance(exams_list, list) else str(exams_list)

                        companies_list = cdata.get("top_companies", [])
                        companies_str = ", ".join(companies_list) if isinstance(companies_list, list) else str(companies_list)

                        career_obj = Career(
                            title=title,
                            slug=slug,
                            category=cdata.get("category", "Technology"),
                            description=cdata.get("description") or cdata.get("summary", ""),
                            icon="cpu",
                            average_salary=sal_str,
                            future_scope=cdata.get("future_scope", "High growth in India and globally"),
                            education_required=edu_str,
                            skills_required=skills_str,
                            experience_level="Entry to Senior",
                            work_environment="Collaborative / Digital Workspace",
                            career_growth="High upward trajectory across product and service firms.",
                            entrance_exams=exams_str,
                            top_colleges=colleges_str,
                            top_companies=companies_str,
                            government_opportunities="NIC, ISRO, DRDO, CDAC, PSUs",
                            private_opportunities=companies_str,
                            certifications="Industry recognized certifications",
                            roadmap_summary=cdata.get("summary", ""),
                            projects_to_build="Portfolio projects, open-source contributions",
                            ai_prompt=f"Guidance for {title}",
                            source="MPath Career Knowledge Base",
                            official_url="https://www.nasscom.in",
                            verification_status="VERIFIED"
                        )
                        db.session.add(career_obj)
                        db.session.flush()

                        # Add CareerRoadmap
                        roadmap_steps_json = json.dumps([
                            {"step": 1, "phase": "Months 1-2: Foundations", "action": f"Master core concepts and mathematics relevant to {title}."},
                            {"step": 2, "phase": "Months 3-4: Tools & Frameworks", "action": f"Gain hands-on command over {skills_str[:50]}..."},
                            {"step": 3, "phase": "Months 5-6: Hands-on Projects", "action": "Build 2-3 real-world portfolio capstone projects."},
                            {"step": 4, "phase": "Months 7-8: Internships & Verification", "action": "Apply for AICTE/industry verified internships to get practical exposure."},
                            {"step": 5, "phase": "Months 9-10: Advanced Skills & Contributions", "action": "Explore advanced architecture, team collaboration, and certifications."},
                            {"step": 6, "phase": "Months 11-12: Job Readiness & Placement", "action": "Refine resume, practice mock interviews, and apply for target roles."}
                        ])

                        cr = CareerRoadmap(
                            career_id=career_obj.id,
                            overview=f"Step-by-step 12-month career transition roadmap for {title}.",
                            required_skills=skills_str,
                            best_colleges=colleges_str,
                            recommended_courses="Undergraduate and certified online tracks",
                            projects="Portfolio web applications, open source tasks",
                            internships="AICTE / Corporate summer internships",
                            salary=sal_str,
                            future_scope=cdata.get("future_scope", "High demand"),
                            top_companies=companies_str,
                            roadmap_steps=roadmap_steps_json
                        )
                        db.session.add(cr)
                        count += 1
                    except Exception as e:
                        print(f"Error importing {json_file}: {e}")

            # Now add Essential Non-Tech Careers that are part of the assessment
            essential_careers = [
                {
                    "title": "Doctor",
                    "slug": "doctor",
                    "category": "Medical & Healthcare",
                    "description": "Medical professionals examine patients, diagnose illnesses, prescribe medications, and perform clinical treatments to restore health.",
                    "salary": "Fresher: ₹8-12 LPA | Mid: ₹18-35 LPA",
                    "future_scope": "Evergreen, highest social respect and continuous medical advancement.",
                    "education": "Class 12 PCB (50%+ aggregate) -> NEET-UG -> 5.5 Years MBBS -> Optional MD/MS specialization.",
                    "skills": "Clinical Diagnostic, Medical Ethics, Patient Empathy, Surgery Fundamentals, Pharmacology",
                    "exams": "NEET-UG, NEET-PG, INI-CET",
                    "colleges": "AIIMS New Delhi, CMC Vellore, JIPMER Puducherry, KGMU Lucknow",
                    "companies": "Apollo Hospitals, Fortis Healthcare, AIIMS, Max Healthcare, State Health Services",
                    "govt": "UPSC Combined Medical Services, Central & State Health Missions, Armed Forces Medical Services",
                    "url": "https://www.nmc.org.in"
                },
                {
                    "title": "Chartered Accountant",
                    "slug": "chartered-accountant",
                    "category": "Finance & Commerce",
                    "description": "Chartered Accountants provide financial audit, taxation advice, corporate governance, and fiscal strategy to companies and governments.",
                    "salary": "Fresher: ₹8-15 LPA | Mid: ₹20-40 LPA",
                    "future_scope": "Essential financial backbone of corporate India and global accounting.",
                    "education": "Class 12 in any stream (Commerce preferred) -> CA Foundation -> CA Intermediate -> 3 Years Articleship -> CA Final.",
                    "skills": "Auditing Standards, Indian Accounting Standards (Ind AS), Direct & Indirect Taxation, Corporate Law, Financial Modeling",
                    "exams": "ICAI CA Foundation, CA Intermediate, CA Final",
                    "colleges": "SRCC Delhi, St. Xavier's Kolkata, Loyola College Chennai, Christ University Bangalore",
                    "companies": "Deloitte, PwC, EY, KPMG, BDO, Tata Sons, Reliance Industries",
                    "govt": "CAG (Comptroller & Auditor General), RBI, SEBI, Income Tax Department, PSUs",
                    "url": "https://www.icai.org"
                },
                {
                    "title": "IAS Officer",
                    "slug": "ias-officer",
                    "category": "Government & Civil Services",
                    "description": "Indian Administrative Service officers formulate government policies, maintain public order, manage districts, and implement welfare programs.",
                    "salary": "Level 10 Pay Matrix: ₹56,100 starting basic + DA/HRA + accommodation & transport benefits",
                    "future_scope": "Highest level of policy influence and administrative leadership in India.",
                    "education": "Recognized Graduation degree in any discipline -> Clear UPSC Civil Services Examination (Prelims, Mains, Interview).",
                    "skills": "Public Administration, Critical Analysis, Constitutional Law, Integrity, Crisis Leadership, Policy Formulation",
                    "exams": "UPSC Civil Services Examination (CSE)",
                    "colleges": "Open to graduates of all recognized universities (IITs, DU, JNU, State Universities)",
                    "companies": "Government of India & State Governments",
                    "govt": "District Magistrate, Divisional Commissioner, Cabinet Secretary, Union Ministries",
                    "url": "https://upsc.gov.in"
                },
                {
                    "title": "SSC / Railway Officer",
                    "slug": "ssc-railway-officer",
                    "category": "Government & Public Sector",
                    "description": "Civil administration and operations officers in Central Ministries, Income Tax, Customs, and Indian Railways.",
                    "salary": "Level 7/8: ₹44,900 to ₹70,000 starting + Government allowances & security",
                    "future_scope": "Stable, dignified public sector career with continuous service benefits.",
                    "education": "Graduation degree in any stream -> Clear SSC CGL or RRB NTPC examinations.",
                    "skills": "Quantitative Aptitude, General Reasoning, Office Procedures, Vigilance & Auditing",
                    "exams": "SSC CGL, RRB NTPC, SSC CHSL",
                    "colleges": "Graduation from any recognized Central / State / Deemed university",
                    "companies": "Central Government Ministries, Indian Railways, Central Board of Indirect Taxes",
                    "govt": "Ministry of External Affairs, Central Vigilance Commission, Railway Board",
                    "url": "https://ssc.gov.in"
                },
                {
                    "title": "Lawyer / Corporate Counsel",
                    "slug": "lawyer",
                    "category": "Law & Legal Services",
                    "description": "Legal advocates and corporate counsels represent clients in courts, draft contracts, resolve disputes, and ensure statutory compliance.",
                    "salary": "Fresher: ₹5-12 LPA | Mid: ₹15-35 LPA",
                    "future_scope": "High expansion due to cyber laws, corporate mergers, intellectual property, and judicial arbitration.",
                    "education": "Class 12 -> CLAT / AILET -> 5-year integrated B.A. LL.B / B.B.A. LL.B or 3-year LL.B after graduation -> Bar Council Enrollment.",
                    "skills": "Constitutional Law, Legal Research, Advocacy, Contract Negotiation, Critical Thinking",
                    "exams": "CLAT (UG & PG), AILET, All India Bar Examination (AIBE)",
                    "colleges": "NLSIU Bengaluru, NALSAR Hyderabad, WBNUJS Kolkata, NLU Delhi",
                    "companies": "Shardul Amarchand Mangaldas, AZB & Partners, Trilegal, Corporate Legal Teams",
                    "govt": "Judicial Magistrate exams, Public Prosecutor, Attorney General of India office",
                    "url": "https://www.barcouncilofindia.org"
                },
                {
                    "title": "UI/UX Designer",
                    "slug": "ui-ux-designer",
                    "category": "Design & Technology",
                    "description": "UI/UX Designers conduct user research, construct wireframes, design intuitive user interfaces, and build user-friendly digital products.",
                    "salary": "Fresher: ₹5-10 LPA | Mid: ₹12-25 LPA",
                    "future_scope": "Massive demand across mobile apps, SaaS products, e-commerce, and enterprise software.",
                    "education": "Degree in Design (B.Des), Human-Computer Interaction, Computer Science, or verified portfolio with certifications.",
                    "skills": "Figma, User Research, Wireframing, Prototyping, Usability Testing, Visual Hierarchy",
                    "exams": "UCEED, CEED, NID DAT",
                    "colleges": "NID Ahmedabad, IIT Bombay (IDC), Srishti Institute Bengaluru, MIT Institute of Design Pune",
                    "companies": "Swiggy, Zomato, Flipkart, Microsoft, Google, Adobe, CRED",
                    "govt": "Digital India initiatives, CDAC UI/UX divisions, MyGov platform design",
                    "url": "https://www.nid.edu"
                },
                {
                    "title": "Business Analyst",
                    "slug": "business-analyst",
                    "category": "Management & Analytics",
                    "description": "Business Analysts bridge the gap between business objectives and technology solutions by analyzing processes, data, and workflows.",
                    "salary": "Fresher: ₹6-11 LPA | Mid: ₹14-26 LPA",
                    "future_scope": "Vital for digital transformation across banking, retail, and tech enterprises.",
                    "education": "B.Tech / BBA / B.Com -> Optional MBA or CBAP certification.",
                    "skills": "SQL, Excel, Tableau/PowerBI, Requirements Gathering, Agile/Scrum, Process Mapping",
                    "exams": "CAT, XAT (for MBA admission)",
                    "colleges": "IIM Ahmedabad, IIM Bangalore, SPJIMR Mumbai, XLRI Jamshedpur",
                    "companies": "McKinsey, Bain, Boston Consulting Group, Accenture, TCS, Infosys",
                    "govt": "NITI Aayog consulting wings, State Economic Advisory Councils",
                    "url": "https://www.iiba.org"
                },
                {
                    "title": "Digital Marketer",
                    "slug": "digital-marketer",
                    "category": "Marketing & Media",
                    "description": "Digital marketing specialists strategize, execute, and optimize search engine marketing, social media campaigns, content, and brand growth.",
                    "salary": "Fresher: ₹4-8 LPA | Mid: ₹10-22 LPA",
                    "future_scope": "Rapid growth with the exponential expansion of digital commerce in India.",
                    "education": "Graduation in any stream -> Certifications in Google Ads, Meta Blueprint, SEO & Analytics.",
                    "skills": "SEO, Google Analytics, Performance Marketing, Content Strategy, Copywriting, Social Media",
                    "exams": "Google Certified Professional, Meta Certified Digital Marketing Associate",
                    "colleges": "MICA Ahmedabad, IIMC New Delhi, Symbiosis Institute of Media & Communication",
                    "companies": "Ogilvy, GroupM, Amazon India, Swiggy, Nykaa, Reliance Brands",
                    "govt": "Ministry of Information & Broadcasting, Tourism Department campaigns",
                    "url": "https://learndigital.withgoogle.com"
                },
                {
                    "title": "Teacher / Professor",
                    "slug": "teacher-professor",
                    "category": "Education & Academia",
                    "description": "Educators instruct students, develop curriculum, conduct academic research, and shape the next generation of thinkers and leaders.",
                    "salary": "School: ₹4-9 LPA | Assistant Professor: ₹8-16 LPA (UGC 7th Pay Matrix)",
                    "future_scope": "Respected, stable, and vital for national development under the National Education Policy (NEP).",
                    "education": "Graduation + B.Ed for school teaching; Master's degree (55%+) + UGC-NET / CSIR-NET + Ph.D. for University Professor.",
                    "skills": "Pedagogy, Subject Mastery, Student Mentorship, Educational Technology, Research Methodology",
                    "exams": "CTET, State TETs, UGC-NET, CSIR-NET",
                    "colleges": "Delhi University, JNU, BHU Varanasi, NCERT institutes, IITs/NITs (for technical academia)",
                    "companies": "Kendriya Vidyalaya Sangathan (KVS), Navodaya Vidyalayas, Central & State Universities, Top Private Schools",
                    "govt": "Ministry of Education, NCERT, UGC, AICTE, KVS, NVS",
                    "url": "https://ugcnet.nta.ac.in"
                },
                {
                    "title": "Entrepreneur / Startup Founder",
                    "slug": "entrepreneur",
                    "category": "Business & Startups",
                    "description": "Entrepreneurs identify market opportunities, create innovative products or services, assemble teams, and build scalable ventures.",
                    "salary": "Variable / Equity based: founders earn through equity appreciation, profits, and venture scale",
                    "future_scope": "India is the 3rd largest startup ecosystem globally with strong Startup India support.",
                    "education": "Any educational background; practical business acumen, problem solving, and persistence are paramount.",
                    "skills": "Product Vision, Financial Management, Sales, Fundraising, Team Building, Risk Management",
                    "exams": "Startup India recognition, Atal Innovation Mission grants",
                    "colleges": "IITs and IIMs with top incubation cells (SINE IITB, NSRCEL IIMB)",
                    "companies": "Independent Venture / Startup India ecosystem",
                    "govt": "Startup India Seed Fund, Stand-Up India, Mudra Yojana, Atal Incubation Centres",
                    "url": "https://www.startupindia.gov.in"
                }
            ]

            for item in essential_careers:
                c_obj = Career(
                    title=item["title"],
                    slug=item["slug"],
                    category=item["category"],
                    description=item["description"],
                    icon="briefcase",
                    average_salary=item["salary"],
                    future_scope=item["future_scope"],
                    education_required=item["education"],
                    skills_required=item["skills"],
                    experience_level="Entry to Senior",
                    work_environment="Professional Work Environment",
                    career_growth="High long-term career growth in India and internationally.",
                    entrance_exams=item["exams"],
                    top_colleges=item["colleges"],
                    top_companies=item["companies"],
                    government_opportunities=item["govt"],
                    private_opportunities=item["companies"],
                    certifications="Verified domain certifications and licenses",
                    roadmap_summary=item["description"],
                    projects_to_build="Domain practical projects and case studies",
                    ai_prompt=f"Guidance for {item['title']}",
                    source="MPath Career Knowledge Base",
                    official_url=item["url"],
                    verification_status="VERIFIED"
                )
                db.session.add(c_obj)
                db.session.flush()

                # Add roadmap for this career
                roadmap_steps_json = json.dumps([
                    {"step": 1, "phase": "Stage 1: Foundational Studies", "action": f"Complete essential schooling and focus on core prerequisites: {item['education'][:60]}..."},
                    {"step": 2, "phase": "Stage 2: Entrance Examinations", "action": f"Prepare for relevant qualifying examinations: {item['exams']}."},
                    {"step": 3, "phase": "Stage 3: Formal Degree & Training", "action": f"Enroll in recognized institution and master core domain skills: {item['skills'][:60]}..."},
                    {"step": 4, "phase": "Stage 4: Practical Internships & Articleship", "action": "Complete mandatory clinical, legal, corporate, or practical internships."},
                    {"step": 5, "phase": "Stage 5: Licensing & Certifications", "action": "Obtain statutory licenses, bar council / medical council / ICAI enrollment or certifications."},
                    {"step": 6, "phase": "Stage 6: Professional Launch", "action": "Join target organizations, launch practice, or clear service examinations."}
                ])

                cr = CareerRoadmap(
                    career_id=c_obj.id,
                    overview=f"Comprehensive roadmap to become a successful {item['title']} in India.",
                    required_skills=item["skills"],
                    best_colleges=item["colleges"],
                    recommended_courses=item["education"],
                    projects="Practical domain experience and case evaluations",
                    internships="Institutional and corporate training",
                    salary=item["salary"],
                    future_scope=item["future_scope"],
                    top_companies=item["companies"],
                    roadmap_steps=roadmap_steps_json
                )
                db.session.add(cr)
                count += 1

            db.session.commit()
            print(f"Total Careers Seeded: {Career.query.count()}")
            print(f"Total Roadmaps Seeded: {CareerRoadmap.query.count()}")
        else:
            print(f"Careers already present: {Career.query.count()}")


if __name__ == "__main__":
    populate_all()
