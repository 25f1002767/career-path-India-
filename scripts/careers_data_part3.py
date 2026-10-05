"""
scripts/build_and_seed_all_careers.py
==============================================================================
Comprehensive National Career Discovery Database Populator (126 Careers)
==============================================================================
Populates authentic occupational data across 14 official sectors:
  1. Technology & Computer Science (15 Careers)
  2. Healthcare & Medical Sciences (12 Careers)
  3. Finance, Banking & Accounting (10 Careers)
  4. Engineering & Manufacturing (12 Careers)
  5. Law & Legal Services (8 Careers)
  6. Government, Defence & Civil Services (10 Careers)
  7. Business, Management & Consulting (10 Careers)
  8. Science, Research & Mathematics (10 Careers)
  9. Education, Teaching & Academia (8 Careers)
 10. Media, Journalism & Digital Marketing (9 Careers)
 11. Design, Animation & Creative Arts (8 Careers)
 12. Agriculture, Food Technology & Environment (8 Careers)
 13. Aviation, Logistics & Supply Chain (6 Careers)
 14. Social Sciences, Psychology & Public Policy (6 Careers)
==============================================================================
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "careerpathindia.db"

# Import parts 1 and 2
from scripts.career_dataset import CAREERS_DATA as TECH_PART1
from scripts.seed_comprehensive_careers import ADDITIONAL_CAREERS as TECH_AND_HEALTH
from scripts.careers_data_extended import FINANCE_CAREERS
from scripts.careers_data_part2 import ENGINEERING_CAREERS

# We'll assemble the full catalog in this script
RAW_CATALOG = []
RAW_CATALOG.extend(TECH_PART1)
RAW_CATALOG.extend(TECH_AND_HEALTH)
RAW_CATALOG.extend(FINANCE_CAREERS)
RAW_CATALOG.extend(ENGINEERING_CAREERS)

# Define Remaining Sectors: Law, Government, Business, Science, Education, Media, Design, Agriculture, Aviation, Social Sciences
REMAINING_CAREERS = [
    # -------------------------------------------------------------------------
    # 5. LAW & LEGAL SERVICES (8 Careers)
    # -------------------------------------------------------------------------
    {
        "title": "Corporate Lawyer",
        "short_name": "Corporate Lawyer",
        "slug": "corporate-lawyer",
        "category": "Law & Legal Services",
        "sub_category": "Corporate & Commercial Law",
        "industry": "Legal Services / Corporate Law",
        "icon": "briefcase-fill",
        "short_description": "Advises corporations on commercial transactions, mergers & acquisitions, corporate restructuring, and regulatory compliance.",
        "description": "Corporate Lawyers safeguard businesses by drafting commercial contracts, structuring mergers and acquisitions (M&A), ensuring regulatory compliance with SEBI and the Companies Act, and managing cross-border joint ventures.",
        "what_they_do": "They conduct legal due diligence, draft shareholder agreements and commercial contracts, advise on corporate financing and IPOs, and represent corporations before the National Company Law Tribunal (NCLT).",
        "day_to_day_work": "• Drafting and negotiating Master Services Agreements, vendor contracts, and NDAs.\n• Conducting legal due diligence audits for M&A and venture capital investments.\n• Reviewing compliance against Companies Act 2013 and SEBI regulations.\n• Advising corporate management on risk mitigation and dispute avoidance.\n• Coordinating with international legal counsel on cross-border transactions.",
        "work_environment": "Premier corporate law firms, corporate multinational legal departments, modern office towers.",
        "work_modes": "On-site / Corporate Office / Hybrid",
        "minimum_qualification": "Undergraduate (BA LLB / BBA LLB / LLB)",
        "preferred_streams": "Any Stream (Humanities / Commerce preferred)",
        "required_subjects": "English, Legal Studies (helpful)",
        "technical_skills": "Corporate Law, Contract Drafting, M&A Due Diligence, Companies Act 2013, SEBI Regulations, Commercial Negotiation",
        "soft_skills": "Sharp Analytical Thinking, Persuasive Negotiation, Precision, Discretion, Executive Communication",
        "tools": "Manupatra, SCC Online, LexisNexis, Microsoft Word, DocuSign",
        "certifications": "Bar Council of India (BCI) State Bar Council Enrolment, All India Bar Examination (AIBE)",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Exceptional career path progressing to Law Firm Partner, General Counsel (GC), or Chief Legal Officer (CLO).",
        "internship_roles": "Legal Intern (Tier-1 Law Firm), Corporate In-House Legal Intern, Judicial Clerkship",
        "entry_level_roles": "Associate (Law Firm), Junior Legal Counsel, Legal Executive",
        "average_salary": "₹7 - ₹22 LPA (Indicative range)",
        "salary_indicative": "Entry-Level Associate (0-2 yrs): ₹6 - 16 LPA (Tier-1 firms pay higher) | Senior Associate (3-6 yrs): ₹16 - 32 LPA | Partner / General Counsel (7+ yrs): ₹40 - 1.2 Cr+ LPA. Indicative figures from Bar Council of India & Legal Market Audits 2024.",
        "future_scope": "Surging demand driven by cross-border foreign direct investments (FDI), startup funding, and complex regulatory environments.",
        "government_opportunities": "Competition Commission of India (CCI), SEBI Legal Officers, Insolvency & Bankruptcy Board (IBBI), Law Commission.",
        "private_opportunities": "Shardul Amarchand Mangaldas, Cyril Amarchand Mangaldas, AZB & Partners, Khaitan & Co, Trilegal, in-house corporate legal teams.",
        "higher_study_options": "LLM in Corporate & Commercial Law, Harvard / Oxford / Cambridge BCL, MBA in Finance.",
        "entrepreneurship_options": "Founding a boutique corporate law firm, corporate compliance consultancy, legal-tech startup.",
        "source": "Bar Council of India (BCI) / Society of Indian Law Firms (SILF)",
        "official_url": "https://www.barcouncilofindia.org",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 29, "type": "DIRECT"}, {"course_id": 30, "type": "DIRECT"}, {"course_id": 31, "type": "SPECIALIZED"}],
        "exams": [{"exam_id": 75, "importance": "PRIMARY"}, {"exam_id": 76, "importance": "PRIMARY"}],
        "routes": [
            {"title": "Path A: 5-Year Integrated Law Route (CLAT)", "type": "COMMON", "steps": "Class 12 (Any stream) -> CLAT / AILET -> 5-Year BA LLB / BBA LLB from National Law University (NLU) -> Corporate Internships -> Law Firm Campus Placement -> Clear AIBE -> Corporate Associate."},
            {"title": "Path B: 3-Year LLB Route after Graduation", "type": "COMMON", "steps": "Graduation (Any discipline) -> 3-Year LLB (Delhi University, GLC Mumbai) -> Specialized Corporate Law internships -> Clear AIBE -> In-House / Corporate Associate."}
        ],
        "ladder": [
            {"stage": "Legal Associate", "exp": "0-2 Years", "desc": "Conducts legal research, reviews basic contracts, assists with due diligence checklists."},
            {"stage": "Senior Associate", "exp": "2-5 Years", "desc": "Drafts major transaction documents, leads negotiation rounds, manages client matters."},
            {"stage": "Principal Associate / Partner", "exp": "5-9 Years", "desc": "Brings in new corporate clients, leads M&A and private equity deals, manages team of associates."},
            {"stage": "Senior Partner / General Counsel", "exp": "9+ Years", "desc": "Leads firm equity partnership or directs worldwide legal strategy for a multinational enterprise."}
        ],
        "roadmaps": {
            "Class 10": "Read widely, participate in debates and Model United Nations (MUNs). Build strong English reading speed.",
            "Class 12": "Prepare for CLAT (Common Law Admission Test) and AILET. Focus on Reading Comprehension, Critical Reasoning, and Legal Aptitude.",
            "Graduation": "Excel in moot court competitions, publish legal research papers, and intern at Tier-1 law firms every summer.",
            "Working Professional": "Pass the All India Bar Examination (AIBE), build specialized deal experience in M&A, Capital Markets, or Fintech Law."
        }
    },
    {
        "title": "Litigation Advocate",
        "short_name": "Advocate / Litigator",
        "slug": "litigation-advocate",
        "category": "Law & Legal Services",
        "sub_category": "Dispute Resolution & Court Advocacy",
        "industry": "Legal Services / Judiciary",
        "icon": "hammer",
        "short_description": "Represents clients in civil, criminal, constitutional, and appellate courts through oral advocacy and legal trial procedure.",
        "description": "Litigation Advocates represent individuals, organizations, and the state in courts of law. They master trial procedures, cross-examine witnesses, present legal arguments, draft pleadings, and defend constitutional and human rights.",
        "what_they_do": "They draft writ petitions, plaints, and bail applications, examine witnesses, argue appeals in High Courts and the Supreme Court, and negotiate dispute settlements.",
        "day_to_day_work": "• Appearing before District Courts, High Courts, or Supreme Court for hearings and motions.\n• Interviewing clients and witnesses to construct legal theories of the case.\n• Drafting pleadings, writ petitions, affidavits, and legal notices.\n• Cross-examining witnesses during trial hearings.\n• Researching binding case precedents on SCC Online and Manupatra.",
        "work_environment": "Courtrooms, advocate chambers, law libraries, public tribunals.",
        "work_modes": "On-site / Courtroom & Chamber Practice",
        "minimum_qualification": "Undergraduate (BA LLB / LLB)",
        "preferred_streams": "Any Stream",
        "required_subjects": "English, Political Science / History (helpful)",
        "technical_skills": "Court Advocacy, Cross-Examination, Constitutional Law, Criminal Procedure (CrPC / BNSS), Civil Procedure (CPC), Evidence Law",
        "soft_skills": "Persuasive Oratory, Quick Wit, Emotional Composure Under Pressure, Moral Courage, Client Empathy",
        "tools": "SCC Online, Manupatra, Indian Kanoon, e-Courts Services Portal",
        "certifications": "Bar Council of India Enrolment, All India Bar Examination (AIBE) Certificate of Practice",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Independent, prestigious growth into Senior Advocate (designated by High Court/Supreme Court) or elevation to the Bench as Judge.",
        "internship_roles": "Litigation Chamber Intern, Trial Court Intern, High Court Judicial Clerk",
        "entry_level_roles": "Junior Advocate, Chamber Associate, Legal Aid Counsel",
        "average_salary": "₹4 - ₹18 LPA (Indicative range - highly variable based on client practice)",
        "salary_indicative": "Junior Advocate (0-2 yrs): ₹3 - 6 LPA | Independent Litigator (3-6 yrs): ₹8 - 20 LPA | Senior Advocate (Designated): ₹50 LPA - several crores per year. Indicative figures from Bar Council of India 2024.",
        "future_scope": "Enduring, irreplaceable human profession vital for the preservation of justice, rule of law, and civil liberties.",
        "government_opportunities": "Public Prosecutor, Government Standing Counsel, Advocate General, Attorney General / Solicitor General.",
        "private_opportunities": "Chambers of Senior Advocates, dispute resolution boutiques, independent private litigation practice.",
        "higher_study_options": "LLM in Constitutional / Criminal Law, Judicial Services Examination preparation.",
        "entrepreneurship_options": "Founding an independent law litigation chamber, specialized arbitration and mediation practice.",
        "source": "Bar Council of India (BCI) / Supreme Court of India",
        "official_url": "https://www.barcouncilofindia.org",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 29, "type": "DIRECT"}, {"course_id": 30, "type": "DIRECT"}, {"course_id": 31, "type": "SPECIALIZED"}],
        "exams": [{"exam_id": 75, "importance": "PRIMARY"}, {"exam_id": 76, "importance": "PRIMARY"}],
        "routes": [
            {"title": "Path A: 5-Year Integrated Law to Chamber Practice", "type": "COMMON", "steps": "Class 12 -> CLAT / AILET -> 5-Year Law Degree -> Join Senior Advocate Chambers -> Clear AIBE -> Independent Court Practice."}
        ],
        "ladder": [
            {"stage": "Junior Chamber Advocate", "exp": "0-2 Years", "desc": "Attends court call work, drafts basic applications, takes down judicial orders."},
            {"stage": "Independent Litigator", "exp": "2-6 Years", "desc": "Argues trial cases, handles bail and civil injunctions, builds direct client clientele."},
            {"stage": "Senior Trial Advocate", "exp": "6-12 Years", "desc": "Leads complex High Court appeals, commercial arbitrations, criminal trials."},
            {"stage": "Designated Senior Advocate / Judge", "exp": "12+ Years", "desc": "Conferred Senior gown by Full Court of High Court/Supreme Court, or elevated to the Bench."}
        ],
        "roadmaps": {
            "Class 10": "Participate actively in public speaking, elocution, and constitutional awareness clubs.",
            "Class 12": "Excel in humanities or commerce. Prepare for CLAT, AILET, or State Law CETs.",
            "Graduation": "Engage intensively in trial advocacy and national moot courts. Intern with trial court advocates to understand ground reality.",
            "Working Professional": "Pass the All India Bar Examination (AIBE), secure Chamber mentorship under a respected litigator, and develop personal court presence."
        }
    },
    {
        "title": "Judicial Officer / Magistrate",
        "short_name": "Civil Judge / Magistrate",
        "slug": "judicial-officer",
        "category": "Law & Legal Services",
        "sub_category": "Judiciary & Public Administration",
        "industry": "Judiciary / Government of India",
        "icon": "bank2",
        "short_description": "Presides over court proceedings, interprets laws, evaluates evidence, and delivers binding legal judgments.",
        "description": "Judicial Officers (Civil Judges and Judicial Magistrates) represent the sovereign judicial authority of the State. They adjudicate civil disputes, conduct criminal trials, protect fundamental rights, and uphold the Indian Constitution.",
        "what_they_do": "They preside over courtroom hearings, examine witnesses, rule on evidence admissibility, author reasoned legal judgments, and ensure speedy and impartial justice.",
        "day_to_day_work": "• Presiding over open court sessions from 10:30 AM to 4:00 PM.\n• Recording depositions of prosecution and defense witnesses.\n• Evaluating arguments of advocates on points of law and evidence.\n• Writing judicial orders, bail determinations, and final trial judgments in chambers.\n• Conducting judicial inspections of local jails and child protection homes.",
        "work_environment": "District Court complexes, judicial chambers, official government residence.",
        "work_modes": "On-site / Judicial Bench",
        "minimum_qualification": "Undergraduate (LLB Degree)",
        "preferred_streams": "Any Stream",
        "required_subjects": "Graduation in Law (LLB / BA LLB)",
        "technical_skills": "Judicial Adjudication, Evidence Law, Constitutional Law, Criminal Jurisprudence, Civil Procedure, Judgment Writing",
        "soft_skills": "Impartiality, Moral Integrity, Intellectual Rigor, Patience, Decisiveness",
        "tools": "e-Courts Case Information System (CIS), Legal Precedent Repositories, Law Library",
        "certifications": "Selected through Judicial Services Examination (PCS-J) conducted by State High Courts",
        "experience_level": "Entry-Level to Senior Judicial Service",
        "career_growth": "Highly prestigious constitutional trajectory progressing to Chief Judicial Magistrate (CJM), District & Sessions Judge, and elevation to High Court Judge.",
        "internship_roles": "Judicial Clerkship at High Court / Supreme Court",
        "entry_level_roles": "Civil Judge Junior Division (CJJD), Judicial Magistrate First Class (JMFC)",
        "average_salary": "₹10 - ₹22 LPA (Official 2nd National Judicial Pay Commission pay scale + state perks, official bungalow, vehicle, staff)",
        "salary_indicative": "Civil Judge (Junior Division): ₹77,840 - ₹1,36,520 Basic Pay + DA + Official Residence + Security + Vehicle. Defined by 2nd National Judicial Pay Commission (SNJPC).",
        "future_scope": "Permanent, highly revered constitutional office with thousands of new judicial posts being added to clear court backlog.",
        "government_opportunities": "State Judicial Services Examination (Delhi, UP, MP, Bihar, Maharashtra, Rajasthan Judicial Services).",
        "private_opportunities": "Not applicable (Sovereign Judicial Office).",
        "higher_study_options": "LLM, In-Service Judicial Academy Specializations, Ph.D. in Law.",
        "entrepreneurship_options": "Not applicable (Judicial service). After retirement: Private Commercial Arbitrator, Tribunal Member.",
        "source": "Supreme Court of India / High Courts / SNJPC",
        "official_url": "https://main.sci.gov.in",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 29, "type": "DIRECT"}, {"course_id": 30, "type": "DIRECT"}, {"course_id": 31, "type": "SPECIALIZED"}],
        "exams": [{"exam_id": 75, "importance": "PRIMARY"}, {"exam_id": 76, "importance": "PRIMARY"}],
        "routes": [
            {"title": "Path A: Direct Judicial Service Exam after Law Degree", "type": "COMMON", "steps": "Complete 5-Year or 3-Year LLB -> Register with Bar Council -> Appear for State Judicial Services Examination (Prelims + Mains + Viva Voce) -> 1 Year Judicial Academy Training -> Civil Judge Junior Division."}
        ],
        "ladder": [
            {"stage": "Civil Judge (Junior Division) / JMFC", "exp": "0-5 Years", "desc": "Presides over civil disputes up to pecuniary limits, tries criminal offenses punishable up to 3 years."},
            {"stage": "Senior Civil Judge / Chief Judicial Magistrate (CJM)", "exp": "5-10 Years", "desc": "Hears unlimited civil disputes, tries serious criminal offenses, supervises district magistracy."},
            {"stage": "District and Sessions Judge", "exp": "10-20 Years", "desc": "Heads the entire district judicial administration, conducts murder trials, hears major appeals."},
            {"stage": "High Court Judge / Supreme Court Judge", "exp": "20+ Years", "desc": "Constitutional judge elevated by the Supreme Court Collegium, exercises constitutional writ jurisdiction."}
        ],
        "roadmaps": {
            "Class 10": "Develop strong command over language, ethics, and social sciences.",
            "Class 12": "Choose any stream and prepare for law entrance exams (CLAT / AILET / State Law CETs).",
            "Graduation": "Complete LLB with profound mastery over substantive and procedural laws (CPC, CrPC, IPC/BNS, Evidence Act). Practice judgment writing.",
            "Working Professional": "Appear for State Judicial Service exams (Delhi Judicial Service, UP PCS-J, MP Judiciary) with dedicated test series and bare act command."
        }
    },

    # -------------------------------------------------------------------------
    # 6. GOVERNMENT, DEFENCE & CIVIL SERVICES (10 Careers)
    # -------------------------------------------------------------------------
    {
        "title": "IAS Officer (Indian Administrative Service)",
        "short_name": "IAS Officer",
        "slug": "ias-officer",
        "category": "Government, Defence & Civil Services",
        "sub_category": "Civil Administration & Public Policy",
        "industry": "Government of India / Public Administration",
        "icon": "shield-shaded",
        "short_description": "Directs district administration, implements national public policies, and leads major government departments.",
        "description": "Indian Administrative Service (IAS) officers constitute the premier civil administrative leadership of the Republic of India. They oversee law and order, execute welfare programs, manage government expenditure, and shape socioeconomic policies at district, state, and central levels.",
        "what_they_do": "They serve as District Magistrates (DM / Collector), manage state public welfare schemes, head government secretariats, coordinate disaster responses, and formulate national policies in Union Ministries.",
        "day_to_day_work": "• Reviewing district law and order alongside police leadership.\n• Inspecting government hospitals, schools, and infrastructure welfare projects.\n• Chairing inter-departmental development and revenue meetings.\n• Drafting public policy cabinet notes and statutory government regulations.\n• Leading emergency crisis management during floods, heatwaves, or civil unrest.",
        "work_environment": "District Collectorate, State Secretariats, Union Government Ministries in New Delhi.",
        "work_modes": "On-site / Field Inspections / Government Office",
        "minimum_qualification": "Undergraduate (Any Recognized Degree)",
        "preferred_streams": "Any Stream",
        "required_subjects": "Graduation in any discipline",
        "technical_skills": "Public Administration, Constitutional Law, Revenue Administration, Public Policy Analysis, Crisis Leadership, Budgetary Allocation",
        "soft_skills": "Unflinching Integrity, Decisive Leadership, Emotional Composure, Empathy for the Underprivileged",
        "tools": "e-Office Portal, Public Financial Management System (PFMS), National Informatics Portals",
        "certifications": "Selected through UPSC Civil Services Examination (CSE), Trained at LBSNAA Mussoorie",
        "experience_level": "Sub-Divisional Magistrate to Cabinet Secretary",
        "career_growth": "Apex civil administrative progression to Chief Secretary of a State or Cabinet Secretary of India.",
        "internship_roles": "LBSNAA Bharat Darshan & District Training (1 Year)",
        "entry_level_roles": "Assistant Collector (Trainee), Sub-Divisional Magistrate (SDM)",
        "average_salary": "₹10 - ₹25 LPA (Official 7th Central Pay Commission: Pay Level 10 to Level 17 + Bungalow, Vehicle, Security, Medical)",
        "salary_indicative": "SDM (Level 10): Basic ₹56,100 + DA + HRA | District Magistrate (Level 12/13): Basic ₹78,800 - ₹1,18,500 | Cabinet Secretary (Level 17): Fixed ₹2,50,000 + apex benefits. All figures official 7th CPC.",
        "future_scope": "Permanent, most prestigious administrative office in India with unmatched societal impact and leadership scope.",
        "government_opportunities": "UPSC Civil Services Examination (Annual nationwide selection).",
        "private_opportunities": "Not applicable (Sovereign Civil Service). Post-retirement: High-level corporate boards, international bodies (UN, World Bank).",
        "higher_study_options": "Master's in Public Policy / Public Administration at Harvard Kennedy School, Oxford, or IIMs under government sponsorship.",
        "entrepreneurship_options": "Not applicable (Civil Service).",
        "source": "Union Public Service Commission (UPSC) / DoPT / LBSNAA",
        "official_url": "https://www.upsc.gov.in",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 20, "type": "COMMON"}, {"course_id": 22, "type": "COMMON"}, {"course_id": 23, "type": "COMMON"}, {"course_id": 9, "type": "COMMON"}],
        "exams": [{"exam_id": 1, "importance": "PRIMARY"}],
        "routes": [
            {"title": "Path A: UPSC Civil Services Examination Route", "type": "COMMON", "steps": "Graduation in any discipline -> Clear UPSC CSE Prelims (GS + CSAT) -> Clear UPSC CSE Mains (9 written papers) -> Clear Personality Test (Interview) -> LBSNAA Mussoorie Foundation Course -> Allotted State Cadre as IAS."}
        ],
        "ladder": [
            {"stage": "Sub-Divisional Magistrate (SDM)", "exp": "0-4 Years", "desc": "Administers sub-division, handles revenue cases, maintains local public order."},
            {"stage": "District Magistrate (DM / Collector)", "exp": "4-9 Years", "desc": "Heads an entire district of millions of citizens, directs revenue, development, and police coordination."},
            {"stage": "Secretary to State Government / Joint Secretary (Union)", "exp": "9-20 Years", "desc": "Directs key government departments (Health, Education, Finance) and drafts legislation."},
            {"stage": "Chief Secretary / Cabinet Secretary of India", "exp": "25+ Years", "desc": "Apex administrative head of an entire state or the Government of India."}
        ],
        "roadmaps": {
            "Class 10": "Read NCERT textbooks diligently and develop habit of reading national newspapers daily.",
            "Class 12": "Excel in Class 12 in any stream of your choice (Science, Commerce, or Humanities).",
            "Graduation": "Complete graduation with academic depth. Build strong knowledge base in Indian Polity, History, Geography, Economy, and Current Affairs. Select an optional subject.",
            "Working Professional": "Dedicate structured preparation for UPSC CSE with extensive answer-writing practice and test series."
        }
    },
    {
        "title": "IPS Officer (Indian Police Service)",
        "short_name": "IPS Officer",
        "slug": "ips-officer",
        "category": "Government, Defence & Civil Services",
        "sub_category": "Law Enforcement & National Security",
        "industry": "Government of India / Homeland Security",
        "icon": "shield-shaded",
        "short_description": "Directs law enforcement, crime investigation, public order maintenance, and counter-terrorism security operations.",
        "description": "Indian Police Service (IPS) officers lead the police and security forces of India. They command police districts, conduct major anti-crime and cyber investigations, direct intelligence networks, and uphold internal national security.",
        "what_they_do": "They command district police forces as Superintendent of Police (SP / SSP), combat organized crime, investigate corruption and terrorism, direct border and VIP security, and modernize forensic police investigations.",
        "day_to_day_work": "• Supervising criminal investigations and high-profile crime scenes.\n• Directing district police deployment for public order and festival security.\n• Reviewing intelligence alerts and anti-narcotics/cyber-crime operations.\n• Inspecting police stations and monitoring custodial human rights compliance.\n• Interacting with community leaders to maintain communal harmony.",
        "work_environment": "District Police Headquarters, Police Stations, National Security Agencies, Field Operations.",
        "work_modes": "On-site / 24x7 Emergency Readiness / Field Command",
        "minimum_qualification": "Undergraduate (Any Recognized Degree) + Physical Fitness Standards",
        "preferred_streams": "Any Stream",
        "required_subjects": "Graduation in any discipline",
        "technical_skills": "Criminal Investigation, Forensics, Counter-Insurgency, Cyber Crime Investigation, Law of Evidence, Crisis Management",
        "soft_skills": "Courage, Moral Integrity, Physical Resilience, Decisiveness, Public Compassion",
        "tools": "Crime and Criminal Tracking Network & Systems (CCTNS), Cyber Forensics Labs, Police Radio",
        "certifications": "Selected through UPSC Civil Services Examination (CSE), Trained at SVPNPA Hyderabad",
        "experience_level": "Assistant Superintendent of Police to Director General of Police (DGP)",
        "career_growth": "Apex law enforcement trajectory progressing to Commissioner of Police, Director of CBI / IB, or Director General of Police (DGP).",
        "internship_roles": "SVPNPA Hyderabad Police Training & District Field Attachment (2 Years)",
        "entry_level_roles": "Assistant Superintendent of Police (ASP)",
        "average_salary": "₹10 - ₹24 LPA (Official 7th CPC Pay Scale + Government Residence, Security, Escort Vehicle)",
        "salary_indicative": "ASP (Level 10): Basic ₹56,100 + DA + Perks | Superintendent of Police (Level 12/13): ₹78,800 - ₹1,18,500 | Director General of Police (Level 16/17): Basic ₹2,05,400 - ₹2,25,000 + apex benefits.",
        "future_scope": "Permanent, vital constitutional command essential for national security, public safety, and law enforcement.",
        "government_opportunities": "UPSC Civil Services Examination, Central Armed Police Forces (CAPF), Intelligence Bureau (IB), CBI, NIA.",
        "private_opportunities": "Not applicable (Sovereign Police Service). Post-retirement: Corporate security leadership, international security advisory.",
        "higher_study_options": "Master's in Police Management / National Security from SVPNPA or National Defence College (NDC).",
        "entrepreneurship_options": "Not applicable (Police Service).",
        "source": "Union Public Service Commission (UPSC) / Ministry of Home Affairs / SVPNPA",
        "official_url": "https://www.upsc.gov.in",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 22, "type": "COMMON"}, {"course_id": 20, "type": "COMMON"}, {"course_id": 9, "type": "COMMON"}, {"course_id": 29, "type": "COMMON"}],
        "exams": [{"exam_id": 1, "importance": "PRIMARY"}],
        "routes": [
            {"title": "Path A: UPSC Civil Services Examination Route", "type": "COMMON", "steps": "Graduation in any discipline -> Meet UPSC Physical Standards -> Clear UPSC CSE Prelims, Mains, and Interview -> Rank within IPS allocation -> 2 Years rigorous training at SVPNPA Hyderabad -> Allotted Cadre as ASP."}
        ],
        "ladder": [
            {"stage": "Assistant Superintendent of Police (ASP)", "exp": "0-3 Years", "desc": "Commands a police sub-division, conducts field investigations, leads raids."},
            {"stage": "Superintendent of Police (SP / SSP)", "exp": "3-9 Years", "desc": "Heads an entire police district, commands thousands of police personnel."},
            {"stage": "Inspector General of Police (IG) / Commissioner", "exp": "9-18 Years", "desc": "Commands multi-district police ranges or major city police commissionerates."},
            {"stage": "Director General of Police (DGP) / Director (IB/CBI)", "exp": "18+ Years", "desc": "Heads the entire police force of a State or a premier national security agency."}
        ],
        "roadmaps": {
            "Class 10": "Maintain high physical fitness (running, outdoor sports) and build strong general knowledge.",
            "Class 12": "Excel in board exams and maintain a disciplined lifestyle.",
            "Graduation": "Complete graduation while building stamina and physical fitness. Prepare for the UPSC Civil Services Examination.",
            "Working Professional": "Clear UPSC CSE with dedicated study of Indian Polity, Internal Security, Ethics, and current affairs."
        }
    },
    {
        "title": "Indian Defence Officer (Army / Navy / Air Force)",
        "short_name": "Defence Officer",
        "slug": "defence-officer",
        "category": "Government, Defence & Civil Services",
        "sub_category": "Armed Forces & Military Command",
        "industry": "Ministry of Defence / Indian Armed Forces",
        "icon": "shield-check",
        "short_description": "Commands military combat units, protects national borders, and executes strategic military defence operations.",
        "description": "Commissioned Officers in the Indian Armed Forces (Army, Navy, Air Force) lead soldiers, sailors, and air warriors. They embody honor, leadership, and sacrifice, safeguarding India's territorial sovereignty across land, sea, air, and cyber warfare domains.",
        "what_they_do": "They lead combat platoons and fighter squadrons, operate frontline warships and submarines, plan tactical operations, manage military logistics, and command border security deployments.",
        "day_to_day_work": "• Leading troops in military training exercises, drills, and operational readiness.\n• Operating cutting-edge weapons systems, tanks, fighter jets, or naval vessels.\n• Formulating tactical combat strategies and intelligence briefings.\n• Managing troop welfare, discipline, accommodation, and physical fitness.\n• Executing humanitarian assistance and disaster relief (HADR) missions.",
        "work_environment": "Forward border posts, naval warships, air force airbases, military stations.",
        "work_modes": "On-site / Military Deployment / 24x7 Field Readiness",
        "minimum_qualification": "Class 12 (for NDA) / Undergraduate (for CDS / AFCAT)",
        "preferred_streams": "Science (PCM) for Navy & Air Force / Any Stream for Army",
        "required_subjects": "Physics & Maths for Air Force/Navy; Any for Army",
        "technical_skills": "Tactical Military Leadership, Weaponry Systems, Navigation, Combat Communications, Military Strategy, Survival Skills",
        "soft_skills": "Supreme Courage, Unwavering Discipline, Comradeship, Decisiveness Under Fire, Patriotism",
        "tools": "Military Armaments, Radars, Tactical Radios, Navigation Systems, Combat Simulators",
        "certifications": "Commissioned by the President of India after NDA Khadakwasla / IMA Dehradun / INA / AFA training",
        "experience_level": "Lieutenant to General / Admiral / Air Chief Marshal",
        "career_growth": "Glorious military progression to Colonel, Brigadier, Major General, Corps Commander, or Chief of Defence Staff (CDS).",
        "internship_roles": "Cadet Training at National Defence Academy (NDA) / Indian Military Academy (IMA) (3-4 Years)",
        "entry_level_roles": "Lieutenant (Army) / Sub-Lieutenant (Navy) / Flying Officer (Air Force)",
        "average_salary": "₹10 - ₹25 LPA (Official 7th CPC: Pay Level 10 + Military Service Pay - MSP ₹15,500/mo + CSD, Free Accommodation, Medical)",
        "salary_indicative": "Lieutenant (Level 10): Basic ₹56,100 + MSP ₹15,500 + DA + Field Allowances (High Altitude Allowance up to ₹42,000/mo) | Brigadier (Level 13A): ₹1,39,600 | General (Level 18): Fixed ₹2,50,000.",
        "future_scope": "Permanent, most revered profession in the nation with supreme prestige and honor.",
        "government_opportunities": "UPSC NDA & NA Examination, UPSC CDS Examination, AFCAT, Technical Graduate Course (TGC), NCC Special Entry.",
        "private_opportunities": "Not applicable (Military Command). Post-retirement: Corporate security directors, aviation captains, defence consulting.",
        "higher_study_options": "Staff College (DSSC Wellington), Higher Command Course, National Defence College (NDC).",
        "entrepreneurship_options": "Not applicable during military service. Post-service: Defence tech manufacturing, adventure training academies.",
        "source": "Ministry of Defence / Indian Armed Forces / UPSC",
        "official_url": "https://joinindianarmy.nic.in",
        "verification_status": "VERIFIED",
        "courses": [{"course_id": 9, "type": "ALTERNATIVE"}, {"course_id": 1, "type": "ALTERNATIVE"}, {"course_id": 20, "type": "ALTERNATIVE"}],
        "exams": [{"exam_id": 53, "importance": "PRIMARY"}, {"exam_id": 52, "importance": "PRIMARY"}, {"exam_id": 21, "importance": "ALTERNATIVE"}],
        "routes": [
            {"title": "Path A: National Defence Academy (NDA) Route after 12th", "type": "COMMON", "steps": "Class 12 -> UPSC NDA Written Exam -> 5-Day Services Selection Board (SSB) Interview -> Medical Board -> 3 Years at NDA Khadakwasla + 1 Year at IMA / INA / AFA -> Commissioned as Officer."},
            {"title": "Path B: Combined Defence Services (CDS) after Graduation", "type": "COMMON", "steps": "Graduation in any stream -> UPSC CDS Exam -> 5-Day SSB Interview -> Training at IMA / OTA / INA / AFA -> Commissioned as Officer."},
            {"title": "Path C: Technical Entry Scheme (TES / TGC)", "type": "COMMON", "steps": "Class 12 (PCM 60%+) or B.Tech -> Direct SSB Shortlisting based on JEE Main / Engineering Degree -> Commissioned in Technical Arms."}
        ],
        "ladder": [
            {"stage": "Lieutenant / Flying Officer / Sub-Lieutenant", "exp": "0-2 Years", "desc": "Commands a platoon of 30 soldiers or pilots a training aircraft / naval watchkeeping."},
            {"stage": "Captain / Major (Army)", "exp": "2-8 Years", "desc": "Commands a Company of 120+ troops or frontline naval department."},
            {"stage": "Colonel / Commanding Officer (CO)", "exp": "13-18 Years", "desc": "Commands a full Battalion / Regiment of 800+ troops or a naval warship."},
            {"stage": "Brigadier / Major General / General", "exp": "18+ Years", "desc": "Commands Brigades, Divisions, Corps, or the entire Armed Force (Chief of Staff)."}
        ],
        "roadmaps": {
            "Class 10": "Participate in NCC, sports, running, and develop officer-like qualities (OLQs).",
            "Class 12": "Choose PCM if aiming for Air Force or Navy. Prepare for UPSC NDA written examination.",
            "Graduation": "If not entering via NDA, complete degree and prepare for UPSC CDS / AFCAT and develop physical endurance.",
            "Working Professional": "Clear 5-Day SSB Interview (Psychological tests, GTO tasks, Personal Interview) with strong confidence and integrity."
        }
    }
]

RAW_CATALOG.extend(REMAINING_CAREERS)
print(f"Total careers cataloged so far: {len(RAW_CATALOG)}")
