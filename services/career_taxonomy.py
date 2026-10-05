"""
services/career_taxonomy.py
==============================================================================
Taxonomy, Sector Definitions, Career Fit Algorithm & Grounded Counselling Engine
==============================================================================
"""

import re
import json

SECTORS_METADATA = {
    "Technology & Computer Science": {
        "slug": "technology-computer-science",
        "icon": "laptop",
        "color": "primary",
        "tagline": "Software, AI, Data Science, Cybersecurity, Cloud & Digital Architecture",
        "description": "Drive technological innovation by engineering scalable software, intelligent neural algorithms, cloud architectures, and digital systems that power modern society.",
        "common_degrees": ["B.Tech Computer Science", "BCA", "B.Sc Data Science", "MCA", "M.Tech CSE"],
        "common_exams": ["JEE Main", "JEE Advanced", "GATE (CS)", "NIMCET"],
        "key_skills": ["Python", "DSA", "System Design", "SQL", "Cloud Computing", "Machine Learning"],
        "typical_streams": ["Science (PCM)", "Computer Science"]
    },
    "Healthcare & Medical Sciences": {
        "slug": "healthcare-medical-sciences",
        "icon": "heart-pulse",
        "color": "danger",
        "tagline": "Clinical Medicine, Diagnostics, Public Health, Pharmacy & Allied Sciences",
        "description": "Dedicate yourself to healing human lives, pioneering medical research, advancing pharmaceutical remedies, and expanding public health wellness.",
        "common_degrees": ["MBBS", "BDS", "B.Pharm", "B.Sc Nursing", "BPT", "MD / MS"],
        "common_exams": ["NEET-UG", "NEET-PG", "INI-CET", "GPAT"],
        "key_skills": ["Patient Diagnosis", "Clinical Pathology", "Pharmacology", "Emergency Triage", "Empathy"],
        "typical_streams": ["Science (PCB)"]
    },
    "Finance, Banking & Accounting": {
        "slug": "finance-banking-accounting",
        "icon": "cash-coin",
        "color": "success",
        "tagline": "Corporate Finance, Investment Banking, Chartered Accountancy & Risk Advisory",
        "description": "Navigate financial capital markets, structure mergers, audit multinational balance sheets, formulate tax strategies, and optimize institutional investment portfolios.",
        "common_degrees": ["B.Com", "BBA Finance", "Chartered Accountancy", "MBA Finance", "B.Sc Statistics"],
        "common_exams": ["CA Foundation/Inter/Final", "CAT", "CFA", "CS Executive", "FRM"],
        "key_skills": ["Financial Modeling", "Corporate Taxation", "Audit Standards", "M&A Valuation", "Risk Analysis"],
        "typical_streams": ["Commerce with Maths", "Economics", "Science (PCM)"]
    },
    "Engineering & Manufacturing": {
        "slug": "engineering-manufacturing",
        "icon": "gear-wide-connected",
        "color": "warning",
        "tagline": "Mechanical, Civil, Electrical, Chemical, Robotics & Infrastructure",
        "description": "Transform physical reality by designing mega infrastructure, high-efficiency automotive powertrains, semiconductor electronics, green chemical plants, and robotic factories.",
        "common_degrees": ["B.Tech Mechanical", "B.Tech Civil", "B.Tech Electrical", "B.Tech Chemical"],
        "common_exams": ["JEE Main", "JEE Advanced", "GATE (Engineering)", "State CETs"],
        "key_skills": ["AutoCAD / SolidWorks", "Thermodynamics", "Structural Analysis", "PLC/SCADA", "Process Safety"],
        "typical_streams": ["Science (PCM)"]
    },
    "Law & Legal Services": {
        "slug": "law-legal-services",
        "icon": "bank",
        "color": "secondary",
        "tagline": "Judiciary, Corporate Advisory, Criminal Defense, Cyber Law & IP Rights",
        "description": "Uphold constitutional justice, represent individuals and multinational corporations before High Courts, arbitrate cross-border commercial disputes, and draft statutory compliance.",
        "common_degrees": ["BA LLB (5 Years)", "BBA LLB", "LLB (3 Years)", "LLM"],
        "common_exams": ["CLAT (UG/PG)", "AILET", "Judicial Service Examinations (PCS-J)", "AIBE"],
        "key_skills": ["Legal Research", "Oral Advocacy", "Contract Drafting", "Constitutional Law", "Due Diligence"],
        "typical_streams": ["Humanities / Arts", "Commerce", "Any Stream"]
    },
    "Government, Defence & Civil Services": {
        "slug": "government-defence-civil-services",
        "icon": "shield-check",
        "color": "primary",
        "tagline": "UPSC Civil Services, Armed Forces, Central Police, PSUs & State Commissions",
        "description": "Lead public administration, safeguard national sovereign borders, formulate national fiscal policy, and direct district administration across the Republic of India.",
        "common_degrees": ["Any Recognized Bachelor's Degree (BA, B.Sc, B.Com, B.Tech)"],
        "common_exams": ["UPSC CSE (IAS/IPS/IFS)", "NDA", "CDS", "SSC CGL", "State PSCs", "CAPF"],
        "key_skills": ["Public Administration", "Constitutional Governance", "Crisis Management", "Leadership"],
        "typical_streams": ["Any Stream (Science, Humanities, Commerce)"]
    },
    "Business, Management & Consulting": {
        "slug": "business-management-consulting",
        "icon": "graph-up-arrow",
        "color": "info",
        "tagline": "Management Consulting, Product Leadership, Operations, HR & Strategy",
        "description": "Drive corporate enterprise growth, optimize international supply networks, formulate market entry strategies, and steer digital product innovation from inception to market leadership.",
        "common_degrees": ["BBA", "B.Com", "B.Tech + MBA", "Master of Business Administration (MBA)"],
        "common_exams": ["CAT", "XAT", "GMAT", "NMAT", "SNAP"],
        "key_skills": ["Strategic Frameworks", "Product Roadmaps", "Data-Driven Decision Making", "Stakeholder Leadership"],
        "typical_streams": ["Commerce", "Science", "Humanities"]
    },
    "Science, Research & Mathematics": {
        "slug": "science-research-mathematics",
        "icon": "atom",
        "color": "dark",
        "tagline": "Pure Mathematics, Physics, Biotechnology, Space Science & Genomics",
        "description": "Expand the frontier of human understanding through fundamental mathematical proofs, quantum computing physics, gene editing biology, and astronomical deep-space research.",
        "common_degrees": ["B.Sc Mathematics / Physics / Chemistry / Biotech", "BS-MS (IISER/IISc)", "M.Sc", "Ph.D."],
        "common_exams": ["CSIR UGC NET", "GATE", "IIT JAM", "TIFR GS", "NEST"],
        "key_skills": ["Scientific Methodology", "Statistical Inference", "Experimental Design", "Python / MATLAB"],
        "typical_streams": ["Science (PCM / PCB)"]
    },
    "Education, Teaching & Academia": {
        "slug": "education-teaching-academia",
        "icon": "mortarboard",
        "color": "success",
        "tagline": "School Pedagogy, University Professorship, EdTech & Academic Research",
        "description": "Shape the minds of coming generations through inspirational classroom teaching, university research mentoring, curriculum innovation, and specialized educational technology.",
        "common_degrees": ["B.Ed", "B.El.Ed", "Master's Degree in Core Subject", "Ph.D."],
        "common_exams": ["CTET (Paper I & II)", "State TET", "UGC NET (Assistant Professor & JRF)"],
        "key_skills": ["Pedagogical Design", "Classroom Engagement", "Curriculum Development", "Student Mentoring"],
        "typical_streams": ["Any Stream"]
    },
    "Media, Journalism & Digital Marketing": {
        "slug": "media-journalism-digital-marketing",
        "icon": "broadcast-pin",
        "color": "danger",
        "tagline": "Investigative Journalism, Digital Marketing, PR, Filmmaking & Content Strategy",
        "description": "Inform, investigate, and captivate audiences across broadcast networks, print publications, documentary cinema, and viral digital performance marketing campaigns.",
        "common_degrees": ["BJMC (Journalism & Mass Comm)", "BA Media Studies", "MA Mass Comm"],
        "common_exams": ["IIMC Entrance Examination", "CUET-UG/PG", "Jamia Millia Mass Comm Entrance"],
        "key_skills": ["Investigative Reporting", "Digital Copywriting", "SEO / Performance Marketing", "Video Editing"],
        "typical_streams": ["Arts / Humanities", "Commerce", "Open to All"]
    },
    "Design, Animation & Creative Arts": {
        "slug": "design-animation-creative-arts",
        "icon": "palette",
        "color": "warning",
        "tagline": "UI/UX Design, Industrial Design, Fashion, 3D Animation & Game Art",
        "description": "Craft intuitive digital experiences, ergonomic physical products, high-fashion textiles, cinematic 3D visual effects, and immersive interactive video games.",
        "common_degrees": ["B.Des (UX / Industrial / Fashion)", "B.F.A.", "M.Des"],
        "common_exams": ["UCEED", "NID DAT (Prelims/Mains)", "NIFT Entrance Exam", "CEED"],
        "key_skills": ["Design Thinking", "Figma / Adobe XD", "Wireframing & Prototyping", "User Research", "Blender / Maya"],
        "typical_streams": ["Open to Any Stream (Creativity & Portfolio Focus)"]
    },
    "Agriculture, Food Technology & Environment": {
        "slug": "agriculture-food-technology-environment",
        "icon": "tree",
        "color": "success",
        "tagline": "Agronomy, Precision Farming, Food Processing, Forestry & Climate Sustainability",
        "description": "Safeguard food security and ecological biodiversity by engineering climate-resilient crops, automated drone agriculture, sustainable food processing, and environmental compliance.",
        "common_degrees": ["B.Sc (Hons) Agriculture", "B.Tech Food Technology", "B.Sc Forestry", "M.Sc Agronomy"],
        "common_exams": ["ICAR AIEEA (UG/PG)", "State Agri CETs", "GATE (Life Sciences / Agri)"],
        "key_skills": ["Crop Science", "Soil Nutrient Analysis", "HACCP Food Safety", "GIS Mapping", "Precision Agri"],
        "typical_streams": ["Science (PCB / PCM)"]
    },
    "Aviation, Logistics & Supply Chain": {
        "slug": "aviation-logistics-supply-chain",
        "icon": "airplane",
        "color": "info",
        "tagline": "Commercial Aviation, Maritime Shipping, Port Operations & Global Logistics",
        "description": "Command commercial airliners, pilot oceangoing cargo ships, coordinate air traffic control radar, and synchronize complex multi-modal global supply chains.",
        "common_degrees": ["CPL Flight Training", "B.Sc Nautical Science", "B.Tech Marine Engg", "BBA Logistics"],
        "common_exams": ["DGCA CPL Exams", "IMU-CET", "Air Traffic Controller (ATC) Exam by AAI"],
        "key_skills": ["Flight Navigation", "Maritime Navigation (COLREGs)", "Supply Chain Optimization", "SAP SCM"],
        "typical_streams": ["Science (PCM) with Physics & Mathematics"]
    },
    "Social Sciences, Psychology & Public Policy": {
        "slug": "social-sciences-psychology-public-policy",
        "icon": "people",
        "color": "primary",
        "tagline": "Clinical Psychology, Public Policy, Urban Planning, Sociology & Development",
        "description": "Understand human behavior, heal psychological trauma, design equitable public policies, and direct non-profit community development initiatives that uplift marginalized populations.",
        "common_degrees": ["BA / B.Sc Psychology", "MA Clinical Psychology", "Master of Public Policy (MPP)", "M.Plan"],
        "common_exams": ["CUET-PG", "RCI Licensure (M.Phil / Professional Diploma in Clinical Psychology)"],
        "key_skills": ["Psychological Assessment (CBT)", "Policy Analysis", "Social Impact Evaluation", "Empathetic Listening"],
        "typical_streams": ["Humanities / Arts", "Science", "Open to All"]
    },
    "Skilled Trades & Vocational Careers": {
        "slug": "skilled-trades-vocational-careers",
        "icon": "tools",
        "color": "warning",
        "tagline": "Industrial Technicians, Solar Energy, Precision Machining, Crafts & Services",
        "description": "Master essential vocational trades, industrial fabrication, renewable solar power installation, automotive mechatronics, and specialized craftsmanship driving India's infrastructure and MSME growth.",
        "common_degrees": ["ITI Trade Certificate (NCVT/SCVT)", "Diploma in Engineering", "B.Voc", "Apprenticeship NAPS"],
        "common_exams": ["AITT (All India Trade Test)", "State Polytechnic Entrance Exams"],
        "key_skills": ["Technical Blueprint Reading", "Precision Fabrication", "Electrical/Mechanical Diagnostics", "Industrial Safety Standards"],
        "typical_streams": ["Class 10 Pass", "Class 12 Any Stream", "Vocational ITI"]
    },
    "Hospitality & Tourism": {
        "slug": "hospitality-tourism",
        "icon": "cup-hot",
        "color": "info",
        "tagline": "Hotel Leadership, Culinary Arts, International Tourism, Event Curation & Resorts",
        "description": "Deliver world-class guest experiences across luxury hotel chains, Michelin-starred culinary kitchens, international eco-resorts, corporate convention centres, and global tour operations.",
        "common_degrees": ["BHM (Hotel Management)", "B.Sc Hospitality & Hotel Admin", "Diploma in Culinary Arts"],
        "common_exams": ["NCHMCT JEE", "IHM Direct Entrances"],
        "key_skills": ["Guest Experience Management", "Culinary Technique & Food Hygiene", "Revenue Management", "Front Office Operations"],
        "typical_streams": ["Any Stream (Arts, Commerce, Science)"]
    },
    "Architecture & Built Environment": {
        "slug": "architecture-built-environment",
        "icon": "building",
        "color": "primary",
        "tagline": "Architectural Design, Urban Planning, Landscape Architecture & Sustainable Habitat",
        "description": "Design sustainable cities, landmark buildings, energy-efficient interior environments, and regional infrastructure registered under the Council of Architecture (COA).",
        "common_degrees": ["B.Arch (5 Years)", "B.Plan (4 Years)", "M.Arch", "M.Plan"],
        "common_exams": ["NATA (National Aptitude Test in Architecture)", "JEE Main Paper 2 (B.Arch/B.Planning)"],
        "key_skills": ["Architectural Drafting", "Building Information Modeling (BIM)", "COA Building Bye-Laws", "Structural Sustainability"],
        "typical_streams": ["Science (PCM) with Physics, Chemistry & Mathematics"]
    },
    "Beauty, Wellness & Personal Services": {
        "slug": "beauty-wellness-personal-services",
        "icon": "gem",
        "color": "danger",
        "tagline": "Aesthetic Therapy, Clinical Cosmetology, Yoga & Integrative Wellness",
        "description": "Elevate human self-care, holistic wellness, skin aesthetics, and therapeutic lifestyle rejuvenation in luxury spas, wellness clinics, and entertainment media.",
        "common_degrees": ["Diploma in Cosmetology", "CIDESCO International Diploma", "B.Sc Yoga & Naturopathy"],
        "common_exams": ["CIDESCO Examination", "B&WSSC Certification"],
        "key_skills": ["Skin Anatomy & Analysis", "Cosmetic Hygiene Protocols", "Aesthetic Enhancement", "Client Consultation"],
        "typical_streams": ["Any Stream", "Vocational Diploma"]
    }
}

SLUG_TO_SECTOR = {meta["slug"]: name for name, meta in SECTORS_METADATA.items()}

def get_sector_by_slug(slug):
    category_name = SLUG_TO_SECTOR.get(slug)
    if not category_name:
        # Fallback check
        for name, meta in SECTORS_METADATA.items():
            if slug.lower() in meta["slug"].lower():
                return name, meta
        return None, None
    return category_name, SECTORS_METADATA[category_name]

def calculate_career_fit(career, user_input):
    """
    Evaluates fit between a Career and student input parameters.
    user_input dictionary keys:
      - stream (e.g., 'Science (PCM)', 'Science (PCB)', 'Commerce', 'Arts / Humanities', 'Any')
      - current_level ('Class 10', 'Class 12', 'Undergraduate', 'Graduate')
      - math_affinity (1 to 5)
      - tech_affinity (1 to 5)
      - people_affinity (1 to 5)
      - creative_affinity (1 to 5)
      - outdoor_affinity (1 to 5)
      - work_mode_pref ('Remote', 'Hybrid', 'On-site', 'Field')
    """
    score = 50.0  # Base neutral score
    positive_signals = []
    growth_areas = []

    c_stream = (career.preferred_streams or "").lower()
    c_desc = (career.description or "").lower() + " " + (career.technical_skills or "").lower()
    c_mode = (career.work_modes or "").lower()

    # 1. Stream alignment
    user_stream = user_input.get("stream", "").lower()
    if user_stream and user_stream != "any":
        if "any" in c_stream or "open" in c_stream:
            score += 15
            positive_signals.append("Open eligibility: Welcomes students from all academic streams.")
        elif any(k in c_stream for k in ["pcm", "math"]) and "pcm" in user_stream:
            score += 20
            positive_signals.append("Strong academic match: Your Mathematics background aligns with the quantitative foundation.")
        elif any(k in c_stream for k in ["pcb", "bio"]) and "pcb" in user_stream:
            score += 20
            positive_signals.append("Strong academic match: Your Biology/Life Sciences stream directly satisfies entry criteria.")
        elif "commerce" in c_stream and "commerce" in user_stream:
            score += 20
            positive_signals.append("Direct stream match: Your Commerce foundation accelerates understanding of financial and business principles.")
        elif "arts" in c_stream or "humanities" in c_stream and ("arts" in user_stream or "humanities" in user_stream):
            score += 20
            positive_signals.append("Strong stream alignment: Your Humanities background provides critical analytical and writing skills.")
        else:
            # Different stream - check if alternative route exists
            score -= 10
            growth_areas.append(f"Standard entry prefers {career.preferred_streams}; alternative lateral pathways may require bridge courses or entrance exams.")

    # 2. Math affinity
    math_val = int(user_input.get("math_affinity", 3))
    requires_math = any(k in c_desc for k in ["mathematics", "calculus", "statistics", "quantitative", "algorithm", "accounting"])
    if requires_math:
        if math_val >= 4:
            score += 15
            positive_signals.append("High mathematical interest matches the heavy analytical / quantitative demands.")
        elif math_val <= 2:
            score -= 15
            growth_areas.append("Involves quantitative reasoning and mathematics; may require dedicated practice to feel comfortable.")

    # 3. Tech affinity
    tech_val = int(user_input.get("tech_affinity", 3))
    is_tech = any(k in career.category.lower() for k in ["technology", "computer", "engineering"]) or any(k in c_desc for k in ["software", "coding", "python", "cad", "ai"])
    if is_tech:
        if tech_val >= 4:
            score += 15
            positive_signals.append("Your enthusiasm for technology and digital tools aligns with the core daily workload.")
        elif tech_val <= 2:
            score -= 12
            growth_areas.append("Involves continuous software tool adoption and digital problem solving.")

    # 4. Creative affinity
    creative_val = int(user_input.get("creative_affinity", 3))
    is_creative = any(k in career.category.lower() for k in ["design", "media", "creative"]) or any(k in c_desc for k in ["visual", "storytelling", "creative", "ui/ux"])
    if is_creative:
        if creative_val >= 4:
            score += 15
            positive_signals.append("High creative drive matches the portfolio-driven, expressive demands.")
        elif creative_val <= 2:
            score -= 10
            growth_areas.append("Demands aesthetic ideation and creative critique.")

    # 5. People / Empathy affinity
    people_val = int(user_input.get("people_affinity", 3))
    is_people = any(k in career.category.lower() for k in ["healthcare", "education", "social sciences", "law", "business"])
    if is_people:
        if people_val >= 4:
            score += 12
            positive_signals.append("Your enjoyment of interpersonal communication and helping others is an asset.")

    # 6. Work mode preference
    user_mode = user_input.get("work_mode_pref", "").lower()
    if user_mode:
        if user_mode in c_mode:
            score += 10
            positive_signals.append(f"Work format matches your preference: {career.work_modes}.")
        else:
            growth_areas.append(f"Typically operates as '{career.work_modes}', which differs slightly from your stated preference.")

    # Normalize score between 25% and 98%
    final_score = max(25, min(98, round(score)))

    if final_score >= 75:
        verdict = "High Potential Match"
        action_step = f"Explore Path A entry requirements and syllabus for entrance exams linked to {career.title}."
    elif final_score >= 55:
        verdict = "Promising Match with Preparation"
        action_step = "Review the required subjects and technical skills to see where you can bridge gaps."
    else:
        verdict = "Exploratory Pathway"
        action_step = "Consider this as an exploratory option or investigate related alternative careers in this sector."

    return {
        "fit_score": final_score,
        "verdict": verdict,
        "positive_signals": positive_signals[:4],
        "growth_areas": growth_areas[:3],
        "action_step": action_step
    }
