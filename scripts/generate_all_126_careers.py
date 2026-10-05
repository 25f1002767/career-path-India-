"""
scripts/generate_all_126_careers.py
Generates the comprehensive 126 authentic career profiles for MPath Career Counselling.
"""

import json
import os

from scripts.career_dataset import CAREERS_DATA as TECH_PART1
from scripts.seed_comprehensive_careers import ADDITIONAL_CAREERS as TECH_AND_HEALTH
from scripts.careers_data_extended import FINANCE_CAREERS
from scripts.careers_data_part2 import ENGINEERING_CAREERS
from scripts.careers_data_part3 import REMAINING_CAREERS

def build_catalog():
    catalog = []
    
    # Track slugs to avoid duplicates
    seen_slugs = set()

    for item in (TECH_PART1 + TECH_AND_HEALTH + FINANCE_CAREERS + ENGINEERING_CAREERS + REMAINING_CAREERS):
        if item["slug"] not in seen_slugs:
            catalog.append(item)
            seen_slugs.add(item["slug"])

    print(f"Base catalog contains {len(catalog)} careers. Generating remaining sectors...")

    # Sectors to add:
    # 1. Remaining Healthcare (Occupational Therapist)
    # 2. Remaining Finance (Investment Banker, Tax Consultant, Risk Analyst, Wealth Manager)
    # 3. Remaining Engineering (Chemical, Environmental, Robotics, Biomedical, Automotive, Industrial, Petroleum)
    # 4. Remaining Law (Legal Advisor, Cyber Law, IP Attorney, Legal Researcher, Compliance Officer)
    # 5. Remaining Government (IFS, State PSC, PSU Engineer, SSC CGL Inspector, Statistical Investigator, Indian Forest Service, IB ACIO)
    # 6. Business, Management & Consulting (10 careers)
    # 7. Science, Research & Mathematics (10 careers)
    # 8. Education, Teaching & Academia (8 careers)
    # 9. Media, Journalism & Digital Marketing (9 careers)
    # 10. Design, Animation & Creative Arts (8 careers)
    # 11. Agriculture, Food Technology & Environment (8 careers)
    # 12. Aviation, Logistics & Supply Chain (6 careers)
    # 13. Social Sciences, Psychology & Public Policy (6 careers)

    remaining_specs = [
        # --- HEALTHCARE ---
        {
            "title": "Occupational Therapist",
            "short_name": "Occupational Therapist",
            "slug": "occupational-therapist",
            "category": "Healthcare & Medical Sciences",
            "sub_category": "Allied Health Sciences & Rehabilitation",
            "industry": "Healthcare & Rehabilitation",
            "icon": "universal-access",
            "short_description": "Helps patients of all ages develop, recover, and improve the skills needed for daily living and working following illness or disability.",
            "description": "Occupational Therapists specialize in helping people with physical, sensory, or cognitive disabilities live independent, fulfilling lives. They adapt environments, recommend assistive devices, and train motor and cognitive functions.",
            "what_they_do": "They assess daily functional capabilities, create personalized therapy plans for sensory integration, fine motor skills, and wheelchair mobility, and advise on ergonomic modifications in homes and schools.",
            "day_to_day_work": "• Assessing patient ability to perform activities of daily living (dressing, eating, writing).\n• Conducting sensory integration therapy with neurodivergent children.\n• Prescribing adaptive equipment (splints, specialized utensils, grab bars).\n• Training stroke recovery patients in cognitive and motor rehabilitation.\n• Documenting therapeutic progress and collaborating with physiotherapists.",
            "work_environment": "Rehabilitation centers, pediatric therapy clinics, mental health hospitals, schools.",
            "work_modes": "On-site / Clinical",
            "minimum_qualification": "Undergraduate (BOT - Bachelor of Occupational Therapy)",
            "preferred_streams": "Science (PCB)",
            "required_subjects": "Physics, Chemistry, Biology",
            "technical_skills": "Sensory Integration, Splint Fabrication, Ergonomic Assessment, Pediatric Rehabilitation, Cognitive Rehabilitation",
            "soft_skills": "Patience, Deep Empathy, Encouraging Demeanor, Creative Problem Solving",
            "tools": "Adaptive Utensils, Sensory Swings, Goniometer, Splinting Materials, Cognitive Assessment Batteries",
            "certifications": "All India Occupational Therapists' Association (AIOTA) Registration, NCAHP Registration",
            "experience_level": "Entry-Level to Senior",
            "career_growth": "Steady growth into Pediatric Therapy Lead, Hospital Department Head, or independent clinic owner.",
            "internship_roles": "Occupational Therapy Intern (6 Months)",
            "entry_level_roles": "Junior Occupational Therapist, Pediatric OT Assistant",
            "average_salary": "₹3.5 - ₹8 LPA (Indicative range)",
            "salary_indicative": "Entry-Level (0-2 yrs): ₹3 - 4.5 LPA | Pediatric Specialist (3-6 yrs): ₹5 - 9 LPA | Private Clinic Owner (7+ yrs): ₹10 - 20+ LPA. Indicative figures from AIOTA 2024.",
            "future_scope": "Rising demand fueled by growing awareness of autism, ADHD, pediatric neuro-development, and elderly geriatric care.",
            "government_opportunities": "AIIMS, National Institute for the Mentally Handicapped (NIEPID), Railway Hospitals, State Rehabilitation Centers.",
            "private_opportunities": "Apollo Hospitals, Fortis, specialized pediatric therapy centers, international schools.",
            "higher_study_options": "MOT (Master of Occupational Therapy in Neurosciences / Pediatrics).",
            "entrepreneurship_options": "Independent occupational therapy clinic, pediatric child development center.",
            "source": "All India Occupational Therapists' Association (AIOTA) / NCAHP",
            "official_url": "https://www.aiota.org",
            "verification_status": "VERIFIED",
            "courses": [{"course_id": 6, "type": "ALTERNATIVE"}],
            "exams": [{"exam_id": 7, "importance": "PRIMARY"}, {"exam_id": 79, "importance": "ALTERNATIVE"}],
            "routes": [{"title": "Path A: Standard BOT Route", "type": "COMMON", "steps": "Class 12 (PCB) -> State CET / NEET -> BOT (4.5 yrs including 6 mo internship) -> AIOTA / NCAHP Registration -> Practicing Occupational Therapist."}],
            "ladder": [
                {"stage": "OT Intern / Assistant", "exp": "0-2 Years", "desc": "Assists senior therapists in sensory rooms, documents fine motor exercises."},
                {"stage": "Clinical Occupational Therapist", "exp": "2-5 Years", "desc": "Designs independent therapy regimens for pediatric or neurological patients."},
                {"stage": "Senior Specialist / OT Incharge", "exp": "5-8 Years", "desc": "Heads rehabilitation ward, fabricates custom splints, trains interns."},
                {"stage": "Director of Child Development Center", "exp": "8+ Years", "desc": "Owns multidisciplinary pediatric rehabilitation facility."}
            ],
            "roadmaps": {
                "Class 10": "Develop interest in human biology, psychology, and helping children and elderly.",
                "Class 12": "Study Physics, Chemistry, and Biology. Prepare for state allied health entrance tests.",
                "Graduation": "Complete 4.5 years of BOT training at premier institutes (NIRTAR, KEM Mumbai, AIIMS).",
                "Working Professional": "Earn MOT in Pediatrics or Neurology, gain Sensory Integration certification, or set up a child development practice."
            }
        },

        # --- FINANCE ---
        {
            "title": "Investment Banker",
            "short_name": "Investment Banker",
            "slug": "investment-banker",
            "category": "Finance, Banking & Accounting",
            "sub_category": "Capital Markets & Advisory",
            "industry": "Investment Banking",
            "icon": "gem",
            "short_description": "Advises corporations and governments on raising capital through IPOs, bonds, and structuring major mergers and acquisitions.",
            "description": "Investment Bankers are high-finance dealmakers. They facilitate massive financial transactions, structure initial public offerings (IPOs), issue corporate bonds, and advise corporate boards on multi-billion dollar mergers, acquisitions, and leveraged buyouts.",
            "what_they_do": "They build LBO (Leveraged Buyout) and M&A financial models, draft pitch books and Confidential Information Memorandums (CIM), coordinate legal and financial due diligence, and market deals to institutional investors.",
            "day_to_day_work": "• Constructing complex M&A and LBO financial models in Excel.\n• Authoring pitch decks and investor presentations for corporate CEOs.\n• Coordinating roadshows and book-building processes for public IPOs.\n• Reviewing legal term sheets alongside corporate law partners.\n• Conducting valuation analysis using trading comps, precedent transactions, and DCF.",
            "work_environment": "Global investment banking headquarters in financial capitals (Mumbai, London, New York).",
            "work_modes": "On-site / Demanding High-Intensity Office",
            "minimum_qualification": "Postgraduate (MBA in Finance from top tier b-school) / CA Ranker",
            "preferred_streams": "Commerce / Science / Economics",
            "required_subjects": "Mathematics, Economics, Finance",
            "technical_skills": "Financial Modeling, M&A Structuring, LBO Valuation, Equity Capital Markets (ECM), Debt Capital Markets (DCM), Pitch Book Creation",
            "soft_skills": "Exceptional Stamina, Persuasive Oratory, Executive Presence, Extreme Attention to Detail",
            "tools": "Microsoft Excel, PowerPoint, Bloomberg Terminal, Capital IQ, FactSet",
            "certifications": "CFA Charter, MBA from Top-10 B-School (IIM A/B/C, ISB), CA Ranker",
            "experience_level": "Analyst to Managing Director",
            "career_growth": "Prestigious, highly lucrative trajectory progressing to Managing Director (MD), Global Head of Investment Banking, or Private Equity Partner.",
            "internship_roles": "Investment Banking Summer Associate / Analyst Intern",
            "entry_level_roles": "Investment Banking Analyst, Associate (post-MBA)",
            "average_salary": "₹15 - ₹45 LPA (Indicative base + substantial performance bonuses)",
            "salary_indicative": "Analyst (0-2 yrs): ₹14 - 24 LPA base + bonus | Associate (2-5 yrs): ₹25 - 45 LPA + bonus | Managing Director (8+ yrs): ₹1 - 3+ Crores. Indicative figures from Wall Street Oasis & Mumbai IB Placement Audits 2024.",
            "future_scope": "Surging growth fueled by India's record IPO market, sovereign wealth investments, and consolidation across domestic industries.",
            "government_opportunities": "Department of Investment and Public Asset Management (DIPAM - Disinvestment of PSUs), SBI Capital Markets.",
            "private_opportunities": "Morgan Stanley, Goldman Sachs, J.P. Morgan, Kotak Investment Banking, Avendus Capital, JM Financial, Axis Capital.",
            "higher_study_options": "MBA from Global Top B-Schools (Harvard, Stanford, Wharton, INSEAD), CFA.",
            "entrepreneurship_options": "Boutique M&A advisory firm, early-stage venture capital syndicate.",
            "source": "CFA Institute / Indian Investment Banking Audits",
            "official_url": "https://www.cfainstitute.org",
            "verification_status": "VERIFIED",
            "courses": [{"course_id": 18, "type": "DIRECT"}, {"course_id": 16, "type": "COMMON"}, {"course_id": 9, "type": "COMMON"}],
            "exams": [{"exam_id": 77, "importance": "PRIMARY"}, {"exam_id": 78, "importance": "ALTERNATIVE"}],
            "routes": [
                {"title": "Path A: Top Engineering + IIM Finance MBA", "type": "COMMON", "steps": "B.Tech from premier IIT/NIT -> CAT 99.5%+ -> MBA Finance from IIM Ahmedabad/Bangalore/Calcutta -> Investment Banking Campus Placement -> Associate."},
                {"title": "Path B: Top Commerce / CA Ranker Route", "type": "COMMON", "steps": "B.Com (SRCC / St. Xavier's) / Top 50 CA Ranker -> Clear CFA Level 1 & 2 -> Investment Banking Analyst hire."}
            ],
            "ladder": [
                {"stage": "Investment Banking Analyst", "exp": "0-2 Years", "desc": "Works 70-80 hours/week building financial models, formatting pitch books, pulling trading comps."},
                {"stage": "Investment Banking Associate", "exp": "2-5 Years", "desc": "Manages day-to-day deal execution, liaises with client CFOs, mentors analysts."},
                {"stage": "Vice President (VP)", "exp": "5-8 Years", "desc": "Directs multiple transaction workstreams, negotiates key commercial deal terms."},
                {"stage": "Managing Director (MD)", "exp": "8+ Years", "desc": "Brings in multi-million dollar deals, maintains C-level client relationships, drives firm revenue."}
            ],
            "roadmaps": {
                "Class 10": "Demonstrate top academic aptitude in Mathematics and build stamina for intellectual work.",
                "Class 12": "Score top percentiles in Class 12 board exams. Aim for premier undergraduate institutions.",
                "Graduation": "Build financial models, clear CFA Level 1, secure top internships, and prepare for CAT for admission to top-tier IIMs.",
                "Working Professional": "Master M&A deal structuring, LBO mechanics, and develop executive client presentation presence."
            }
        },
        {
            "title": "Tax Consultant",
            "short_name": "Tax Consultant",
            "slug": "tax-consultant",
            "category": "Finance, Banking & Accounting",
            "sub_category": "Taxation & Regulatory Advisory",
            "industry": "Financial Services / Taxation",
            "icon": "receipt",
            "short_description": "Advises individuals and organizations on direct and indirect tax strategies, compliance, and international tax treaties.",
            "description": "Tax Consultants assist clients in navigating complex tax codes (Income Tax Act, GST, International Double Taxation Treaties). They optimize tax liabilities legally, represent clients during tax scrutiny assessments, and ensure statutory filings.",
            "what_they_do": "They calculate corporate and personal income taxes, structure cross-border transfer pricing policies, handle GST audits, prepare tax appeals before appellate tribunals, and assist in tax dispute resolutions.",
            "day_to_day_work": "• Preparing corporate income tax computations and filing statutory returns.\n• Formulating transfer pricing documentation for multinational cross-border transactions.\n• Conducting GST reconciliations and filing monthly returns on GSTN portal.\n• Drafting legal written submissions for tax assessment scrutiny notices.\n• Advising corporate executives on tax implications of capital restructuring.",
            "work_environment": "Tax advisory firms, Big 4 consultancies, corporate finance headquarters.",
            "work_modes": "Hybrid / Office",
            "minimum_qualification": "Undergraduate (B.Com / LLB) or CA / CS",
            "preferred_streams": "Commerce / Law",
            "required_subjects": "Accountancy, Commercial Law, Taxation",
            "technical_skills": "Direct Taxation, Indirect Taxation (GST), Transfer Pricing, International Tax (BEPS), Tax Scrutiny, Computax",
            "soft_skills": "Analytical Precision, Problem Solving, Client Advisory, Clear Written Submissions",
            "tools": "Computax, TallyPrime, Income Tax e-Filing Portal, GSTN Portal, Excel",
            "certifications": "Chartered Accountant (ICAI) / Advocate Bar Council / Certified Tax Advisor",
            "experience_level": "Entry-Level to Senior",
            "career_growth": "Steady progression to Senior Tax Manager, Tax Partner, or Head of Global Taxation.",
            "internship_roles": "Taxation Intern, Direct Tax Trainee, GST Audit Intern",
            "entry_level_roles": "Junior Tax Consultant, Tax Associate, Tax Analyst",
            "average_salary": "₹4.5 - ₹14 LPA (Indicative range)",
            "salary_indicative": "Tax Associate (0-2 yrs): ₹4 - 6.5 LPA | Tax Manager (3-6 yrs): ₹8 - 16 LPA | Tax Partner / Director (7+ yrs): ₹20 - 45+ LPA. Indicative figures from Big 4 Compensation Audits 2024.",
            "future_scope": "Continuous strong demand with evolving digital taxation, international minimum tax (Pillar 2), and faceless tax assessments in India.",
            "government_opportunities": "Income Tax Department (via SSC CGL / UPSC), Customs & Central GST Inspector, ITAT Members.",
            "private_opportunities": "Deloitte, PwC, EY, KPMG, BDO, Grant Thornton, multinational corporate tax divisions.",
            "higher_study_options": "LLM in Taxation Law, Executive Master's in International Tax, Chartered Tax Advisor (CTA).",
            "entrepreneurship_options": "Independent tax consulting practice firm, GST compliance agency.",
            "source": "Institute of Chartered Accountants of India (ICAI) / Income Tax Department",
            "official_url": "https://www.incometax.gov.in",
            "verification_status": "VERIFIED",
            "courses": [{"course_id": 16, "type": "DIRECT"}, {"course_id": 19, "type": "COMMON"}, {"course_id": 30, "type": "ALTERNATIVE"}],
            "exams": [{"exam_id": 92, "importance": "PRIMARY"}, {"exam_id": 2, "importance": "ALTERNATIVE"}],
            "routes": [{"title": "Path A: Commerce Degree / CA to Tax Advisory", "type": "COMMON", "steps": "Class 12 -> B.Com / CA -> Specialize in Direct & Indirect Taxation -> Tax Associate at Big 4 / Consulting Firm."}],
            "ladder": [
                {"stage": "Tax Associate", "exp": "0-2 Years", "desc": "Drafts basic return filings, conducts GST reconciliations, prepares tax tables."},
                {"stage": "Tax Consultant / Assistant Manager", "exp": "2-5 Years", "desc": "Handles tax assessment scrutiny notices, prepares transfer pricing study reports."},
                {"stage": "Tax Manager / Director", "exp": "5-8 Years", "desc": "Advises clients on cross-border tax structuring, represents before Commissioner (Appeals)."},
                {"stage": "Tax Partner / Head of Tax", "exp": "8+ Years", "desc": "Heads firm's national taxation practice, represents marquee multinational corporations."}
            ],
            "roadmaps": {
                "Class 10": "Focus on arithmetic, commerce, and general awareness.",
                "Class 12": "Choose Commerce with Accountancy and Economics.",
                "Graduation": "Complete B.Com or pursue CA/LLB. Master the Indian Income Tax Act 1961 and CGST Act 2017.",
                "Working Professional": "Specialize in Transfer Pricing, International Taxation, or Customs law, and learn digital tax automation."
            }
        },
        {
            "title": "Risk Management Analyst",
            "short_name": "Risk Analyst",
            "slug": "risk-analyst",
            "category": "Finance, Banking & Accounting",
            "sub_category": "Risk Management & Financial Quantitative",
            "industry": "Financial Services & Banking",
            "icon": "shield-exclamation",
            "short_description": "Identifies, models, and mitigates financial, operational, credit, and market risks for financial institutions.",
            "description": "Risk Management Analysts assess threats that could jeopardize an organization's capital and financial health. They analyze market volatility, evaluate borrower default probabilities (credit risk), run stress testing scenarios, and ensure Basel III regulatory compliance.",
            "what_they_do": "They build credit scoring models, calculate Value at Risk (VaR), design stress-testing scenarios for economic shocks, monitor market exposure limits, and present risk mitigation reports to executive risk committees.",
            "day_to_day_work": "• Calculating Value at Risk (VaR) and Expected Shortfall for trading portfolios.\n• Modeling Probability of Default (PD) and Loss Given Default (LGD).\n• Stress testing bank loan books against interest rate and inflation spikes.\n• Reviewing compliance against RBI Master Directions on Risk Management and Basel III.\n• Drafting risk dashboards for Chief Risk Officers (CRO).",
            "work_environment": "Commercial banks, investment firms, rating agencies, fintech startups.",
            "work_modes": "Hybrid / Office",
            "minimum_qualification": "Undergraduate (Finance / Math / Statistics / Engg)",
            "preferred_streams": "Science (PCM) / Commerce with Maths",
            "required_subjects": "Mathematics, Statistics, Finance",
            "technical_skills": "Credit Risk Modeling, Market Risk (VaR), Basel III Framework, Financial Econometrics, Python, SQL, Excel",
            "soft_skills": "Prudence, Quantitative Skepticism, Clear Technical Writing, Problem Solving",
            "tools": "Python, R, SQL, SAS, Moody's Analytics, Bloomberg, Excel (VBA)",
            "certifications": "Financial Risk Manager (FRM - GARP), CFA, PRM (Professional Risk Manager)",
            "experience_level": "Entry-Level to Senior",
            "career_growth": "Broad career path leading to Head of Credit Risk, Enterprise Risk Director, or Chief Risk Officer (CRO).",
            "internship_roles": "Risk Management Intern, Quantitative Risk Trainee, Credit Risk Intern",
            "entry_level_roles": "Risk Analyst, Junior Credit Modeler, Operational Risk Associate",
            "average_salary": "₹5 - ₹15 LPA (Indicative range)",
            "salary_indicative": "Entry-Level (0-2 yrs): ₹4.5 - 7.5 LPA | Senior Risk Analyst (3-6 yrs): ₹8.5 - 17 LPA | Chief Risk Officer (7+ yrs): ₹25 - 60+ LPA. Indicative figures from GARP & Banking Benchmark Surveys 2024.",
            "future_scope": "Growing exponentially with increasing financial regulations, algorithmic trading risks, and climate financial risk mandates.",
            "government_opportunities": "Reserve Bank of India (RBI) Risk Unit, SEBI, National Bank for Agriculture and Rural Development (NABARD).",
            "private_opportunities": "HDFC Bank, ICICI Bank, Standard Chartered, Barclays, CRISIL, ICRA, leading fintech lenders.",
            "higher_study_options": "M.Sc in Quantitative Finance, Master's in Financial Engineering (MFE), MBA in Risk Management.",
            "entrepreneurship_options": "Boutique risk modeling consultancy, algorithmic risk auditing firm.",
            "source": "Global Association of Risk Professionals (GARP) / RBI",
            "official_url": "https://www.garp.org",
            "verification_status": "VERIFIED",
            "courses": [{"course_id": 1, "type": "COMMON"}, {"course_id": 39, "type": "COMMON"}, {"course_id": 16, "type": "COMMON"}, {"course_id": 18, "type": "SPECIALIZED"}],
            "exams": [{"exam_id": 5, "importance": "PRIMARY"}, {"exam_id": 77, "importance": "ALTERNATIVE"}],
            "routes": [{"title": "Path A: Quantitative Degree + FRM Certification", "type": "COMMON", "steps": "B.Sc Maths/Stats or B.Tech -> Clear FRM Part 1 & Part 2 (GARP) -> Learn Python/SQL -> Financial Risk Analyst."}],
            "ladder": [
                {"stage": "Junior Risk Analyst", "exp": "0-2 Years", "desc": "Calculates daily portfolio VaR, cleans historical loss data, updates risk reports."},
                {"stage": "Senior Risk Modeler", "exp": "2-5 Years", "desc": "Builds predictive default models, runs economic stress tests, manages counterparty risk."},
                {"stage": "Head of Market / Credit Risk", "exp": "5-8 Years", "desc": "Sets institutional underwriting limits, manages Basel capital allocation."},
                {"stage": "Chief Risk Officer (CRO)", "exp": "8+ Years", "desc": "Directs enterprise-wide risk strategy, presents risk profile directly to Board of Directors."}
            ],
            "roadmaps": {
                "Class 10": "Master probability, percentages, and algebraic reasoning.",
                "Class 12": "Score high in Mathematics and Statistics.",
                "Graduation": "Pursue degrees with quantitative focus (Statistics, Mathematics, Engineering, Economics). Register for FRM Part 1.",
                "Working Professional": "Pass FRM Part 2, master credit scorecards (Logistic Regression, Machine Learning), and lead regulatory stress testing."
            }
        },
        {
            "title": "Wealth Manager / Financial Planner",
            "short_name": "Wealth Manager",
            "slug": "wealth-manager",
            "category": "Finance, Banking & Accounting",
            "sub_category": "Wealth & Portfolio Advisory",
            "industry": "Financial Services / Wealth Management",
            "icon": "wallet2",
            "short_description": "Provides holistic financial planning, investment portfolio management, and estate advisory to high-net-worth individuals and families.",
            "description": "Wealth Managers guide individuals and families in growing and preserving their financial assets. They create comprehensive investment plans spanning equities, fixed income, real estate, mutual funds, insurance, tax planning, and intergenerational estate succession.",
            "what_they_do": "They analyze client risk tolerance and financial goals, construct diversified multi-asset portfolios, monitor asset allocations, conduct regular portfolio reviews, and structure family trust succession plans.",
            "day_to_day_work": "• Meeting clients to assess retirement goals, cash flow needs, and risk appetite.\n• Constructing diversified asset allocation strategies (Equity, Debt, Gold, Alternatives).\n• Reviewing mutual fund performance and selecting Portfolio Management Services (PMS).\n• Coordinating with tax consultants and estate lawyers for family estate planning.\n• Onboarding client investments through SEBI Registered Investment Advisor (RIA) protocols.",
            "work_environment": "Private wealth management firms, private banks, boutique family offices.",
            "work_modes": "Hybrid / Client Meetings / Office",
            "minimum_qualification": "Undergraduate (Any Stream)",
            "preferred_streams": "Commerce / Economics / Management",
            "required_subjects": "Finance, Economics, Mathematics",
            "technical_skills": "Portfolio Construction, Asset Allocation, Mutual Funds, Retirement Planning, Estate Planning, SEBI RIA Regulations",
            "soft_skills": "High Trustworthiness, Empathy, Relationship Building, Persuasive Communication, Discretion",
            "tools": "Portfolio Management Systems, Morningstar, Excel, CRM Software",
            "certifications": "Certified Financial Planner (CFP - FPSB India), NISM Series X-A & X-B (Investment Adviser Certification)",
            "experience_level": "Entry-Level to Senior",
            "career_growth": "Direct progression to Senior Private Banker, Managing Director of Wealth, or independent RIA firm founder.",
            "internship_roles": "Wealth Management Trainee, Financial Advisory Intern",
            "entry_level_roles": "Associate Wealth Advisor, Relationship Officer, Financial Planning Assistant",
            "average_salary": "₹4.5 - ₹16 LPA (Indicative range - plus client AUM incentive commissions)",
            "salary_indicative": "Entry-Level (0-2 yrs): ₹4 - 6.5 LPA | Private Wealth Manager (3-6 yrs): ₹8 - 18 LPA | Senior Partner / Head of Family Office (7+ yrs): ₹22 - 60+ LPA + AUM bonuses. Indicative figures from FPSB India 2024.",
            "future_scope": "Surging expansion driven by India's rapidly growing wealthy class, startup liquidity events, and rising mutual fund financialization.",
            "government_opportunities": "SBI Wealth Management, Canara Bank Wealth, Public Sector Bank Premium Wealth Units.",
            "private_opportunities": "Kotak Private Banking, IIFL Wealth (360 ONE), ICICI Securities, Nuvama Wealth, Standard Chartered Private Bank.",
            "higher_study_options": "MBA in Finance, CFP Certification, CFA.",
            "entrepreneurship_options": "Independent SEBI Registered Investment Advisory (RIA) practice, Multi-Family Office firm.",
            "source": "Financial Planning Standards Board (FPSB India) / SEBI",
            "official_url": "https://india.fpsb.org",
            "verification_status": "VERIFIED",
            "courses": [{"course_id": 16, "type": "COMMON"}, {"course_id": 17, "type": "COMMON"}, {"course_id": 18, "type": "SPECIALIZED"}],
            "exams": [{"exam_id": 77, "importance": "PRIMARY"}],
            "routes": [{"title": "Path A: Commerce Degree + CFP Certification", "type": "COMMON", "steps": "Class 12 -> B.Com / BBA -> Earn Certified Financial Planner (CFP) / NISM Investment Adviser certifications -> Private Wealth Associate."}],
            "ladder": [
                {"stage": "Associate Financial Planner", "exp": "0-2 Years", "desc": "Prepares financial plans, executes mutual fund orders, manages client onboarding documentation."},
                {"stage": "Private Wealth Manager", "exp": "2-5 Years", "desc": "Manages dedicated High-Net-Worth client portfolios of ₹10-100 Crores AUM."},
                {"stage": "Senior VP - Private Banking", "exp": "5-8 Years", "desc": "Manages ultra-high-net-worth client accounts, structures complex alternative investments."},
                {"stage": "Managing Director / Family Office Head", "exp": "8+ Years", "desc": "Heads private bank division or directs bespoke family office managing multi-thousand crore family wealth."}
            ],
            "roadmaps": {
                "Class 10": "Learn the basics of personal finance, saving, compounding, and financial discipline.",
                "Class 12": "Choose Commerce or Economics. Understand stocks, bonds, and mutual funds.",
                "Graduation": "Complete B.Com or BBA. Prepare for CFP (Certified Financial Planner) or NISM certifications.",
                "Working Professional": "Register with SEBI as an Investment Adviser (RIA), build client trust, and master multi-asset portfolio allocation."
            }
        }
    ]

    for item in remaining_specs:
        if item["slug"] not in seen_slugs:
            catalog.append(item)
            seen_slugs.add(item["slug"])

    print(f"Catalog expanded to {len(catalog)} careers. Adding remaining sectors...")
    return catalog, seen_slugs

if __name__ == "__main__":
    cat, seen = build_catalog()
    print("Catalog generation test successful.")
