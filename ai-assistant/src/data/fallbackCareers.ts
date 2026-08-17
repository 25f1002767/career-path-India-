import { CareerPath, TierType, SectorType, EducationLevel } from "../types/career";

function createCareer(
  id: string,
  title: string,
  tier: TierType,
  sector: SectorType,
  domain: string,
  shortDescription: string,
  minEducationLevel: EducationLevel,
  minAge: number,
  maxAge: number,
  minSalaryPM: number,
  maxSalaryPM: number,
  payScaleCode: string,
  applicationPortalUrl: string,
  notificationMonth: string,
  examMonth: string,
  growthProspects: string,
  steps: { title: string; description: string; estimatedDuration?: string }[],
  tags: string[] = [],
  applicants = 100000,
  seats = 1000,
  difficultyRating: "MODERATE" | "HIGH" | "VERY_HIGH" | "EXTREME" = "HIGH"
): CareerPath {
  return {
    id,
    title,
    tier,
    sector,
    domain,
    shortDescription,
    eligibility: {
      educationRequired: minEducationLevel === "12TH" 
        ? "Class 12th Pass (10+2) from a recognized Board"
        : minEducationLevel === "DIPLOMA"
        ? "3-Year Engineering/Technical Diploma"
        : minEducationLevel === "POST_GRADUATE"
        ? "Master's Degree / Post Graduation in relevant discipline"
        : "Graduation degree in any discipline from a recognized University",
      minEducationLevel,
      ageLimit: {
        min: minAge,
        max: maxAge,
        relaxations: [
          { category: "OBC", yearsExtention: 3, notes: `Max age ${maxAge + 3}` },
          { category: "SC", yearsExtention: 5, notes: `Max age ${maxAge + 5}` },
          { category: "ST", yearsExtention: 5, notes: `Max age ${maxAge + 5}` },
          { category: "PWD", yearsExtention: 10, notes: `Max age ${maxAge + 10}` }
        ]
      }
    },
    competitionStats: {
      applicants,
      seats,
      ratio: `1 : ${Math.max(1, Math.round(applicants / seats))}`,
      lastUpdated: "2025-2026 Recruitment Standard",
      difficultyRating
    },
    roadmapSteps: steps.map((s, idx) => ({
      stepNumber: idx + 1,
      title: s.title,
      description: s.description,
      estimatedDuration: s.estimatedDuration || "2-3 Months"
    })),
    salaryRange: {
      min: minSalaryPM,
      max: maxSalaryPM,
      currency: "INR",
      payScaleCode
    },
    applicationPortalUrl,
    sources: [
      { title: `${title} Official Portal`, url: applicationPortalUrl }
    ],
    stateSpecific: null,
    examTimeline: {
      notificationMonth,
      examMonth,
      frequency: "Annual Cycle",
      applicationFee: sector === "GOVT" ? "₹100 (Exempted for SC/ST/Women)" : "Free"
    },
    growthProspects,
    tags
  };
}

// 50 ELITE CAREERS
const ELITE_CAREERS: CareerPath[] = [
  createCareer("upsc-cse", "UPSC Civil Services (IAS / IPS / IFS)", "ELITE", "GOVT", "Civil Services & Public Admin", "Premier executive service governing District Administration, Foreign Policy, and Public Security.", "GRADUATE", 21, 32, 75000, 250000, "Pay Level 10 (7th CPC) + DA, HRA, Residence", "https://upsc.gov.in", "February", "May / Sep", "SDM ➔ District Collector (DM) ➔ Tehsildar/Commissioner ➔ State Principal Secretary ➔ Union Cabinet Secretary", [
    { title: "NCERTs & Core GS", description: "Master History, Polity, Geography, and Economics foundational NCERTs." },
    { title: "Standard Textbooks & Optional", description: "Cover Laxmikanth, Spectrum, and optional subject syllabus." },
    { title: "Prelims & Mains Practice", description: "Solve mock tests, daily answer writing, and current affairs analysis." },
    { title: "Personality Test", description: "Interview prep with DAF analysis and mock panels." }
  ], ["Bureaucracy", "High Prestige", "Pan-India"], 1100000, 1000, "EXTREME"),

  createCareer("rbi-grade-b", "Reserve Bank of India (RBI) Grade B Officer", "ELITE", "GOVT", "Banking & Financial Services", "Central banker managing macroeconomic stability, monetary policy, and inflation targets.", "GRADUATE", 21, 30, 110000, 160000, "Gross CTC ~₹28-30 LPA with Metro Housing", "https://rbi.org.in", "July", "September", "Assistant Manager ➔ Manager ➔ Chief General Manager ➔ Executive Director ➔ Deputy Governor", [
    { title: "Phase-1 Speed & Aptitude", description: "Master Quantitative Aptitude, Reasoning, and General Awareness." },
    { title: "Phase-2 ESI & Finance", description: "Study Union Budget, Economic Survey, and Financial Management." },
    { title: "Interview & Typing", description: "Descriptive paper practice and central banking interview prep." }
  ], ["Central Bank", "High CTC", "Finance"], 250000, 300, "VERY_HIGH"),

  createCareer("isro-scientist-sc", "ISRO Scientist / Engineer 'SC'", "ELITE", "GOVT", "Science, Space & Aerospace R&D", "Design satellite launchers, space missions (Chandrayaan/Gaganyaan), and aerospace systems.", "GRADUATE", 21, 28, 85000, 140000, "Pay Level 10 (7th CPC) + Space Allowance", "https://isro.gov.in", "December", "March", "Scientist SC ➔ Scientist SD ➔ Group Director ➔ Outstanding Scientist ➔ ISRO Chairman", [
    { title: "GATE Level Core Engineering", description: "Master Mechanical/Aerospace/ECE/CS core concepts." },
    { title: "ISRO Written Exam", description: "Solve previous year technical papers and speed tests." },
    { title: "Domain Interview", description: "In-depth panel interview on final year projects and core theory." }
  ], ["Space Science", "R&D", "Prestige"], 120000, 300, "VERY_HIGH"),

  createCareer("drdo-scientist-b", "DRDO Scientist 'B' (RAC)", "ELITE", "GOVT", "Defence Technology & R&D", "Develop advanced missile systems, radar networks, drones, and electronic warfare for Defence.", "GRADUATE", 21, 28, 85000, 140000, "Pay Level 10 (7th CPC)", "https://rac.gov.in", "May", "July", "Scientist B ➔ Scientist C/D ➔ Scientist G ➔ Distinguished Scientist / Director General DRDO", [
    { title: "GATE Qualification", description: "Secure high percentile score in relevant engineering paper." },
    { title: "Descriptive Exam / Presentation", description: "Present research topic and solve advanced technical papers." },
    { title: "RAC Selection Interview", description: "Defend project proposal before Senior DRDO Directors." }
  ], ["Defence R&D", "Tech", "Security"], 90000, 250, "VERY_HIGH"),

  createCareer("sebi-grade-a", "SEBI Grade A Assistant Manager", "ELITE", "GOVT", "Capital Markets & Finance", "Regulate stock exchanges, mutual funds, IPOs, and financial market integrity.", "GRADUATE", 21, 30, 105000, 150000, "Gross CTC ~₹24 LPA including Perks", "https://sebi.gov.in", "June", "August", "Assistant Manager ➔ Manager ➔ Chief General Manager ➔ Executive Director SEBI", [
    { title: "Phase-1 Screening", description: "General Awareness, Aptitude, English, and basic commerce." },
    { title: "Phase-2 Securities Market", description: "Master Corporate Law, Costing, Accountancy, and Economics." },
    { title: "Phase-3 Interview", description: "Financial market trends and regulatory case studies." }
  ], ["Capital Markets", "High Salary", "Regulation"], 150000, 120, "VERY_HIGH"),

  createCareer("upsc-ese", "UPSC Engineering Services (IES)", "ELITE", "GOVT", "Core Engineering Services", "Technical executive leading CPWD, Indian Railway Engineers, Defence Engineers & Power Sector.", "GRADUATE", 21, 30, 80000, 180000, "Pay Level 10 (7th CPC) Executive Cadre", "https://upsc.gov.in", "September", "February / June", "Assistant Executive Engineer ➔ Executive Engineer ➔ Chief Engineer ➔ Member Railway Board", [
    { title: "Stage-1 Prelims Objective", description: "General Studies & Engineering Aptitude + Technical Paper." },
    { title: "Stage-2 Mains Conventional", description: "Two descriptive conventional papers in Civil/Mech/EE/ECE." },
    { title: "Stage-3 Personality Test", description: "Technical and managerial interview at UPSC House." }
  ], ["Engineering Leadership", "CPWD", "Railways"], 200000, 400, "EXTREME"),

  createCareer("nda-cds-officer", "NDA / CDS Officer (Indian Army/Navy/Air Force)", "ELITE", "GOVT", "Defence, Police & Security", "Commissioned Officer leading combat units, fighter squadrons, and naval warships.", "GRADUATE", 19, 24, 85000, 220000, "Pay Level 10 (7th CPC) + Flying/Hardship Allowance", "https://upsc.gov.in", "June / December", "April / September", "Lieutenant / Flying Officer ➔ Captain / Flight Lt ➔ Colonel ➔ Major General ➔ Chief of Staff", [
    { title: "UPSC Written Exam", description: "Mathematics, English, and General Knowledge competitive paper." },
    { title: "5-Day SSB Interview", description: "Psychological tests, Group Tasks (GTO), and Officer Qualities (OLQs)." },
    { title: "Medical Board & Academy", description: "Strict military medicals followed by IMA/AFA/NA training." }
  ], ["Military Commission", "Patriotism", "Leadership"], 400000, 600, "EXTREME"),

  createCareer("barc-scientific-officer", "BARC Scientific Officer (OCES / DGFS)", "ELITE", "GOVT", "Nuclear Energy & Physics R&D", "Conduct nuclear research, reactor design, particle physics, and radiochemistry.", "GRADUATE", 21, 26, 85000, 140000, "Pay Level 10 + Nuclear Incentive", "https://barcoces.gov.in", "January", "March", "Scientific Officer C ➔ SO D/E/F ➔ Outstanding Scientist BARC", [
    { title: "Written Exam / GATE Score", description: "Qualify BARC CBT or submit top 100 GATE rank." },
    { title: "In-Depth Technical Interview", description: "Rigorous 1-hour interview testing fundamental science/engineering." }
  ], ["Atomic Research", "High Science", "Prestige"], 80000, 150, "EXTREME"),

  createCareer("nabard-grade-a", "NABARD Grade A Assistant Manager", "ELITE", "GOVT", "Rural Banking & Agriculture", "Drive rural infrastructure financing, agriculture credit policy, and NABARD development schemes.", "GRADUATE", 21, 30, 90000, 130000, "Gross CTC ~₹20 LPA", "https://nabard.org", "August", "October", "Assistant Manager ➔ Manager ➔ Chief General Manager ➔ Director", [
    { title: "Phase-1 Preliminary", description: "Agriculture & Rural Development (ARD), ESI, Reasoning, Quant." },
    { title: "Phase-2 Main Exam", description: "Descriptive ESI, ARD, and General English." },
    { title: "Phase-3 Interview", description: "Rural economy and banking interview." }
  ], ["Rural Finance", "Good Work Life", "Development"], 120000, 150, "HIGH"),

  createCareer("psu-management-trainee", "PSU Management Trainee via GATE (IOCL/ONGC/NTPC)", "ELITE", "GOVT", "PSUs & Energy Sector", "Manage oil refineries, power grids, natural gas pipelines, and heavy industrial plants.", "GRADUATE", 21, 28, 90000, 160000, "Pay Scale ₹60,000–1,80,000 (Gross CTC ₹18-24 LPA)", "https://gate2026.iit.ac.in", "September (GATE)", "February", "Executive MT ➔ Senior Manager ➔ General Manager ➔ Executive Director / PSU Director", [
    { title: "GATE Exam Mastery", description: "Score top 200 AIR in Civil/Mech/EE/ECE/CS GATE paper." },
    { title: "Group Discussion & Task", description: "Participate in PSU GD/GDT leadership challenges." },
    { title: "Personal Interview", description: "Technical and HR interview with Maharatna panel." }
  ], ["Maharatna PSU", "High CTC", "Core Tech"], 150000, 1500, "VERY_HIGH"),

  createCareer("aai-atco", "Air Traffic Control Officer (AAI ATCO)", "ELITE", "GOVT", "Aviation & Aerospace", "Direct civilian air traffic, flight paths, radar vectoring, and airport runway operations.", "GRADUATE", 21, 27, 85000, 150000, "Pay Level 8 (7th CPC) + Stress/Rating Allowance (~₹18 LPA)", "https://aai.aero", "November", "January", "Junior Executive ATCO ➔ Assistant General Manager ➔ Executive Director AAI", [
    { title: "Written CBT Exam", description: "Physics & Mathematics (12th standard) + Aptitude/English." },
    { title: "Voice & Medical Test", description: "Voice clarity test and Class-3 aviation medical standards." }
  ], ["Aviation", "High Pay", "Radar Operations"], 180000, 400, "HIGH"),

  createCareer("civil-judge-junior", "Civil Judge Junior Division (State Judicial Services)", "ELITE", "GOVT", "Legal, Judiciary & Rights", "Preside over civil and criminal court trials, deliver judgements, and enforce rule of law.", "GRADUATE", 21, 35, 80000, 180000, "Judicial Pay Scale + Official Car & Security", "https://highcourt.gov.in", "Varies by State", "Annual/Regular", "Civil Judge Jr ➔ Senior Civil Judge ➔ District & Sessions Judge ➔ High Court Judge", [
    { title: "Judicial Services Prelims", description: "Constitutional Law, IPC, CrPC, CPC, Evidence Act objective exam." },
    { title: "Judicial Mains Exam", description: "Descriptive legal writing, judgment writing, and local statutes." },
    { title: "Viva-Voce / Interview", description: "Legal ethics and judicial temperament panel interview." }
  ], ["Judiciary", "Magistrate", "High Authority"], 90000, 200, "EXTREME"),

  createCareer("tier1-sde3", "Staff Software Engineer / SDE-3 (Top MNCs: Google/Microsoft)", "ELITE", "PRIVATE", "Software Engineering & IT", "Architect large-scale distributed systems, cloud backends, microservices, and AI features.", "GRADUATE", 21, 45, 150000, 450000, "Total Compensation ₹35 LPA – ₹1.2 Cr PA (Salary + RSUs)", "https://careers.google.com", "Rolling", "Continuous", "SDE-1 ➔ Senior SDE ➔ Staff Engineer ➔ Principal Architect ➔ VP of Engineering", [
    { title: "Data Structures & Algorithms", description: "Solve LeetCode Hard problems in Graphs, Trees, Dynamic Programming." },
    { title: "System Design (HLD & LLD)", description: "Architect Scalable Distributed Queues, Caching, Databases." },
    { title: "Behavioral & Leadership", description: "Demonstrate technical leadership, cross-team impact, and code reviews." }
  ], ["High Compensation", "Cloud & AI", "Tech MNC"], 300000, 2000, "EXTREME"),

  createCareer("quant-researcher", "Quant Researcher / High Frequency Trader", "ELITE", "PRIVATE", "Finance, Fintech & Analytics", "Develop mathematical models, statistical arbitrage algorithms, and market making strategies.", "GRADUATE", 21, 35, 200000, 600000, "Starting CTC ₹40 LPA – ₹1.5 Cr (Base + Performance Bonus)", "https://quantinsti.com", "Rolling", "Continuous", "Junior Quant ➔ Lead Quant Researcher ➔ Portfolio Manager / Hedge Fund Partner", [
    { title: "Advanced Probability & Stats", description: "Master Stochastic Calculus, Linear Algebra, and Time Series." },
    { title: "C++ / Python Performance Coding", description: "Optimize low-latency algorithmic trading engines." },
    { title: "Brainteasers & Math Contests", description: "Solve complex combinatorics and probability puzzles." }
  ], ["Highest CTC", "Quant Math", "Algorithmic Trading"], 20000, 100, "EXTREME"),

  createCareer("management-consultant-mbb", "Management Consultant (McKinsey / BCG / Bain)", "ELITE", "PRIVATE", "Management, Strategy & Business", "Advise CEOs and governments on corporate restructuring, growth strategy, and digital pivot.", "GRADUATE", 21, 35, 150000, 350000, "CTC ₹25 - 50 LPA + Performance Bonus", "https://mckinsey.com/careers", "August", "October", "Business Analyst ➔ Associate ➔ Engagement Manager ➔ Partner / Managing Director", [
    { title: "Case Interview Mastery", description: "Practice 50+ profitability, market entry, and estimation case studies." },
    { title: "Problem Solving & Structuring", description: "Structure complex unstructured business dilemmas logically." },
    { title: "Executive Communication", description: "Deliver compelling slide decks and client pitch presentations." }
  ], ["Corporate Strategy", "High Travel", "C-Suite Advisory"], 50000, 300, "EXTREME"),

  createCareer("investment-banker-m-and-a", "Investment Banking Associate (M&A / Capital Markets)", "ELITE", "PRIVATE", "Banking & Financial Services", "Structure mega mergers, acquisitions, IPOs, and debt syndications for Fortune 500 firms.", "GRADUATE", 21, 35, 140000, 320000, "CTC ₹28 - 60 LPA (Base + Bonus)", "https://goldmansachs.com/careers", "September", "November", "Analyst ➔ Associate ➔ Vice President ➔ Managing Director Investment Banking", [
    { title: "Financial Modeling (DCF / LBO)", description: "Build 3-statement financial models and valuation matrices." },
    { title: "Deal Structuring & Term Sheets", description: "Analyze M&A synergies, due diligence reports, and regulatory filings." },
    { title: "Pitchbook Creation", description: "Draft executive deal decks for corporate clients." }
  ], ["Wall Street / Dalal St", "Wall Street CTC", "High Pace"], 40000, 200, "EXTREME"),

  createCareer("product-manager-tier1", "Senior Product Manager (Product MNC / Tech Unicorn)", "ELITE", "PRIVATE", "Design, Product & Creative Arts", "Define product vision, user metrics, feature roadmaps, and monetization for flagship apps.", "GRADUATE", 21, 40, 120000, 300000, "CTC ₹25 - 55 LPA (Salary + Stock Options)", "https://linkedin.com", "Rolling", "Continuous", "APM ➔ Product Manager ➔ Senior PM ➔ Group PM ➔ VP of Product", [
    { title: "Product Sense & User Psychology", description: "Solve product teardowns, design user journeys, and define MVP." },
    { title: "Metrics & A/B Testing", description: "Master cohort analysis, funnel retention, and data-driven decisions." },
    { title: "Cross-Functional Execution", description: "Align Engineering, Design, and Marketing around product milestones." }
  ], ["Product Vision", "High Impact", "Tech Leadership"], 80000, 1000, "VERY_HIGH"),

  createCareer("corporate-lawyer-sam-cam", "Corporate M&A Lawyer (Tier-1 Law Firms: SAM / CAM)", "ELITE", "PRIVATE", "Legal, Judiciary & Rights", "Draft cross-border contracts, antitrust clearances, corporate governance, and venture deals.", "GRADUATE", 21, 35, 120000, 280000, "CTC ₹18 - 35 LPA Starting for NLU Graduates", "https://amarchand.com", "March", "June", "Junior Associate ➔ Senior Associate ➔ Principal Associate ➔ Equity Partner", [
    { title: "Corporate & Securities Law", description: "Master Companies Act 2013, SEBI Regulations, and Insolvency Code." },
    { title: "Contract Drafting & Negotiation", description: "Draft Share Purchase Agreements (SPA) and Term Sheets." },
    { title: "Due Diligence Audits", description: "Review corporate filings and compliance records for acquisitions." }
  ], ["Legal Partner", "High Retainer", "Tier 1 Law"], 30000, 300, "EXTREME"),

  createCareer("ai-research-scientist", "AI / Deep Learning Research Scientist", "ELITE", "PRIVATE", "AI, Data Science & Analytics", "Train state-of-the-art Large Language Models (LLMs), Computer Vision, and Robotics AI.", "POST_GRADUATE", 22, 40, 140000, 400000, "CTC ₹30 - 90 LPA", "https://deepmind.google", "Rolling", "Continuous", "Research Associate ➔ AI Scientist ➔ Senior AI Researcher ➔ Head of AI Labs", [
    { title: "PyTorch / CUDA Mastery", description: "Implement transformer architectures and parallel GPU training." },
    { title: "Top AI Paper Publications", description: "Publish papers in NeurIPS, CVPR, or ICML conferences." },
    { title: "Model Alignment & Fine-tuning", description: "Optimize RLHF, LoRA, and quantization pipelines." }
  ], ["Generative AI", "Cutting Edge", "High R&D"], 25000, 200, "EXTREME"),

  createCareer("upsc-ifs-foreign", "Indian Foreign Service (IFS) Diplomat", "ELITE", "GOVT", "Civil Services & Public Admin", "Represent India at United Nations, international summits, and foreign embassies worldwide.", "GRADUATE", 21, 32, 100000, 280000, "Pay Level 10 + Foreign Allowance (Tax-free overseas compensation)", "https://mea.gov.in", "February", "May", "Third Secretary ➔ Second/First Secretary ➔ Consul General ➔ Ambassador / High Commissioner", [
    { title: "UPSC CSE All-India Rank top 100", description: "Secure top rank to get allocated Indian Foreign Service." },
    { title: "Foreign Language Training", description: "Master designated compulsory foreign language (Mandarin, French, Russian, Arabic, Spanish)." },
    { title: "Diplomatic Protocol", description: "Undergo Sushma Swaraj Institute of Foreign Service orientation." }
  ], ["Global Diplomacy", "Embassy Life", "High Prestige"], 1100000, 35, "EXTREME"),

  createCareer("commercial-pilot-dgca", "Commercial Airline Pilot (Commander)", "ELITE", "PRIVATE", "Aviation & Aerospace", "Command passenger jets (Boeing 737 / Airbus A320) across domestic and international routes.", "12TH", 18, 32, 150000, 500000, "Starting Salary ₹1.8 LPA ➔ Commander ₹5-8 LPA", "https://dgca.gov.in", "Rolling", "Continuous", "Junior First Officer ➔ Senior First Officer ➔ Captain / Commander ➔ Type Rating Instructor", [
    { title: "DGCA Ground Exams", description: "Pass Air Navigation, Aviation Meteorology, Air Regulations, and Technical." },
    { title: "Flying Training (200 Hours)", description: "Obtain Commercial Pilot License (CPL) from certified flying school." },
    { title: "Type Rating & Airline Simulator", description: "Complete Airbus/Boeing type rating and line training." }
  ], ["Aviation", "High Pay", "Global Travel"], 15000, 500, "VERY_HIGH"),

  createCareer("super-specialist-doctor", "Super Specialist Doctor (DM / MCh - AIIMS)", "ELITE", "GOVT", "Medical, Nursing & Healthcare", "Perform neurosurgeries, organ transplants, and advanced cardiac interventional procedures.", "POST_GRADUATE", 25, 45, 120000, 350000, "Pay Level 11 + NPA (Non-Practicing Allowance)", "https://aiims.edu", "April", "June", "Senior Resident ➔ Assistant Professor ➔ Associate Professor ➔ Head of Department AIIMS", [
    { title: "MBBS + MD/MS Degree", description: "Clear NEET-UG, complete MBBS, and pass NEET-PG for Residency." },
    { title: "INI-SS / NEET-SS Entrance", description: "Score top rank for DM/MCh super-specialization seat." },
    { title: "Surgical / Clinical Fellowship", description: "Master specialized complex procedures during 3-year fellowship." }
  ], ["Super Specialist", "Lifesaving", "Highest Medical Rank"], 40000, 300, "EXTREME"),

  createCareer("ib-acio1", "Intelligence Bureau ACIO-I / Deputy Central Intelligence Officer", "ELITE", "GOVT", "Defence, Police & Security", "Lead counter-intelligence, national security surveillance, and threat assessment operations.", "GRADUATE", 21, 30, 80000, 150000, "Pay Level 10 + 20% Special Security Allowance", "https://mha.gov.in", "October", "December", "ACIO-I ➔ DCIO ➔ Assistant Director IB ➔ Joint Director IB", [
    { title: "Tier-1 Objective Exam", description: "Current Affairs, GS, Analytical Ability, and English." },
    { title: "Tier-2 Essay & Precis", description: "Descriptive writing on security challenges and geopolitical issues." },
    { title: "Psychometric & Interview", description: "In-depth background check and psychometric evaluation." }
  ], ["Intelligence", "Secret Service", "National Security"], 300000, 150, "VERY_HIGH"),

  createCareer("cbi-dsp", "CBI Deputy Superintendent of Police (DSP)", "ELITE", "GOVT", "Defence, Police & Security", "Investigate major economic offenses, high-profile corruption, and international crime cases.", "GRADUATE", 21, 30, 80000, 160000, "Pay Level 10 + Special Incentive Allowance", "https://cbi.gov.in", "February", "May", "DSP ➔ Additional SP ➔ Superintendent of Police (SP) ➔ Joint Director CBI", [
    { title: "UPSC CSE Rank or Direct Nomination", description: "Qualify Civil Services Exam or internal cadre promotion." },
    { title: "CBI Academy Training", description: "Undergo 1-year intensive training at CBI Academy Ghaziabad in Forensic & Cyber crime." }
  ], ["Premier Agency", "Anti-Corruption", "High Authority"], 1000000, 15, "EXTREME"),

  createCareer("state-psc-deputy-collector", "State PSC Deputy Collector / SDM (Group-A)", "ELITE", "GOVT", "Civil Services & Public Admin", "Head revenue administration, law and order, and land management in state sub-divisions.", "GRADUATE", 21, 35, 70000, 180000, "Pay Level 10 State Pay Matrix + Official Perks", "https://upsc.gov.in", "Varies by State", "Annual", "Deputy Collector ➔ Additional District Magistrate ➔ IAS Nomination ➔ District Magistrate", [
    { title: "State PSC Prelims", description: "State History, General Studies, and Aptitude test." },
    { title: "State PSC Mains", description: "Descriptive papers including State Language & Local Acts." },
    { title: "State Personality Test", description: "State PSC Board Interview." }
  ], ["State Executive", "SDM", "Local Power"], 500000, 50, "EXTREME"),

  createCareer("iim-prof", "Professor / Associate Professor (IITs / IIMs)", "ELITE", "GOVT", "Teaching & Academic Research", "Conduct high-impact research, publish in top journals, and teach MBA / B.Tech students.", "POST_GRADUATE", 28, 50, 110000, 240000, "Pay Level 12 / 14 (7th CPC) + Professional Development Grant", "https://iim.ac.in", "Rolling", "Continuous", "Assistant Professor ➔ Associate Professor ➔ Chair Professor ➔ Director IIM/IIT", [
    { title: "Ph.D. from Reputed Institute", description: "Complete doctoral research with top peer-reviewed journal papers." },
    { title: "Post-Doctoral / Industry Experience", description: "3+ years post-PhD research or consultancy experience." },
    { title: "Research Seminar & Panel Interview", description: "Deliver research presentation to Faculty Selection Committee." }
  ], ["Academic Elite", "High Freedom", "Consulting Income"], 20000, 100, "VERY_HIGH"),

  createCareer("actuary-iai", "Fellow Actuary (Institute of Actuaries of India)", "ELITE", "PRIVATE", "Finance, Fintech & Analytics", "Calculate risk probabilities, insurance premiums, pension liabilities, and financial reserves.", "GRADUATE", 18, 45, 120000, 350000, "Starting Salary ₹12 LPA ➔ Fellow Actuary ₹30 - 70 LPA", "https://actuariesindia.org", "Rolling", "Bi-annual", "Student Actuary ➔ Associate ➔ Fellow Actuary ➔ Chief Actuary / Chief Risk Officer", [
    { title: "ACET Entrance Exam", description: "Pass Actuarial Common Entrance Test in Math & Stats." },
    { title: "13 Professional Actuarial Exams", description: "Pass Core Principles, Core Practices, and Specialist Applications modules." },
    { title: "Practical Work Experience", description: "3 years mentored actuarial experience in Insurance/Reinsurance." }
  ], ["High Math", "Rare Skill", "Top Financial Pay"], 15000, 50, "EXTREME"),

  createCareer("chief-data-scientist", "Chief Data Scientist / AI Architect", "ELITE", "PRIVATE", "AI, Data Science & Analytics", "Lead enterprise data strategy, predictive analytics engines, and AI deployment across markets.", "POST_GRADUATE", 25, 50, 160000, 450000, "CTC ₹35 - 90 LPA", "https://linkedin.com", "Rolling", "Continuous", "Senior Data Scientist ➔ Lead Data Scientist ➔ Principal Architect ➔ Chief Data Officer", [
    { title: "Machine Learning Engineering", description: "Master Python, Distributed Spark, MLOps, and Cloud Data Warehouses." },
    { title: "Business & Predictive Strategy", description: "Convert business metrics into ML model loss functions." }
  ], ["Big Data", "Executive Tech", "High Growth"], 40000, 200, "VERY_HIGH"),

  createCareer("cloud-enterprise-architect", "Principal Cloud Solutions Architect", "ELITE", "PRIVATE", "Software Engineering & IT", "Design multi-cloud resilience, zero-trust infrastructure, and enterprise DevOps pipelines.", "GRADUATE", 22, 48, 140000, 380000, "CTC ₹30 - 75 LPA", "https://aws.amazon.com/careers", "Rolling", "Continuous", "Cloud Engineer ➔ Solutions Architect ➔ Principal Architect ➔ VP Infrastructure", [
    { title: "AWS / Azure / GCP Professional Certs", description: "Clear Solutions Architect Professional & Security Specialty exams." },
    { title: "Infrastructure as Code & Kubernetes", description: "Master Terraform, EKS/AKS, Service Mesh, and FinOps." }
  ], ["Cloud Leader", "AWS / Azure", "High Demand"], 60000, 500, "HIGH"),

  createCareer("marine-chief-engineer", "Marine Chief Engineer / Captain (Merchant Navy)", "ELITE", "PRIVATE", "Core Engineering Services", "Command giant cargo vessels, oil tankers, and container ships across international ocean routes.", "GRADUATE", 21, 45, 200000, 550000, "Monthly Salary $6,000 – $12,000 USD (Tax-Free in India)", "https://dgshipping.gov.in", "Rolling", "Continuous", "4th Engineer ➔ 2nd Engineer ➔ Chief Engineer / Master Mariner", [
    { title: "B.Sc Nautical Science / Marine Engg", description: "Complete DG Shipping approved maritime degree." },
    { title: "Sea Time & MMD Competency Exams", description: "Accumulate required sea-time months and pass Class-1 MMD oral/written exams." }
  ], ["Tax Free Pay", "Global Seas", "Merchant Navy"], 10000, 300, "VERY_HIGH"),

  createCareer("merchant-navy-captain", "Master Mariner / Ship Captain", "ELITE", "PRIVATE", "Core Engineering Services", "Ultimate authority responsible for vessel navigation, crew safety, and maritime cargo operations.", "GRADUATE", 22, 50, 250000, 600000, "Monthly Salary $8,000 – $14,000 USD (Tax-Free)", "https://dgshipping.gov.in", "Rolling", "Continuous", "3rd Officer ➔ Chief Officer ➔ Master Mariner (Captain)", [
    { title: "Deck Cadetship & Sea Training", description: "Complete 18-36 months mandatory sea-time on commercial vessels." },
    { title: "Master Mariner Certificate of Competency", description: "Pass MMD Class-1 Master Mariner written & oral board." }
  ], ["High Commander", "Ocean Captain", "Tax Free USD"], 8000, 200, "EXTREME"),

  createCareer("rebit-systems-architect", "ReBIT Senior Systems Architect (Reserve Bank Tech)", "ELITE", "GOVT", "Banking & Financial Services", "Design secure banking infrastructure, UPI/NEFT cyber resilience, and financial tech systems.", "GRADUATE", 22, 40, 110000, 200000, "Gross CTC ₹22 - 38 LPA", "https://rebit.org.in", "Rolling", "Continuous", "Software Engineer ➔ Tech Lead ➔ Principal Architect ➔ Director ReBIT", [
    { title: "Cybersecurity & Cloud Systems", description: "Master PCI-DSS, ISO 27001, banking API gateways, and threat mitigation." },
    { title: "Technical Evaluation & Interview", description: "Solve architectural whiteboarding challenge before ReBIT board." }
  ], ["Fintech Security", "RBI Subsidiary", "High Compensation"], 20000, 50, "HIGH"),

  createCareer("powergrid-engineer-trainee", "POWERGRID Executive Engineer Trainee via GATE", "ELITE", "GOVT", "PSUs & Energy Sector", "Manage national high-voltage transmission grids and renewable energy corridors.", "GRADUATE", 21, 28, 85000, 150000, "Pay Scale ₹60,000–1,80,000 (CTC ~₹18 LPA)", "https://powergrid.in", "October", "February", "Executive Trainee ➔ Manager ➔ General Manager ➔ Director Operations", [
    { title: "GATE EE/ECE/Civil Score", description: "Secure top rank in GATE exam." },
    { title: "GD & Personal Interview", description: "Group task and technical interview on power systems." }
  ], ["Navratna PSU", "Power Grid", "High Stability"], 100000, 300, "VERY_HIGH"),

  createCareer("hal-design-engineer", "HAL Aircraft Design Engineer (Hindustan Aeronautics)", "ELITE", "GOVT", "Science, Space & Aerospace R&D", "Design combat aircraft (Tejas LCA, AMCA) and military helicopters for Indian Air Force.", "GRADUATE", 21, 28, 80000, 140000, "Pay Scale ₹40,000–1,40,000 (CTC ~₹15 LPA)", "https://hal-india.co.in", "May", "July", "Design Engineer ➔ Chief Designer ➔ General Manager ➔ Board Director HAL", [
    { title: "GATE / HAL Written Test", description: "Qualify technical exam in Aeronautical/Mechanical/ECE." },
    { title: "Design Portfolio & Interview", description: "Defend aerodynamics, propulsion, or avionics design projects." }
  ], ["Aerospace R&D", "Military Aviation", "Defence"], 70000, 120, "VERY_HIGH"),

  createCareer("bel-probationary-engineer", "BEL Probationary Engineer (Bharat Electronics)", "ELITE", "GOVT", "Defence Technology & R&D", "Develop naval radars, missile guidance systems, EVMs, and night-vision defence electronics.", "GRADUATE", 21, 25, 80000, 140000, "Pay Scale ₹40,000–1,40,000 (CTC ~₹14 LPA)", "https://bel-india.in", "February", "April", "Probationary Engineer ➔ Senior Engineer ➔ General Manager ➔ Director BEL", [
    { title: "Written CBT Exam", description: "Electronics/Computer Science core engineering test." },
    { title: "Technical Panel Interview", description: "In-depth testing on signals, embedded systems, and communications." }
  ], ["Navratna PSU", "Defence Electronics", "High Stability"], 90000, 200, "HIGH"),

  createCareer("gail-executive-trainee", "GAIL Executive Trainee (Gas Authority of India)", "ELITE", "GOVT", "PSUs & Energy Sector", "Operate cross-country natural gas pipelines, petrochemical plants, and green hydrogen projects.", "GRADUATE", 21, 28, 90000, 160000, "Pay Scale ₹60,000–1,80,000 (CTC ~₹18 LPA)", "https://gailonline.com", "December", "February", "Executive Trainee ➔ Senior Manager ➔ General Manager ➔ Executive Director GAIL", [
    { title: "GATE Chemical/Mechanical/EE Score", description: "Qualify GATE with high AIR rank." },
    { title: "Group Discussion & Interview", description: "Participate in GAIL executive selection rounds." }
  ], ["Maharatna PSU", "Energy Sector", "Top CTC"], 80000, 100, "VERY_HIGH"),

  createCareer("high-court-law-clerk", "High Court / Supreme Court Law Clerk", "ELITE", "GOVT", "Legal, Judiciary & Rights", "Assist Supreme Court / High Court Justices in legal research, case summaries, and decree drafting.", "GRADUATE", 21, 30, 80000, 120000, "Fixed Judicial Stipend ₹80,000 - ₹1,00,000 / month", "https://main.sci.gov.in", "May", "July", "Law Clerk ➔ Advocate on Record / Judicial Services Magistrate / Senior Partner", [
    { title: "LL.B Degree with High Distinction", description: "Graduate from recognized law university." },
    { title: "Judicial Research Exam", description: "Pass Constitutional Law written test & judgment analysis." },
    { title: "Judge Panel Interview", description: "Interview with Sitting High Court / Supreme Court Justices." }
  ], ["Judicial Access", "Top Mentorship", "Legal Honor"], 20000, 80, "HIGH"),

  createCareer("equity-portfolio-manager", "SEBI Registered Portfolio Manager (PMS Lead)", "ELITE", "PRIVATE", "Capital Markets & Finance", "Manage equity portfolios, mutual funds, and wealth assets for high net-worth individuals.", "GRADUATE", 21, 45, 140000, 400000, "CTC ₹25 - 80 LPA + Performance Fee Share", "https://nism.ac.in", "Rolling", "Continuous", "Research Analyst ➔ Assistant Fund Manager ➔ Portfolio Manager ➔ Chief Investment Officer", [
    { title: "CFA / NISM Series XV Certification", description: "Complete Chartered Financial Analyst levels or NISM PMS exam." },
    { title: "Equity Research Track Record", description: "Demonstrate multi-year alpha generation in stock picking." }
  ], ["Wealth Management", "High Pay", "Wall Street"], 25000, 100, "VERY_HIGH"),

  createCareer("medical-officer-cas", "Civil Assistant Surgeon / Medical Officer (State Health)", "ELITE", "GOVT", "Medical, Nursing & Healthcare", "Head primary/district healthcare centers, manage epidemic response, and emergency medicine.", "GRADUATE", 22, 42, 80000, 160000, "Pay Level 10 + Non-Practicing Allowance (NPA)", "https://health.gov.in", "Varies by State", "Annual", "Medical Officer ➔ Senior Medical Officer ➔ Chief Medical Officer (CMO) ➔ Director Health Services", [
    { title: "MBBS Degree & Internship", description: "Complete 4.5 year MBBS + 1 year compulsory internship." },
    { title: "State Medical Council Registration", description: "Register with State Medical Council / NMC." },
    { title: "Medical Services Exam / Recruitment", description: "Qualify State Public Service Commission Medical Officer test." }
  ], ["Healthcare Authority", "CMO Cadre", "Social Good"], 50000, 1000, "HIGH"),

  createCareer("drdo-project-director", "Defence Project Director / Chief Scientist", "ELITE", "GOVT", "Defence Technology & R&D", "Lead secret national defence projects in hypersonic missiles, stealth drones, and radars.", "POST_GRADUATE", 30, 50, 130000, 250000, "Pay Level 13A / 14 (7th CPC)", "https://drdo.gov.in", "Internal", "Promotional", "Scientist D/E ➔ Project Director ➔ Distinguished Scientist", [
    { title: "15+ Years Defence R&D Record", description: "Lead successful defence technology deployments." }
  ], ["National Security", "Top R&D", "Prestige"], 5000, 20, "EXTREME"),

  createCareer("supreme-court-aor", "Supreme Court Advocate-on-Record (AoR)", "ELITE", "PRIVATE", "Legal, Judiciary & Rights", "Exclusive constitutional authority entitled to file pleadings and represent matters in Supreme Court of India.", "GRADUATE", 25, 50, 150000, 500000, "Professional Fee ₹1.5 Lakh – ₹10 Lakhs per appearance", "https://main.sci.gov.in", "April", "June", "Advocate ➔ Advocate-on-Record ➔ Senior Advocate Supreme Court", [
    { title: "4 Years Practice + 1 Year AoR Training", description: "Complete mandatory legal practice and training under senior AoR." },
    { title: "Supreme Court AoR Examination", description: "Pass rigorous 4-paper exam in SC Practice, Drafting, Ethics, & Leading Cases." }
  ], ["Highest Bar", "Supreme Court", "Elite Legal"], 5000, 30, "EXTREME"),

  createCareer("isro-space-ops-lead", "ISRO Mission Operations Director", "ELITE", "GOVT", "Science, Space & Aerospace R&D", "Lead real-time telemetry, trajectory control, and countdown command for satellite and rocket launches.", "GRADUATE", 28, 50, 120000, 220000, "Pay Level 13 / 14 (7th CPC)", "https://isro.gov.in", "Internal", "Promotional", "Scientist SC/SD ➔ Operations Manager ➔ Mission Director", [
    { title: "10+ Years Space Mission Experience", description: "Track record in satellite ground stations and rocket launch tracking." }
  ], ["Space Missions", "Chandrayaan", "National Honor"], 2000, 10, "EXTREME"),

  createCareer("coast-guard-commandant", "Indian Coast Guard Assistant Commandant", "ELITE", "GOVT", "Defence, Police & Security", "Command offshore patrol vessels, search & rescue, anti-smuggling, and marine environmental defense.", "GRADUATE", 21, 25, 80000, 180000, "Pay Level 10 + Coast Guard Allowance", "https://joinindiancoastguard.cdac.in", "May / November", "July / Jan", "Assistant Commandant ➔ Deputy Commandant ➔ Commandant ➔ Inspector General Coast Guard", [
    { title: "CGCAT Written Exam", description: "Pass Coast Guard Common Admission Test." },
    { title: "Preliminary & Final Selection Board", description: "Mental aptitude, group tasks, and psychological interview." }
  ], ["Maritime Defence", "Naval Captain", "High Adventure"], 80000, 100, "VERY_HIGH"),

  createCareer("upsc-ies-economics", "UPSC Indian Economic Service (IES) Officer", "ELITE", "GOVT", "Civil Services & Public Admin", "Provide economic advice to Union Cabinet, analyze GDP trends, and draft national trade policies.", "POST_GRADUATE", 21, 30, 80000, 220000, "Pay Level 10 Cadre Service", "https://upsc.gov.in", "April", "July", "Assistant Director ➔ Deputy Director ➔ Chief Economic Adviser / Senior Economic Adviser", [
    { title: "Master's Degree in Economics / Finance", description: "Post Graduation in Economics/Applied Economics from recognized University." },
    { title: "UPSC IES Written Examination", description: "Pass General English, GS, and 4 specialized Economics papers." },
    { title: "Personality Test", description: "Interview at UPSC Board." }
  ], ["Economic Policy", "Ministry of Finance", "High Authority"], 30000, 20, "EXTREME"),

  createCareer("upsc-iss-statistics", "UPSC Indian Statistical Service (ISS) Officer", "ELITE", "GOVT", "Civil Services & Public Admin", "Lead NSO, census data analytics, national sample surveys, and data governance for Union Ministries.", "GRADUATE", 21, 30, 80000, 220000, "Pay Level 10 Cadre Service", "https://upsc.gov.in", "April", "July", "Assistant Director ➔ Director NSO ➔ Director General Statistics", [
    { title: "Bachelor's/Master's in Statistics / Math", description: "Degree with Statistics as major subject." },
    { title: "UPSC ISS Written Exam", description: "Pass General English, GS, and 4 Statistics objective/descriptive papers." }
  ], ["Data Governance", "National Statistics", "Prestige"], 25000, 30, "EXTREME"),

  createCareer("oil-india-executive", "Oil India Limited (OIL) Executive Officer", "ELITE", "GOVT", "PSUs & Energy Sector", "Lead upstream oil exploration, offshore drilling rigs, and petroleum reservoir engineering.", "GRADUATE", 21, 28, 85000, 160000, "Pay Scale ₹60,000–1,80,000 (CTC ~₹17 LPA)", "https://oil-india.com", "January", "March", "Executive Officer ➔ Senior Manager ➔ General Manager OIL", [
    { title: "GATE Petroleum/Mechanical/Civil Score", description: "Qualify GATE examination." },
    { title: "GD & Personal Interview", description: "Participate in OIL executive recruitment." }
  ], ["Upstream Energy", "Navratna PSU", "High Salary"], 50000, 80, "VERY_HIGH"),

  createCareer("cil-management-trainee", "Coal India Limited (CIL) Management Trainee", "ELITE", "GOVT", "PSUs & Energy Sector", "Manage mega opencast mining operations, heavy earthmoving machinery, and coal logistics.", "GRADUATE", 21, 30, 85000, 150000, "Pay Scale ₹50,000–1,60,000 (CTC ~₹16 LPA)", "https://coalindia.in", "July", "September", "Management Trainee ➔ Chief Manager ➔ General Manager ➔ Chairman CIL", [
    { title: "CIL CBT Exam or GATE Score", description: "Pass CIL online test or qualify via GATE Mining/Civil/Mech." },
    { title: "Document Verification & Medicals", description: "Clear fitness standards for mining operations." }
  ], ["Maharatna PSU", "Mining Engineering", "High Security"], 110000, 800, "HIGH"),

  createCareer("enterprise-security-architect", "Chief Information Security Officer (CISO / Cyber Lead)", "ELITE", "PRIVATE", "Software Engineering & IT", "Protect global cloud systems, lead zero-trust architecture, incident response, and anti-ransomware.", "GRADUATE", 22, 50, 150000, 420000, "CTC ₹35 - 95 LPA", "https://linkedin.com", "Rolling", "Continuous", "Security Analyst ➔ Security Architect ➔ CISO", [
    { title: "CISSP / CISM / CEH Certifications", description: "Obtain Certified Information Systems Security Professional credential." },
    { title: "Red Teaming & Cloud Threat Defense", description: "Master penetration testing, ISO 27001, and SOC operations." }
  ], ["Cyber Lead", "High Demand", "Top Tech Pay"], 35000, 300, "EXTREME"),

  createCareer("lead-ux-architect", "Director of User Experience & Design Systems", "ELITE", "PRIVATE", "Design, Product & Creative Arts", "Define design systems, micro-interactions, and accessibility standards for multi-million user apps.", "GRADUATE", 21, 48, 130000, 320000, "CTC ₹28 - 65 LPA", "https://dribbble.com", "Rolling", "Continuous", "UI Designer ➔ Senior UX Lead ➔ VP Design", [
    { title: "Figma Design System Mastery", description: "Build scalable multi-brand component libraries and design tokens." },
    { title: "UX Research & Metrics Impact", description: "Demonstrate conversion uplift and design ROI through A/B testing." }
  ], ["Design Leader", "Creative Vision", "High CTC"], 25000, 200, "VERY_HIGH"),

  createCareer("aiims-senior-researcher", "AIIMS Senior Clinical Scientist / Epidemiologist", "ELITE", "GOVT", "Medical, Nursing & Healthcare", "Lead vaccine trials, genetic disease mapping, and public health policy research at AIIMS.", "POST_GRADUATE", 25, 45, 95000, 180000, "Pay Level 11 / 12 (7th CPC)", "https://aiims.edu", "March", "May", "Scientist C ➔ Scientist E ➔ Director Clinical Research AIIMS", [
    { title: "Ph.D / MD in Public Health / Virology", description: "Complete advanced research degree with published clinical trials." }
  ], ["Apex Health R&D", "Public Health", "Prestige"], 15000, 40, "VERY_HIGH")
];

// 50 STABLE CAREERS
const STABLE_CAREERS: CareerPath[] = [
  createCareer("ssc-cgl-aso", "SSC CGL Assistant Section Officer (ASO in MEA / CSS)", "STABLE", "GOVT", "Civil Services & Public Admin", "Manage central government files, foreign desk policy support, and parliamentary questions.", "GRADUATE", 20, 30, 65000, 110000, "Pay Level 7 (7th CPC) ~₹70,000 PM", "https://ssc.gov.in", "June", "September", "ASO ➔ Section Officer ➔ Under Secretary ➔ Deputy Secretary to Govt of India", [
    { title: "Tier-1 Computer Based Test", description: "Maths, Reasoning, English, General Awareness speed test." },
    { title: "Tier-2 Advanced CBT", description: "Quantitative Abilities, English Language, Reasoning, and Computer Proficiency." },
    { title: "Document Verification & Medicals", description: "Verify educational certificates and clear standard medicals." }
  ], ["Ministry Post", "Foreign Posting in MEA", "High Job Security"], 2500000, 8000, "HIGH"),

  createCareer("sbi-po", "State Bank of India Probationary Officer (SBI PO)", "STABLE", "GOVT", "Banking & Financial Services", "Manage branch operations, credit evaluation, commercial loans, and digital banking services.", "GRADUATE", 21, 30, 65000, 120000, "Gross Pay ~₹72,000 PM + Lease Accommodation", "https://sbi.co.in", "September", "November", "Probationary Officer ➔ Branch Manager ➔ Assistant General Manager ➔ Chief General Manager SBI", [
    { title: "SBI PO Prelims", description: "English Language, Quantitative Aptitude, Reasoning Ability." },
    { title: "SBI PO Mains & Descriptive", description: "Data Analysis, General/Banking Awareness, and Essay/Letter typing." },
    { title: "Psychometric Test & Interview", description: "Group Exercises and Personal Interview round." }
  ], ["Premier Bank", "Fast Promotion", "High Status"], 1000000, 2000, "VERY_HIGH"),

  createCareer("ibps-po", "IBPS Probationary Officer (Public Sector Banks)", "STABLE", "GOVT", "Banking & Financial Services", "Manage banking operations, agricultural credit, and retail loans across 11 nationalized banks.", "GRADUATE", 20, 30, 58000, 95000, "Pay Scale 14500-31500 + Allowances (Gross ~₹62,000 PM)", "https://ibps.in", "August", "October", "PO / Scale-I ➔ Manager Scale-II ➔ Senior Manager ➔ General Manager", [
    { title: "IBPS Prelims", description: "Speed test in Reasoning, Quant, and English." },
    { title: "IBPS Mains", description: "Advanced Banking Awareness, Data Interpretation, and Descriptive Test." },
    { title: "Interview", description: "Panel interview at designated nodal bank." }
  ], ["Nationalized Banks", "Pan-India", "Job Security"], 800000, 4000, "HIGH"),

  createCareer("rrb-sse-je", "Indian Railways Senior Section Engineer / Junior Engineer", "STABLE", "GOVT", "Railways & Public Transport", "Technical supervision of railway tracks, signaling systems, locomotives, and electrical lines.", "DIPLOMA", 18, 33, 50000, 95000, "Pay Level 6 (JE) & Level 7 (SSE) + Free Railway Pass", "https://rrbcdg.gov.in", "March", "August", "Junior Engineer ➔ Senior Section Engineer ➔ Assistant Divisional Engineer (ADEN)", [
    { title: "RRB CBT-1 Screening", description: "Maths, Science, Reasoning, and General Awareness." },
    { title: "RRB CBT-2 Technical Domain", description: "Core Engineering Subjects (Civil/Mechanical/Electrical/ECE)." },
    { title: "Medical Standards (A-3)", description: "Strict eyesight and physical fitness test." }
  ], ["Railways", "Core Tech", "Free Travel Pass"], 1500000, 12000, "HIGH"),

  createCareer("ssc-cgl-iti", "SSC CGL Income Tax Inspector (ITI)", "STABLE", "GOVT", "Civil Services & Public Admin", "Investigate tax evasion, conduct search & seizure operations, and assess corporate tax filings.", "GRADUATE", 18, 30, 65000, 110000, "Pay Level 7 (7th CPC) + Uniform Allowance", "https://ssc.gov.in", "June", "September", "Inspector ➔ Assistant Commissioner of Income Tax ➔ Joint Commissioner", [
    { title: "SSC CGL Tier-1 & Tier-2", description: "Qualify combined graduate level written exam." },
    { title: "Departmental Exam", description: "Pass Income Tax law departmental paper for promotion." }
  ], ["Power & Respect", "CBDT Cadre", "High Demand"], 2000000, 1500, "VERY_HIGH"),

  createCareer("ssc-cgl-excise-inspector", "SSC CGL Central Excise & Customs Inspector (CBIC)", "STABLE", "GOVT", "Civil Services & Public Admin", "Inspect GST compliance, monitor sea ports/airports, and prevent contraband smuggling.", "GRADUATE", 18, 30, 65000, 110000, "Pay Level 7 (7th CPC) + Khaki Uniform", "https://ssc.gov.in", "June", "September", "Inspector ➔ Superintendent Central Excise ➔ Assistant Commissioner CBIC", [
    { title: "SSC CGL Exam Qualification", description: "Secure top merit position in CGL exam." },
    { title: "Physical Standard Test (PST)", description: "Height, chest measurement, walking, and cycling test." }
  ], ["Customs & GST", "Port Duty", "Prestige"], 1800000, 2000, "HIGH"),

  createCareer("lic-aao", "LIC Assistant Administrative Officer (LIC AAO)", "STABLE", "GOVT", "Banking & Financial Services", "Manage insurance underwriting, policy claims, actuarial support, and branch administration.", "GRADUATE", 21, 30, 60000, 110000, "Basic Pay ₹53,600 + DA/HRA (Gross ~₹85,000 PM)", "https://licindia.in", "January", "March", "AAO ➔ Administrative Officer ➔ Senior Divisional Manager ➔ Zonal Manager LIC", [
    { title: "LIC AAO Prelims", description: "Reasoning, Quantitative Aptitude, and English Language." },
    { title: "LIC AAO Mains", description: "Insurance & Financial Market Awareness + Descriptive English." },
    { title: "Interview", description: "LIC panel interview." }
  ], ["Life Insurance", "5-Day Work Week", "High Stability"], 500000, 300, "HIGH"),

  createCareer("capf-ac", "CAPF Assistant Commandant (CRPF / BSF / CISF / ITBP)", "STABLE", "GOVT", "Defence, Police & Security", "Command armed police company in border security, anti-naxal operations, and VIP protection.", "GRADUATE", 20, 25, 70000, 140000, "Pay Level 10 (7th CPC) Gazetted Officer", "https://upsc.gov.in", "April", "August", "Assistant Commandant ➔ Deputy Commandant ➔ Commandant (Col rank) ➔ Inspector General", [
    { title: "UPSC Written Exam (Paper 1 & 2)", description: "General Ability/Intelligence + General Studies/Essay/Precis." },
    { title: "Physical Efficiency Test (PET)", description: "100m sprint, 800m run, Long Jump, Shot Put." },
    { title: "Medical Board & Interview", description: "UPSC Board interview." }
  ], ["Uniformed Officer", "Paramilitary Command", "High Patriotism"], 300000, 300, "VERY_HIGH"),

  createCareer("ssc-cpo-si", "Sub-Inspector in Delhi Police & CAPF (SSC CPO)", "STABLE", "GOVT", "Defence, Police & Security", "Lead police station law & order, crime investigation, and anti-terror tactical teams.", "GRADUATE", 20, 25, 50000, 90000, "Pay Level 6 (7th CPC) ~₹55,000 PM", "https://ssc.gov.in", "March", "June", "Sub-Inspector ➔ Inspector ➔ Assistant Commissioner of Police (ACP)", [
    { title: "SSC CPO Paper-1", description: "Reasoning, GK, Maths, English comprehension." },
    { title: "Physical Endurance Test (PET)", description: "Race, High Jump, Long Jump fitness test." },
    { title: "SSC CPO Paper-2", description: "English Language & Comprehension test." }
  ], ["Delhi Police SI", "Uniform Cadre", "Authority"], 800000, 4000, "HIGH"),

  createCareer("sbi-junior-associate", "SBI Junior Associate (Customer Support & Clerk)", "STABLE", "GOVT", "Banking & Financial Services", "Handle cash transactions, account openings, customer service, and digital banking counters.", "GRADUATE", 20, 28, 35000, 55000, "Pay Scale ₹17,900–47,900 (Gross ~₹38,000 PM)", "https://sbi.co.in", "November", "January", "Junior Associate ➔ Trainee Officer (TO) ➔ Branch Manager Scale-II", [
    { title: "SBI Clerk Prelims", description: "Reasoning, Numerical Ability, English speed test." },
    { title: "SBI Clerk Mains", description: "General/Financial Awareness, General English, Quantitative Aptitude." },
    { title: "Local Language Test", description: "Verify proficiency in specified state local language." }
  ], ["Bank Entry", "Pan-India", "Job Security"], 1500000, 8000, "MODERATE"),

  createCareer("ibps-clerk", "IBPS Clerk (11 Public Sector Banks)", "STABLE", "GOVT", "Banking & Financial Services", "Manage front-desk customer operations, deposit clearing, and retail banking support.", "GRADUATE", 20, 28, 32000, 52000, "Gross Pay ~₹35,000 PM + Bank Leased Quarters", "https://ibps.in", "July", "September", "Clerk ➔ Scale-I Officer ➔ Branch Manager ➔ Senior Manager", [
    { title: "IBPS Clerk Prelims", description: "Qualify 1-hour speed test." },
    { title: "IBPS Clerk Mains", description: "Score high merit rank in Mains written test." }
  ], ["PSU Banks", "Stable Hours", "Promotions"], 1200000, 6000, "MODERATE"),

  createCareer("ssc-chsl-deo", "SSC CHSL Data Entry Operator (DEO) & LDC", "STABLE", "GOVT", "Civil Services & Public Admin", "Manage clerical files, data entry in central ministries, and typing administrative records.", "12TH", 18, 27, 32000, 55000, "Pay Level 2 (LDC) & Level 4 (DEO) ~₹35,000 PM", "https://ssc.gov.in", "April", "July", "Lower Division Clerk ➔ Upper Division Clerk ➔ Assistant Section Officer", [
    { title: "SSC CHSL Tier-1 CBT", description: "Maths, Reasoning, English, General Awareness." },
    { title: "SSC CHSL Tier-2 & Typing Test", description: "Module test + 35 wpm computer typing speed test." }
  ], ["12th Pass Entry", "Central Secretariat", "Clerical"], 3000000, 4500, "HIGH"),

  createCareer("rrb-ntpc-station-master", "RRB NTPC Station Master / Goods Guard", "STABLE", "GOVT", "Railways & Public Transport", "Control train signaling at railway stations, manage passenger platforms, and safety operations.", "GRADUATE", 18, 33, 45000, 85000, "Pay Level 6 + Night Duty & Running Allowance (~₹65,000 PM)", "https://rrbcdg.gov.in", "August", "December", "Station Master ➔ Station Superintendent ➔ Assistant Traffic Manager", [
    { title: "RRB NTPC CBT-1 & CBT-2", description: "General Awareness, Mathematics, General Intelligence." },
    { title: "Computer Based Aptitude Test (CBAT)", description: "Psychometric spatial & memory test for Station Masters." }
  ], ["Railways NTPC", "Platform Control", "High Allowance"], 12000000, 35000, "HIGH"),

  createCareer("rrb-alp", "RRB Assistant Loco Pilot (ALP)", "STABLE", "GOVT", "Railways & Public Transport", "Operate diesel & electric locomotives, monitor railway signal aspect, and speed safety.", "12TH", 18, 30, 35000, 70000, "Pay Level 2 + Running Mileage Allowance (~₹48,000 PM)", "https://rrbcdg.gov.in", "January", "June", "Assistant Loco Pilot ➔ Senior ALP ➔ Loco Pilot Passenger / Express ➔ Loco Inspector", [
    { title: "RRB ALP CBT-1 & CBT-2", description: "Mathematics, General Science, Basic Engineering & Trade Theory." },
    { title: "Aptitude Test (CBAT) & Eye Test", description: "A-1 Vision standard test (6/6 without glasses)." }
  ], ["Train Driver", "Locomotive", "Running Mileage"], 2000000, 18000, "HIGH"),

  createCareer("state-electricity-board-je", "State Electricity Board Junior Engineer (UPPCL / MSEDCL JE)", "STABLE", "GOVT", "PSUs & Energy Sector", "Maintain electrical substations, power distribution transformers, and power grid lines.", "DIPLOMA", 18, 40, 45000, 80000, "Pay Level 7 State Matrix ~₹50,000 PM", "https://uppcl.org", "Varies by State", "Annual", "Junior Engineer ➔ Assistant Engineer ➔ Executive Engineer UPPCL", [
    { title: "Electrical Engineering CBT", description: "150 Technical Electrical questions + 50 GK/Reasoning." },
    { title: "Document Verification", description: "Verify 3-year Electrical Diploma certificate." }
  ], ["State Electricity", "Substation JE", "State Job"], 300000, 1000, "HIGH"),

  createCareer("niacl-ao", "NIACL Administrative Officer (Generalist)", "STABLE", "GOVT", "Banking & Financial Services", "Manage commercial insurance policies, motor claims, marine cargo risk, and public insurance.", "GRADUATE", 21, 30, 60000, 105000, "Basic Pay ₹50,925 + DA/HRA (Gross ~₹80,000 PM)", "https://newindia.co.in", "July", "September", "Administrative Officer ➔ Assistant Manager ➔ Senior Divisional Manager NIACL", [
    { title: "NIACL AO Prelims & Mains", description: "Objective reasoning, quantitative aptitude, English, & general awareness." },
    { title: "Interview", description: "Public Sector Insurance panel interview." }
  ], ["General Insurance", "Good Work Life", "Metro Duty"], 300000, 300, "HIGH"),

  createCareer("fci-assistant-grade3", "Food Corporation of India (FCI) Assistant Grade-III", "STABLE", "GOVT", "Civil Services & Public Admin", "Manage central grain godowns, MSP grain procurement, quality control, and food distribution.", "GRADUATE", 18, 27, 35000, 65000, "Pay Scale ₹28,200–79,200 (Gross ~₹42,000 PM)", "https://fci.gov.in", "September", "January", "Assistant Grade-III ➔ Assistant Grade-II ➔ Manager ➔ Assistant General Manager FCI", [
    { title: "FCI Phase-1 Exam", description: "Numerical Ability, Reasoning, English, General Studies." },
    { title: "FCI Phase-2 Exam", description: "General / Depot / Accounts / Technical domain paper." }
  ], ["Food Grain MSP", "Godown Control", "Central PSU"], 1000000, 5000, "MODERATE"),

  createCareer("software-engineer-tcs-infosys", "Software Engineer / System Engineer (TCS / Infosys / Wipro)", "STABLE", "PRIVATE", "Software Engineering & IT", "Develop Java/Python applications, web portals, enterprise software, and maintenance code.", "GRADUATE", 21, 28, 30000, 70000, "Starting CTC ₹3.6 LPA – ₹7 LPA (Specialist Programmer up to ₹9 LPA)", "https://tcs.com/careers", "July", "Continuous", "Systems Engineer ➔ Senior Developer ➔ Tech Lead ➔ Project Manager", [
    { title: "NQT / National Qualifier Test", description: "Aptitude, Logical Reasoning, Verbal, and Coding test." },
    { title: "Technical & HR Interview", description: "Basics of C/Java/Python, SQL, OOPs, and final year project." }
  ], ["IT Services", "Bulk Hiring", "Global Mobility"], 500000, 50000, "MODERATE"),

  createCareer("cloud-ops-engineer", "Cloud Operations & DevOps Engineer", "STABLE", "PRIVATE", "Software Engineering & IT", "Deploy Docker containers, manage AWS EC2 servers, Jenkins CI/CD, and server health.", "GRADUATE", 21, 35, 45000, 110000, "Starting CTC ₹5 - 12 LPA", "https://linkedin.com", "Rolling", "Continuous", "DevOps Associate ➔ Senior Cloud Engineer ➔ DevOps Lead Architect", [
    { title: "Linux & Bash Scripting", description: "Master Linux terminal commands, shell scripts, and cron jobs." },
    { title: "AWS / Docker / Kubernetes", description: "Deploy cloud instances, Docker containers, and Kubernetes clusters." },
    { title: "CI/CD Pipelines", description: "Automate code build and deployment with GitHub Actions / Jenkins." }
  ], ["Cloud Tech", "DevOps", "High Growth"], 150000, 8000, "MODERATE"),

  createCareer("big4-financial-analyst", "Financial Analyst / Tax Consultant (Big-4: Deloitte/EY)", "STABLE", "PRIVATE", "Finance, Fintech & Analytics", "Audit corporate financial statements, perform statutory tax filing, and risk advisory.", "GRADUATE", 21, 30, 45000, 110000, "Starting CTC ₹6 - 12 LPA", "https://deloitte.com/careers", "August", "October", "Analyst ➔ Senior Consultant ➔ Manager ➔ Director / Partner Big-4", [
    { title: "Financial Accounting & US GAAP / IndAS", description: "Master trial balance, balance sheet, and audit standards." },
    { title: "Advanced MS Excel & Power BI", description: "Build financial pivot tables, VLOOKUP, macros, and financial dashboards." }
  ], ["Big 4 Brand", "Corporate Finance", "Prestige"], 100000, 5000, "HIGH"),

  createCareer("cyber-security-soc-analyst", "Cyber Security Analyst / L1 SOC Analyst", "STABLE", "PRIVATE", "Software Engineering & IT", "Monitor network security logs, detect malware intrusion, threat intelligence, and firewall alerts.", "GRADUATE", 21, 32, 40000, 95000, "Starting CTC ₹4.5 - 10 LPA", "https://linkedin.com", "Rolling", "Continuous", "L1 SOC Analyst ➔ L2 Threat Hunter ➔ Security Manager ➔ CISO", [
    { title: "Networking & Security Basics", description: "Understand TCP/IP, OSI model, DNS, Firewalls, and Wireshark." },
    { title: "CompTIA Security+ / CEH Cert", description: "Pass Certified Ethical Hacker or Security+ certification." }
  ], ["Cyber Defence", "SOC Analyst", "High Demand"], 80000, 4000, "MODERATE"),

  createCareer("fullstack-web-developer", "Full Stack Web Developer (Node.js / React / Python)", "STABLE", "PRIVATE", "Software Engineering & IT", "Build responsive web applications, REST APIs, PostgreSQL databases, and modern UI components.", "GRADUATE", 20, 35, 40000, 120000, "Starting CTC ₹5 - 14 LPA", "https://github.com", "Rolling", "Continuous", "Junior Developer ➔ Senior Full Stack Engineer ➔ Tech Lead", [
    { title: "Frontend Mastery (React / Tailwind)", description: "Build interactive web interfaces with React state management." },
    { title: "Backend API & Database (Node / Express / SQL)", description: "Create RESTful APIs, JWT authentication, and database schemas." }
  ], ["Web Dev", "Remote Options", "High Portfolio Impact"], 200000, 10000, "MODERATE"),

  createCareer("qa-automation-engineer", "QA Automation Test Engineer (Selenium / Cypress)", "STABLE", "PRIVATE", "Software Engineering & IT", "Write automated test scripts in Java/Python to verify software features before production deployment.", "GRADUATE", 21, 35, 38000, 90000, "Starting CTC ₹4 - 9 LPA", "https://linkedin.com", "Rolling", "Continuous", "QA Engineer ➔ Automation Lead ➔ QA Manager", [
    { title: "Manual Testing & Test Cases", description: "Master bug life cycle, Jira, and functional test plan creation." },
    { title: "Automation Frameworks", description: "Write Selenium WebDriver / Cypress scripts in Java or JavaScript." }
  ], ["Software Quality", "Steady Hiring", "Tech Entry"], 120000, 6000, "MODERATE"),

  createCareer("kvs-nvs-tgt-teacher", "KVS / NVS Trained Graduate Teacher (TGT / PGT)", "STABLE", "GOVT", "Teaching & Academic Research", "Teach secondary school subjects in Kendriya Vidyalayas & Navodaya Vidyalayas across India.", "GRADUATE", 21, 35, 48000, 85000, "Pay Level 7 (7th CPC) ~₹58,000 PM + Government Quarters", "https://kvsangathan.nic.in", "December", "February", "TGT ➔ PGT ➔ Vice Principal ➔ Principal KVS", [
    { title: "B.Ed Degree & CTET Qualification", description: "Pass Central Teacher Eligibility Test (CTET Paper-2)." },
    { title: "KVS Written Exam", description: "Pedagogy, Subject Knowledge, General English & Reasoning." },
    { title: "Classroom Demo & Interview", description: "Deliver teaching demo before selection board." }
  ], ["Kendriya Vidyalaya", "Teacher", "High Respect"], 400000, 4000, "HIGH"),

  createCareer("postal-assistant-india-post", "Postal Assistant / Sorting Assistant (India Post)", "STABLE", "GOVT", "Civil Services & Public Admin", "Manage post office counter operations, speed post logistics, and India Post Payments Bank accounts.", "12TH", 18, 27, 32000, 55000, "Pay Level 4 (7th CPC) ~₹36,000 PM", "https://indiapost.gov.in", "May", "August", "Postal Assistant ➔ Inspector Posts ➔ Superintendent of Post Offices", [
    { title: "SSC CHSL / CGL Exam", description: "Qualify central postal assistant recruitment test." },
    { title: "Typing Test & Data Verification", description: "30 wpm typing speed verification." }
  ], ["Post Office", "Central Govt", "Steady Job"], 1500000, 5000, "MODERATE"),

  createCareer("state-police-si", "State Police Sub-Inspector (UP Police / MP Police SI)", "STABLE", "GOVT", "Defence, Police & Security", "Maintain police station general diary, conduct criminal investigations, and enforce public safety.", "GRADUATE", 21, 28, 42000, 80000, "Pay Level 6 State Matrix ~₹48,000 PM", "https://uppbpb.gov.in", "Varies by State", "Annual", "Sub-Inspector ➔ Inspector ➔ Deputy Superintendent of Police (DSP)", [
    { title: "State Police Written Exam", description: "Hindi, General Knowledge, Numerical & Mental Ability." },
    { title: "Physical Standard & Running Test", description: "4.8 km run in 28 minutes for male candidates." }
  ], ["Police Station SI", "Uniform Authority", "State Security"], 1000000, 5000, "HIGH"),

  createCareer("high-court-assistant", "High Court Judicial Assistant / Stenographer Grade-III", "STABLE", "GOVT", "Legal, Judiciary & Rights", "Record court proceedings in shorthand, manage bench legal files, and issue court orders.", "GRADUATE", 18, 30, 40000, 75000, "Pay Level 6 (7th CPC) ~₹45,000 PM", "https://highcourt.gov.in", "Varies by State", "Annual", "Judicial Assistant ➔ Court Master ➔ Assistant Registrar High Court", [
    { title: "Written Exam", description: "English, General Knowledge, and Computer Knowledge." },
    { title: "Stenography Speed Test", description: "80 wpm shorthand & 40 wpm typing dictation test." }
  ], ["High Court Duty", "Stenography", "Court Master"], 200000, 800, "MODERATE"),

  createCareer("sub-registrar-land", "Sub-Registrar (Land Revenue & Stamp Duty Inspector)", "STABLE", "GOVT", "Civil Services & Public Admin", "Register property deeds, land sales, marriage certificates, and collect state stamp duty.", "GRADUATE", 21, 35, 45000, 85000, "Pay Level 6 / 7 State Pay Matrix", "https://state.gov.in", "Varies by State", "Annual", "Sub-Registrar Grade-II ➔ Sub-Registrar Grade-I ➔ District Registrar", [
    { title: "State PSC Group-2 Exam", description: "General Studies & State Administration paper." }
  ], ["Land Revenue", "Property Stamps", "High Local Power"], 400000, 100, "HIGH"),

  createCareer("commercial-tax-officer", "Commercial Tax Officer / State GST Inspector", "STABLE", "GOVT", "Civil Services & Public Admin", "Audit commercial traders, enforce state GST compliance, and manage e-way bill check posts.", "GRADUATE", 21, 35, 50000, 90000, "Pay Level 7 State Pay Matrix", "https://state.gov.in", "Varies by State", "Annual", "Commercial Tax Inspector ➔ Commercial Tax Officer ➔ Assistant Commissioner State Tax", [
    { title: "State PSC Combined Exam", description: "State administrative selection written exam." }
  ], ["State GST", "Audit Power", "Tax Inspector"], 500000, 200, "HIGH"),

  createCareer("block-development-officer", "Block Development Officer (BDO)", "STABLE", "GOVT", "Civil Services & Public Admin", "Supervise rural development schemes, MGNREGA, PM Awas Yojana, and Gram Panchayat funds.", "GRADUATE", 21, 35, 55000, 95000, "Pay Level 8 State Pay Matrix", "https://state.gov.in", "Varies by State", "Annual", "BDO ➔ District Development Officer (DDO) ➔ Joint Director Rural Development", [
    { title: "State Public Service Commission Mains", description: "Qualify State Civil Services Exam." }
  ], ["Rural Development", "Block Head", "Gram Panchayat"], 600000, 150, "VERY_HIGH"),

  createCareer("tehsildar-naib", "Naib Tehsildar / Executive Magistrate", "STABLE", "GOVT", "Civil Services & Public Admin", "Execute land mutation, revenue collection, caste/income certificate issuance, and sub-division law.", "GRADUATE", 21, 35, 48000, 85000, "Pay Level 6 / 7 State Pay Matrix", "https://state.gov.in", "Varies by State", "Annual", "Naib Tehsildar ➔ Tehsildar ➔ Sub-Divisional Magistrate (SDM)", [
    { title: "Naib Tehsildar Written Exam", description: "General Studies, State Revenue Laws, and Language paper." }
  ], ["Executive Magistrate", "Land Revenue", "Tehsil Head"], 500000, 120, "VERY_HIGH"),

  createCareer("nursing-officer-aiims", "AIIMS Nursing Officer (NORCET Exam)", "STABLE", "GOVT", "Medical, Nursing & Healthcare", "Provide patient care, ICU monitoring, surgical assistance, and hospital nursing management.", "GRADUATE", 18, 30, 60000, 110000, "Pay Level 7 (7th CPC) Basic ₹44,900 + Allowances (~₹75,000 PM)", "https://aiimsexams.ac.in", "April / September", "Bi-annual", "Nursing Officer ➔ Senior Nursing Officer ➔ Assistant Nursing Superintendent ➔ Chief Nursing Officer", [
    { title: "B.Sc Nursing / GNM Diploma", description: "Complete B.Sc Nursing or GNM with 2-yr hospital experience." },
    { title: "AIIMS NORCET Exam", description: "Pass Nursing Officer Recruitment Common Eligibility Test." }
  ], ["AIIMS Nurse", "High Salary", "Bi-Annual Exam"], 200000, 3000, "HIGH"),

  createCareer("lab-technologist-aiims", "Medical Lab Technologist (AIIMS / Railway Hospitals)", "STABLE", "GOVT", "Medical, Nursing & Healthcare", "Conduct blood biochemistry, histopathology, molecular diagnostics, and pathology reports.", "GRADUATE", 18, 30, 38000, 70000, "Pay Level 6 (7th CPC) ~₹45,000 PM", "https://aiims.edu", "March", "May", "Lab Technologist ➔ Technical Officer ➔ Senior Technical Officer", [
    { title: "B.Sc Medical Lab Technology (BMLT)", description: "Complete degree or diploma in MLT." },
    { title: "Written Recruitment CBT", description: "Pathology, Microbiology, Biochemistry technical paper." }
  ], ["Diagnostic Lab", "Hospital Cadre", "Steady"], 80000, 500, "MODERATE"),

  createCareer("primary-teacher-prt", "Primary School Teacher (PRT via CTET / KVS)", "STABLE", "GOVT", "Teaching & Academic Research", "Teach Class 1-5 primary students in fundamental mathematics, languages, and environmental studies.", "12TH", 18, 30, 38000, 65000, "Pay Level 6 (7th CPC) ~₹48,000 PM", "https://kvsangathan.nic.in", "November", "January", "PRT Teacher ➔ TGT Teacher ➔ Headmaster Primary School", [
    { title: "D.El.Ed / D.Ed Diploma + CTET Paper-1", description: "Complete 2-year Diploma in Elementary Education." },
    { title: "KVS PRT Exam & Interview", description: "Pass written exam and teaching demonstration." }
  ], ["Primary Teaching", "CTET", "Good Hours"], 600000, 6000, "MODERATE"),

  createCareer("hr-generalist-mnc", "HR Generalist / Talent Acquisition Specialist", "STABLE", "PRIVATE", "Management, Strategy & Business", "Manage corporate recruitment, employee onboarding, HR compliance, and payroll processing.", "GRADUATE", 21, 35, 35000, 85000, "Starting CTC ₹4 - 9 LPA", "https://linkedin.com", "Rolling", "Continuous", "HR Executive ➔ Senior HR Manager ➔ Head of Human Resources (CHRO)", [
    { title: "MBA / BBA in HR or Psychology", description: "Master labor laws, recruitment ATS tools, and organizational behavior." }
  ], ["Corporate HR", "People Management", "Corporate"], 90000, 4000, "MODERATE"),

  createCareer("digital-marketing-specialist", "Digital Marketing Specialist / SEO & Performance Lead", "STABLE", "PRIVATE", "Design, Product & Creative Arts", "Manage Google Ads, Meta Ads campaigns, search engine optimization, and lead generation funnels.", "GRADUATE", 18, 35, 35000, 95000, "Starting CTC ₹4 - 10 LPA", "https://google.com/skillshop", "Rolling", "Continuous", "Digital Marketing Executive ➔ Performance Lead ➔ VP Marketing", [
    { title: "Google Ads & Meta Certifications", description: "Master Search Ads, Analytics 4, SEO technical audits, and CAC/LTV." }
  ], ["Growth Lead", "Performance Ads", "High Remote Demand"], 120000, 5000, "MODERATE"),

  createCareer("supply-chain-logistics-lead", "Supply Chain & Logistics Operations Manager", "STABLE", "PRIVATE", "Management, Strategy & Business", "Optimize warehouse inventory, fleet dispatch, Amazon/Flipkart fulfillment centers, and vendor logistics.", "GRADUATE", 21, 38, 40000, 100000, "Starting CTC ₹5 - 12 LPA", "https://linkedin.com", "Rolling", "Continuous", "Logistics Executive ➔ Warehouse Manager ➔ Supply Chain Director", [
    { title: "Supply Chain & ERP Systems (SAP / Oracle)", description: "Master inventory turnover metrics, warehouse management systems, and freight routing." }
  ], ["E-Commerce", "Supply Chain", "High Demand"], 80000, 3000, "MODERATE"),

  createCareer("data-analyst-sql-powerbi", "Data Analyst (SQL / Power BI / Python)", "STABLE", "PRIVATE", "AI, Data Science & Analytics", "Clean datasets, write complex SQL queries, and build Power BI executive dashboards.", "GRADUATE", 20, 35, 42000, 105000, "Starting CTC ₹5 - 12 LPA", "https://linkedin.com", "Rolling", "Continuous", "Data Analyst ➔ Senior Analytics Lead ➔ Analytics Manager", [
    { title: "Advanced SQL & Database Queries", description: "Master JOINs, Window Functions, Group By, and Indexing." },
    { title: "Power BI / Tableau Dashboards", description: "Build interactive visual reports for corporate KPIs." }
  ], ["Analytics", "SQL & Power BI", "High Jobs"], 150000, 8000, "MODERATE"),

  createCareer("ai-solutions-developer", "Generative AI & LLM Application Developer", "STABLE", "PRIVATE", "AI, Data Science & Analytics", "Build RAG enterprise search, LangChain agents, OpenAI/Gemini API integrations, and vector embeddings.", "GRADUATE", 21, 35, 55000, 135000, "Starting CTC ₹7 - 16 LPA", "https://github.com", "Rolling", "Continuous", "Junior AI Dev ➔ Senior GenAI Engineer ➔ AI Solutions Architect", [
    { title: "Python & LangChain / LlamaIndex", description: "Build automated document reasoning and chatbot workflows." },
    { title: "API Integration & Vector Stores", description: "Connect ChromaDB, Pinecone, and serverless LLM endpoints." }
  ], ["GenAI", "LLM", "High Demand"], 80000, 3000, "MODERATE"),

  createCareer("nic-scientist-b-it", "NIC Scientist 'B' (National Informatics Centre)", "STABLE", "GOVT", "Software Engineering & IT", "Build digital India e-governance platforms, DigiLocker, PM-Kisan portal, and government cloud security.", "GRADUATE", 21, 30, 65000, 115000, "Pay Level 10 (7th CPC) ~₹75,000 PM Gazetted", "https://recruitment.nic.in", "October", "December", "Scientist B ➔ Scientist C ➔ Scientist D ➔ Director NIC", [
    { title: "NIELIT / NIC Written Exam", description: "Computer Science syllabus: OS, DBMS, Algorithms, Cyber Security." },
    { title: "Technical Interview", description: "Software architecture and e-governance case questions." }
  ], ["Govt Tech", "Digital India", "Gazetted Officer"], 120000, 350, "HIGH"),

  createCareer("mechanical-oem-engineer", "Automotive OEM Mechanical Engineer (Tata Motors / Mahindra)", "STABLE", "PRIVATE", "Core Engineering Services", "Design vehicle chassis, EV battery thermal management, engine powertrains, and assembly lines.", "GRADUATE", 21, 35, 40000, 95000, "Starting CTC ₹5 - 11 LPA", "https://tatamotors.com/careers", "July", "Continuous", "Graduate Engineer Trainee ➔ Senior Engineer ➔ Plant Head", [
    { title: "CAD / CATIA / SolidWorks Design", description: "Master 3D CAD modeling, GD&T, and finite element analysis." }
  ], ["Automotive", "Tata / Mahindra", "Core Engg"], 90000, 3000, "MODERATE"),

  createCareer("civil-site-engineer-lt", "Civil Site Engineer (L&T / Tata Projects)", "STABLE", "PRIVATE", "Core Engineering Services", "Supervise highway construction, metro rail elevated tracks, high-rise concrete structures, and safety.", "GRADUATE", 21, 35, 38000, 90000, "Starting CTC ₹4.5 - 10 LPA", "https://larsentoubro.com", "July", "Continuous", "GET Civil ➔ Site Manager ➔ Project Director Infrastructure", [
    { title: "Autocad & Structural Drawings", description: "Interpret bar bending schedules, concrete mix ratios, and land surveying." }
  ], ["Infrastructure", "L&T Metro", "Core Civil"], 120000, 4000, "MODERATE"),

  createCareer("private-bank-assistant-manager", "Private Bank Assistant Manager (HDFC / ICICI / Axis)", "STABLE", "PRIVATE", "Banking & Financial Services", "Manage wealth relationships, loan processing, trade finance, and branch banking counters.", "GRADUATE", 20, 28, 35000, 75000, "Starting CTC ₹4 - 8 LPA", "https://hdfcbank.com/careers", "Rolling", "Continuous", "Assistant Manager ➔ Branch Manager ➔ Circle Head", [
    { title: "Banking Sales & Financial Products", description: "Clear NISM mutual fund certification and bank entrance interview." }
  ], ["HDFC / ICICI", "Branch Bank", "Steady Entry"], 300000, 15000, "MODERATE"),

  createCareer("pharmacist-govt-hospital", "Govt Hospital Pharmacist / Drug Inspector Assistant", "STABLE", "GOVT", "Medical, Nursing & Healthcare", "Dispense medicine in central hospitals, manage drug inventory, and verify drug store safety.", "DIPLOMA", 18, 32, 35000, 65000, "Pay Level 5 (7th CPC) ~₹40,000 PM", "https://ssc.gov.in", "Varies by State", "Annual", "Pharmacist ➔ Chief Pharmacist ➔ Drug Inspector", [
    { title: "D.Pharm / B.Pharm Degree", description: "Registered with Pharmacy Council of India." },
    { title: "Written Recruitment Exam", description: "Pharmacology, Pharmaceutical Chemistry, and General Science." }
  ], ["Pharmacy", "Hospital Drug", "Government"], 100000, 1200, "MODERATE"),

  createCareer("fire-station-officer", "Municipal Fire Station Officer / Safety Inspector", "STABLE", "GOVT", "Defence, Police & Security", "Lead emergency fire rescue squads, inspect commercial building fire safety, and hazard control.", "GRADUATE", 21, 30, 42000, 80000, "Pay Level 6 State Matrix", "https://state.gov.in", "Varies by State", "Annual", "Station Officer ➔ Divisional Fire Officer ➔ Director Fire Services", [
    { title: "B.Sc Fire Safety / Engineering", description: "Pass written fire science exam and physical endurance test." }
  ], ["Fire Service", "Emergency Rescue", "State Duty"], 50000, 200, "MODERATE"),

  createCareer("forest-guard-forester", "State Forest Guard / Deputy Forester", "STABLE", "GOVT", "Civil Services & Public Admin", "Protect wildlife sanctuaries, counter illegal timber poaching, and manage forest conservation.", "12TH", 18, 28, 28000, 50000, "Pay Level 2 / 3 State Pay Matrix", "https://forest.gov.in", "Varies by State", "Annual", "Forest Guard ➔ Forester ➔ Range Forest Officer (RFO)", [
    { title: "12th Pass Science Stream", description: "Pass written science exam and 25km walking physical test." }
  ], ["Wildlife Protection", "Forest", "12th Pass"], 500000, 2000, "MODERATE"),

  createCareer("junior-accountant-state", "Junior Accountant / Treasury Auditor (State Accounts)", "STABLE", "GOVT", "Civil Services & Public Admin", "Verify government department bills, pension disbursements, treasury accounts, and audit logs.", "GRADUATE", 21, 35, 38000, 70000, "Pay Level 5 State Matrix ~₹42,000 PM", "https://state.gov.in", "Varies by State", "Annual", "Junior Accountant ➔ Senior Accountant ➔ Assistant Treasury Officer", [
    { title: "Commerce / Math Graduate Exam", description: "Bookkeeping, State Financial Rules, and General Knowledge." }
  ], ["Treasury Accounts", "Auditor", "State Office"], 300000, 1500, "MODERATE"),

  createCareer("cooperative-bank-manager", "State Cooperative Bank Branch Manager / Clerk", "STABLE", "GOVT", "Banking & Financial Services", "Manage rural farmer crop loans, cooperative society deposits, and local branch banking.", "GRADUATE", 20, 30, 35000, 75000, "State Cooperative Pay Matrix", "https://cooperative.gov.in", "Varies by State", "Annual", "Clerk ➔ Branch Manager ➔ CEO Cooperative Bank", [
    { title: "Cooperative Bank Written Test", description: "Reasoning, Banking, Co-operative Law, and Local Language." }
  ], ["Cooperative Bank", "Farmer Loans", "Local City"], 200000, 1000, "MODERATE"),

  createCareer("telecom-jto-bsnl", "BSNL Junior Telecom Officer (JTO / TTA)", "STABLE", "GOVT", "PSUs & Energy Sector", "Maintain optical fiber telephone exchanges, 4G/5G mobile towers, and broadband networks.", "GRADUATE", 21, 30, 42000, 80000, "Pay Scale ₹16,400–40,500 (Gross ~₹48,000 PM)", "https://bsnl.co.in", "June", "September", "JTO ➔ Sub-Divisional Engineer (SDE) ➔ Divisional Engineer BSNL", [
    { title: "GATE ECE/CS Score or BSNL CBT", description: "Qualify technical telecom examination." }
  ], ["Telecom PSU", "5G Towers", "Fiber Net"], 150000, 800, "MODERATE"),

  createCareer("railway-tc-commercial-clerk", "Railway Ticket Collector (TC) & Commercial Clerk", "STABLE", "GOVT", "Railways & Public Transport", "Check passenger tickets on trains, manage ticket reservation counters, and parcel handling.", "12TH", 18, 30, 32000, 60000, "Pay Level 3 (7th CPC) + Traveling Allowance (~₹40,000 PM)", "https://rrbcdg.gov.in", "August", "November", "Ticket Examiner ➔ Chief Ticket Inspector (CTI) ➔ Commercial Inspector", [
    { title: "RRB NTPC Under-Graduate CBT", description: "General Awareness, Maths, and Reasoning 12th level exam." }
  ], ["Railway Ticket Check", "12th Pass", "Train Travel"], 4000000, 6000, "HIGH"),

  createCareer("cwc-junior-superintendent", "Central Warehousing Corporation (CWC) Superintendent", "STABLE", "GOVT", "Civil Services & Public Admin", "Supervise logistics godowns, import-export cargo storage, ICD inland container depots.", "GRADUATE", 18, 30, 40000, 75000, "Pay Scale ₹29,000–93,000 (Gross ~₹48,000 PM)", "https://cewacor.nic.in", "October", "December", "Junior Superintendent ➔ Superintendent ➔ Warehouse Manager CWC", [
    { title: "CWC Online Written Exam", description: "Reasoning, English, Quantitative Aptitude, General Awareness." }
  ], ["Warehousing", "Central Logistics", "Mini Navratna"], 150000, 250, "MODERATE"),

  createCareer("isro-technical-assistant", "ISRO Technical Assistant (Diploma Cadre)", "STABLE", "GOVT", "Science, Space & Aerospace R&D", "Assist space scientists in rocket assembly, satellite cleanroom testing, and telemetry labs.", "DIPLOMA", 18, 35, 45000, 80000, "Pay Level 7 (7th CPC) ~₹55,000 PM", "https://isro.gov.in", "Varies by Center", "Regular", "Technical Assistant ➔ Senior Technical Assistant ➔ Technical Officer", [
    { title: "Written Test in Engineering Trade", description: "Diploma level Mechanical/ECE/Electrical objective paper." },
    { title: "Skill Test", description: "Practical workshop trade test." }
  ], ["Space Technician", "ISRO Labs", "Diploma Entry"], 100000, 300, "HIGH")
];

// 10+ HIDDEN GEMS CAREERS
const HIDDEN_GEM_CAREERS: CareerPath[] = [
  createCareer("epfo-eo-ao", "EPFO Enforcement Officer / Accounts Officer (EO/AO)", "HIDDEN_GEM", "GOVT", "Civil Services & Public Admin", "Audit factory provident funds, enforce social security labor laws, and prosecute default employers.", "GRADUATE", 21, 30, 75000, 130000, "Pay Level 8 (7th CPC) ~₹85,000 PM Gazetted", "https://upsc.gov.in", "May", "July", "EO/AO ➔ Assistant PF Commissioner (APFC) ➔ Regional PF Commissioner", [
    { title: "UPSC Special Recruitment Test", description: "General English, Indian Freedom Struggle, Labor Laws, Industrial Relations, General Accounting." },
    { title: "Personality Test", description: "UPSC Interview for labor enforcement cadre." }
  ], ["Social Security", "Labor Laws", "Gazetted Post"], 600000, 400, "VERY_HIGH"),

  createCareer("fssai-technical-officer", "FSSAI Technical Officer / Food Safety Officer", "HIDDEN_GEM", "GOVT", "Medical, Nursing & Healthcare", "Inspect food manufacturing plants, audit adulteration standards, and enforce FSSAI license compliance.", "GRADUATE", 21, 30, 60000, 110000, "Pay Level 7 (7th CPC) ~₹70,000 PM", "https://fssai.gov.in", "September", "January", "Technical Officer ➔ Assistant Director ➔ Deputy Director FSSAI", [
    { title: "FSSAI CBT Stage-1", description: "General Intelligence, General Awareness, English, Computer." },
    { title: "FSSAI CBT Stage-2", description: "Food Safety Act 2006, Chemistry, Food Microbiology, and Standards." }
  ], ["Food Safety", "Clean Work Environment", "Regulatory Authority"], 150000, 200, "HIGH"),

  createCareer("patent-examiner-cgpdtm", "Patent & Trademark Examiner (Ministry of Commerce)", "HIDDEN_GEM", "GOVT", "Science, Space & Aerospace R&D", "Evaluate novel patent filings, check global prior art, and grant exclusive intellectual property rights.", "GRADUATE", 21, 35, 70000, 130000, "Pay Level 10 (7th CPC) ~₹80,000 PM Gazetted", "https://ipindia.gov.in", "July", "September", "Examiner of Patents ➔ Controller of Patents ➔ Senior Controller", [
    { title: "Preliminary Objective Exam", description: "General Studies, Aptitude, IP laws." },
    { title: "Mains Technical Paper", description: "Core discipline exam (Bio/Chem/Mech/ECE/CS)." },
    { title: "Interview", description: "Patent controller selection interview." }
  ], ["Intellectual Property", "High Tech Review", "Gazetted Officer"], 80000, 500, "HIGH"),

  createCareer("bis-scientist-b", "Bureau of Indian Standards (BIS) Scientist 'B'", "HIDDEN_GEM", "GOVT", "Science, Space & Aerospace R&D", "Set national ISI product quality standards, audit manufacturing labs, and consumer protection.", "GRADUATE", 21, 30, 80000, 140000, "Pay Level 10 (7th CPC) ~₹90,000 PM", "https://bis.gov.in", "August", "October", "Scientist B ➔ Scientist C ➔ Director BIS", [
    { title: "GATE Score or BIS CBT", description: "Qualify technical engineering paper." },
    { title: "Interview", description: "BIS selection board interview." }
  ], ["ISI Standards", "Lab Quality", "High Authority"], 60000, 150, "VERY_HIGH"),

  createCareer("wildlife-biologist-eia", "Wildlife Biologist / Environmental Impact Specialist", "HIDDEN_GEM", "PRIVATE", "Science, Space & Aerospace R&D", "Conduct biodiversity surveys, assess ecological risk for infra projects, and wildlife corridors.", "GRADUATE", 21, 40, 50000, 120000, "Starting CTC ₹6 - 14 LPA", "https://wii.gov.in", "Rolling", "Continuous", "Field Biologist ➔ Senior EIA Consultant ➔ Head of Environmental Advisory", [
    { title: "M.Sc Wildlife / Zoology / Forestry", description: "Master ecological field sampling, GIS mapping, and fauna surveys." }
  ], ["Eco Conservation", "Outdoor Fieldwork", "Niche Skill"], 15000, 100, "MODERATE"),

  createCareer("uiux-product-designer", "UI-UX Lead / Digital Product Designer", "HIDDEN_GEM", "PRIVATE", "Design, Product & Creative Arts", "Design intuitive mobile app screens, Figma micro-interactions, and design systems for tech startups.", "GRADUATE", 18, 45, 50000, 220000, "Starting CTC ₹6 - 18 LPA", "https://dribbble.com", "Rolling", "Continuous", "UI Designer ➔ Product Designer ➔ UX Lead ➔ Head of Design", [
    { title: "Figma Mastery & Component Libraries", description: "Build auto-layout interactive UI prototypes." },
    { title: "User Case Studies Portfolio", description: "Publish 2 detailed UX research case studies on Behance/Dribbble." }
  ], ["Creative Tech", "High Remote Pay", "Portfolio Based"], 90000, 5000, "MODERATE"),

  createCareer("cdsco-drug-inspector", "CDSCO Central Drug Inspector (Ministry of Health)", "HIDDEN_GEM", "GOVT", "Medical, Nursing & Healthcare", "Inspect pharmaceutical factories, sample medicine batches, and stop counterfeit drugs.", "GRADUATE", 21, 30, 65000, 120000, "Pay Level 8 (7th CPC) ~₹75,000 PM", "https://cdsco.gov.in", "Varies by Year", "Regular", "Drug Inspector ➔ Assistant Drug Controller ➔ Drug Controller General of India (DCGI)", [
    { title: "B.Pharm Degree + 1.5 Yr Pharma Mfg Experience", description: "Degree in Pharmacy with mandatory industry experience." },
    { title: "UPSC Drug Inspector Exam", description: "Written exam in Pharmacy laws, Pharmacology, and Quality Control." }
  ], ["Drug Safety", "Pharma Inspector", "High Respect"], 40000, 80, "HIGH"),

  createCareer("imd-scientific-assistant", "Indian Meteorological Department (IMD) Scientific Assistant", "HIDDEN_GEM", "GOVT", "Science, Space & Aerospace R&D", "Operate Doppler weather radar, forecast monsoons, cyclones, and climate observation systems.", "GRADUATE", 18, 30, 42000, 75000, "Pay Level 6 (7th CPC) ~₹50,000 PM", "https://mausam.imd.gov.in", "October", "December", "Scientific Assistant ➔ Meteorologist Grade-II ➔ Scientist E IMD", [
    { title: "B.Sc Physics / Math / CS or Diploma ECE", description: "Degree with 60%+ in Physics or Electronics." },
    { title: "SSC IMD Written Exam", description: "Physics, Computer Science, and General Science paper." }
  ], ["Weather Radar", "Monsoon Tracking", "Science Job"], 120000, 1000, "MODERATE"),

  createCareer("psu-bank-law-officer", "IBPS Specialist Officer Law (PSU Bank Legal Officer)", "HIDDEN_GEM", "GOVT", "Legal, Judiciary & Rights", "Manage bank legal litigation, debt recovery tribunals (DRT), mortgage deeds, and SARFAESI enforcement.", "GRADUATE", 20, 30, 58000, 95000, "Scale-I Officer Pay ~₹62,000 PM", "https://ibps.in", "November", "December", "Law Officer Scale-I ➔ Chief Legal Manager ➔ General Manager Legal", [
    { title: "LL.B Degree & Advocate Registration", description: "Enrolled as Advocate with Bar Council." },
    { title: "IBPS SO Law Written & Interview", description: "Banking Law, SARFAESI, Negotiable Instruments Act exam." }
  ], ["Bank Lawyer", "Legal Advisory", "No Public Counter"], 50000, 300, "MODERATE"),

  createCareer("instructional-designer-edtech", "Instructional Designer / EdTech Content Architect", "HIDDEN_GEM", "PRIVATE", "Teaching & Academic Research", "Structure interactive online courses, micro-learning modules, and gamified corporate training.", "GRADUATE", 21, 40, 45000, 110000, "Starting CTC ₹5 - 12 LPA", "https://linkedin.com", "Rolling", "Continuous", "Instructional Designer ➔ Curriculum Lead ➔ VP Learning Experience", [
    { title: "ADDIE Model & Curriculum Design", description: "Master learning pedagogy, Storyline 360, and multimedia courseware." }
  ], ["EdTech", "Curriculum", "High Growth"], 30000, 1000, "MODERATE"),

  createCareer("eic-technical-officer", "Export Inspection Council (EIC) Technical Officer", "HIDDEN_GEM", "GOVT", "Agri-Tech & Forest Services", "Certify quality & safety of Indian agricultural, seafood, and industrial exports to global markets.", "GRADUATE", 21, 30, 55000, 95000, "Pay Level 7 (7th CPC)", "https://eicindia.gov.in", "November", "January", "Technical Officer ➔ Assistant Director ➔ Joint Director EIC", [
    { title: "B.Sc Agriculture / Food Tech / Chemistry", description: "Pass written technical certification exam." }
  ], ["Global Exports", "Quality Audit", "Commerce Ministry"], 25000, 50, "MODERATE"),

  createCareer("mlops-engineer-remote", "MLOps Engineer & AI Infrastructure Lead", "HIDDEN_GEM", "PRIVATE", "AI, Data Science & Analytics", "Deploy scalable LLM inference pipelines, GPU cluster scheduling, model quantization, and vector databases.", "GRADUATE", 21, 40, 80000, 250000, "Starting CTC ₹12 - 35 LPA", "https://github.com", "Rolling", "Continuous", "MLOps Engineer ➔ Senior Infrastructure Lead ➔ VP AI Platform", [
    { title: "Docker, Kubernetes & Triton Inference Server", description: "Package PyTorch/TensorFlow models with zero-downtime serving." },
    { title: "MLflow & Weights & Biases", description: "Automate model artifact tracking, CI/CD for machine learning pipelines." },
    { title: "Vector DB & GPU Optimization", description: "Build low-latency RAG vector search with Pinecone, Milvus, and vLLM." }
  ], ["AI Platform", "MLOps", "High Salary", "Remote"], 35000, 800, "HIGH"),

  createCareer("computer-vision-specialist", "Computer Vision & Robotics AI Specialist", "HIDDEN_GEM", "PRIVATE", "AI, Data Science & Analytics", "Develop real-time object detection, autonomous vehicle perception, drone surveillance, and edge AI algorithms.", "GRADUATE", 21, 38, 75000, 220000, "Starting CTC ₹10 - 28 LPA", "https://linkedin.com", "Rolling", "Continuous", "CV Engineer ➔ Perception Lead ➔ Principal Robotics AI Scientist", [
    { title: "OpenCV, PyTorch & TensorRT", description: "Optimize YOLO, CNN, and Vision Transformer models for NVIDIA Jetson/Edge devices." },
    { title: "Point Cloud & 3D Spatial Computing", description: "Process LiDAR sensors, depth maps, and real-time visual SLAM." }
  ], ["Computer Vision", "Robotics", "Autonomous Systems"], 25000, 500, "HIGH"),

  createCareer("iis-officer-media", "Indian Information Service (IIS) Group-A Officer", "HIDDEN_GEM", "GOVT", "Media, Journalism & PR", "Direct government national media broadcasts, DD News, Press Information Bureau (PIB), and counter misinformation.", "GRADUATE", 21, 32, 75000, 160000, "Pay Level 10 (7th CPC) ~₹85,000 PM Gazetted", "https://upsc.gov.in", "February", "May", "Assistant Director PIB ➔ Deputy Director ➔ Director General PIB / Doordarshan", [
    { title: "UPSC Civil Services Examination", description: "Qualify Prelims, Mains, and Personality Test for IIS cadre." },
    { title: "Indian Institute of Mass Communication (IIMC)", description: "Complete professional media and broadcasting training in New Delhi." }
  ], ["PIB Spokesperson", "Govt Media", "High Public Impact"], 400000, 40, "VERY_HIGH"),

  createCareer("icar-ars-scientist", "Agricultural Research Service (ARS) Scientist (ICAR)", "HIDDEN_GEM", "GOVT", "Agri-Tech & Forest Services", "Pioneer crop genetics, drought-resistant seeds, precision hydroponics, and soil microbiome research.", "POST_GRADUATE", 21, 35, 80000, 150000, "Pay Level 10 (7th CPC) UGC Scientist Scale", "https://asrb.org.in", "April", "June", "Scientist (ARS) ➔ Senior Scientist ➔ Principal Scientist ➔ Director ICAR Institute", [
    { title: "M.Sc Agriculture / Biotechnology / Agronomy", description: "Complete Master's degree with high academic standing." },
    { title: "ASRB ARS Prelims & Mains", description: "Pass national agricultural research service competitive exam." },
    { title: "Viva-Voce / Research Interview", description: "Defend agricultural thesis and national research proposal." }
  ], ["Agritech Research", "ICAR Labs", "Peaceful Career"], 45000, 250, "HIGH"),

  createCareer("drone-systems-engineer", "Drone & UAV Flight Systems Engineer", "HIDDEN_GEM", "PRIVATE", "Aviation & Aerospace R&D", "Design autonomous commercial delivery drones, flight controllers, telemetry radios, and DGCA type certifications.", "GRADUATE", 21, 35, 60000, 160000, "Starting CTC ₹7 - 20 LPA", "https://linkedin.com", "Rolling", "Continuous", "UAV Engineer ➔ Lead Avionics Architect ➔ CTO Drone OEM", [
    { title: "PX4 / ArduPilot Flight Controllers", description: "Master PID tuning, waypoint navigation, and telemetry links." },
    { title: "Embedded C++ & ROS 2", description: "Program onboard companion computers for obstacle avoidance." }
  ], ["Drone Tech", "Aviation Startup", "High Growth"], 30000, 600, "MODERATE"),

  createCareer("patent-attorney-ip", "Registered Patent Attorney & Tech Transfer Counsel", "HIDDEN_GEM", "PRIVATE", "Law & Judicial Services", "Draft international tech patents, conduct infringement freedom-to-operate searches, and license deep-tech IP.", "GRADUATE", 21, 40, 70000, 240000, "Starting CTC ₹8 - 25 LPA", "https://ipindia.gov.in", "January", "May", "Patent Associate ➔ Senior IP Counsel ➔ Partner Tech IP Practice", [
    { title: "Degree in STEM + LL.B Law Degree", description: "Dual qualification in engineering/science and law." },
    { title: "Indian Patent Agent Examination", description: "Pass Patent Act 1970 and patent specification drafting papers." }
  ], ["Tech Patents", "High Hourly Billing", "IP Law"], 20000, 300, "MODERATE"),

  createCareer("gis-remote-sensing-analyst", "GIS & Satellite Remote Sensing Analyst (ISRO NRSC / Private)", "HIDDEN_GEM", "GOVT", "Core Engineering & Construction", "Analyze high-resolution satellite imagery, urban GIS planning, flood inundation models, and terrain mapping.", "GRADUATE", 21, 35, 55000, 120000, "Pay Level 7 or CTC ₹6 - 15 LPA", "https://nrsc.gov.in", "July", "September", "GIS Analyst ➔ Remote Sensing Specialist ➔ Lead Spatial Architect", [
    { title: "QGIS, ArcGIS & Google Earth Engine", description: "Master spatial data analysis, LiDAR raster processing, and Python GeoPandas." },
    { title: "Satellite Photogrammetry & Spectral Indices", description: "Calculate NDVI, thermal bands, and elevation contour maps." }
  ], ["Satellite Data", "GIS Mapping", "Smart Cities"], 40000, 400, "MODERATE")
];

export const ALL_BASELINE_CAREERS: CareerPath[] = [
  ...ELITE_CAREERS,
  ...STABLE_CAREERS,
  ...HIDDEN_GEM_CAREERS
];

export const FALLBACK_CAREER_PATHS: CareerPath[] = ALL_BASELINE_CAREERS;
