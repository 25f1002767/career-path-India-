"""
services/career_assessment_questions.py
==============================================================================
MPath Career Discovery & Assessment Question Bank
==============================================================================
Research-informed career exploration questions synthesized from:
- Holland's RIASEC vocational interest model (Realistic, Investigative, Artistic, Social, Enterprising, Conventional)
- Social Cognitive Career Theory (SCCT) by Lent, Brown & Hackett (Self-efficacy, Outcome expectations, Environmental supports/barriers)
- O*NET Career Exploration Dimensions (Work Activities, Work Styles, Work Values)
- Super's Career Development & Adaptability Theory
- Indian Secondary, Higher Secondary, and Vocational Career Realities

Principles:
1. Scenario-based, not generic school quiz.
2. Explores latent problem-solving affinity without revealing "obvious" career names.
3. Distinguishes Interest from Current Ability from Self-Efficacy (Confidence to master with practice).
4. Uncovers negative preferences (deal-breakers) and practical constraints.
5. Captures 14-16 high-information core scenarios.
"""

ASSESSMENT_VERSION = "2.0.0"

DISCOVERY_QUESTIONS = [
    {
        "id": "q1_curiosity_scenario",
        "category": "Curiosity & Problem Solving",
        "dimension": "RIASEC_PRIMARY",
        "prompt": "You are given an unfamiliar problem with three hours to explore it on your own. Which situation would keep you genuinely engaged even when the answer isn't immediately obvious?",
        "hint": "Choose the type of challenge that makes you curious rather than frustrated.",
        "options": [
            {
                "key": "A",
                "label": "Figuring out why a mechanical device, software system, or physical machine is malfunctioning.",
                "weights": {"R": 3.0, "I": 2.0},
                "problem_type": "technical_systems",
                "evidence": "You show strong curiosity for physical systems, technical troubleshooting, and understanding how things work."
            },
            {
                "key": "B",
                "label": "Investigating scientific data or clues to discover why an unexpected event or pattern occurred.",
                "weights": {"I": 3.5, "C": 1.0},
                "problem_type": "scientific_investigation",
                "evidence": "You are naturally drawn to hypothesis testing, scientific inquiry, and evidence-based analysis."
            },
            {
                "key": "C",
                "label": "Creating a compelling visual concept, story, or design to communicate an emotional message.",
                "weights": {"A": 3.5},
                "problem_type": "creative_expression",
                "evidence": "You naturally express ideas visually or creatively and enjoy shaping how people perceive concepts."
            },
            {
                "key": "D",
                "label": "Listening to a person who is struggling and helping them figure out a practical way forward.",
                "weights": {"S": 3.5},
                "problem_type": "human_development",
                "evidence": "You possess natural empathy, active listening patience, and an inclination toward helping individuals grow."
            },
            {
                "key": "E",
                "label": "Organizing people, resources, and timelines to turn a complex project into reality.",
                "weights": {"E": 3.0, "C": 1.5},
                "problem_type": "leadership_execution",
                "evidence": "You thrive when bringing structure to ambiguity, mobilizing teams, and driving measurable execution."
            },
            {
                "key": "F",
                "label": "Analyzing numerical trends, financial records, or policy documents to spot errors and ensure accuracy.",
                "weights": {"C": 3.5, "I": 1.0},
                "problem_type": "order_precision",
                "evidence": "You value precision, structured verification, and identifying patterns within structured data."
            }
        ]
    },
    {
        "id": "q2_flow_activity",
        "category": "Latent Interests & Energy",
        "dimension": "ENERGY_FLOW",
        "prompt": "Which activity could you spend an entire Saturday afternoon doing without anyone having to tell you to continue?",
        "hint": "Focus on what actually gives you energy rather than what you think sounds impressive.",
        "options": [
            {
                "key": "A",
                "label": "Assembling, fixing, or modifying physical tools, electronic circuits, or 3D models.",
                "weights": {"R": 3.0},
                "cluster": "Hands-on & Engineering",
                "evidence": "You lose track of time when working with tangible materials, mechanics, and physical craftsmanship."
            },
            {
                "key": "B",
                "label": "Deep-diving into research articles, documentaries, or coding tutorials to master a complex concept.",
                "weights": {"I": 3.0},
                "cluster": "Research & Technology",
                "evidence": "You enjoy self-directed learning and intellectual deep-dives into complex topics."
            },
            {
                "key": "C",
                "label": "Illustrating, shooting/editing video, writing stories, or designing visual graphics.",
                "weights": {"A": 3.0},
                "cluster": "Design & Media",
                "evidence": "Your energy flows into visual aesthetics, narrative creation, and creative experimentation."
            },
            {
                "key": "D",
                "label": "Teaching someone a concept they couldn't understand or mediating a conflict among peers.",
                "weights": {"S": 3.0},
                "cluster": "Teaching & Counselling",
                "evidence": "You find deep fulfillment in patient explanation, mentoring others, and human interpersonal support."
            },
            {
                "key": "E",
                "label": "Drafting a business plan, negotiating a deal, or managing an event's budget and publicity.",
                "weights": {"E": 3.0},
                "cluster": "Business & Management",
                "evidence": "You are stimulated by strategic negotiation, commerce, enterprise building, and public engagement."
            },
            {
                "key": "F",
                "label": "Organizing data catalogs, categorizing collections, or optimizing workflows for maximum efficiency.",
                "weights": {"C": 3.0},
                "cluster": "Analytics & Administration",
                "evidence": "You take satisfaction in systemizing chaos into structured, reliable, and auditable records."
            }
        ]
    },
    {
        "id": "q3_self_efficacy",
        "category": "Confidence & Growth Mindset",
        "dimension": "SELF_EFFICACY",
        "prompt": "When you encounter a challenging subject or skill that you are not initially good at, which response sounds most like your genuine inner belief?",
        "hint": "This measures your confidence in your ability to learn and adapt with sustained practice.",
        "options": [
            {
                "key": "A",
                "label": "I am confident that with disciplined, step-by-step practice, I can become skilled in almost any analytical or technical subject.",
                "weights": {"self_efficacy": 5, "I": 1.0, "R": 1.0},
                "efficacy_level": "high_analytical",
                "evidence": "You exhibit high cognitive self-efficacy and confidence in mastering rigorous technical domains."
            },
            {
                "key": "B",
                "label": "I excel most when learning through real-world trial, hands-on building, and physical demonstration rather than pure theory.",
                "weights": {"self_efficacy": 4, "R": 2.0},
                "efficacy_level": "hands_on_practical",
                "evidence": "You build mastery fastest through experiential, practical learning rather than abstract lecture formats."
            },
            {
                "key": "C",
                "label": "My confidence comes from human interaction, communication, and emotional connection rather than abstract equations.",
                "weights": {"self_efficacy": 4, "S": 2.0, "E": 1.0},
                "efficacy_level": "interpersonal",
                "evidence": "You demonstrate high social self-efficacy, excelling where empathy and verbal persuasion drive outcomes."
            },
            {
                "key": "D",
                "label": "I often feel intimidated by heavy mathematics or abstract coding, but I feel very capable with visual, creative, or language tasks.",
                "weights": {"self_efficacy": 3, "A": 2.0, "math_discomfort": True},
                "efficacy_level": "creative_verbal",
                "evidence": "You have strong self-efficacy in creative and expressive domains, with a preference for intuitive rather than heavy formulaic tasks."
            },
            {
                "key": "E",
                "label": "I am currently uncertain about my strengths and want to explore low-pressure avenues before committing to a hyper-specialized field.",
                "weights": {"self_efficacy": 2, "exploratory": True},
                "efficacy_level": "exploratory",
                "evidence": "You are currently in an exploratory stage, benefiting from broad foundational paths with flexible pivot points."
            }
        ]
    },
    {
        "id": "q4_work_values",
        "category": "Work Values & Driving Purpose",
        "dimension": "WORK_VALUES",
        "prompt": "When you imagine your career 10 years from now, which statement would make you feel that your hard work was genuinely worth the effort?",
        "hint": "There is no wrong answer. Knowing what drives you prevents career burnout.",
        "options": [
            {
                "key": "A",
                "label": "I built financial independence and strong income security that protects my family.",
                "weights": {"value_security": 3.0, "value_income": 3.0, "C": 1.0},
                "primary_value": "Financial Security & High Return",
                "evidence": "You place high value on financial stability, predictable earnings, and economic resilience."
            },
            {
                "key": "B",
                "label": "I directly healed, educated, or empowered vulnerable people and made society better.",
                "weights": {"value_impact": 4.0, "S": 2.0},
                "primary_value": "Social Impact & Helping Others",
                "evidence": "You are primarily motivated by altruism, civic contribution, and measurable human welfare."
            },
            {
                "key": "C",
                "label": "I became recognized as a premier expert who solved problems nobody else could crack.",
                "weights": {"value_mastery": 4.0, "I": 2.0},
                "primary_value": "Intellectual Mastery & Prestige",
                "evidence": "You value deep expertise, intellectual challenge, and the respect of professional peers."
            },
            {
                "key": "D",
                "label": "I built something of my own (a venture, studio, or enterprise) and had total freedom over my time.",
                "weights": {"value_autonomy": 4.0, "E": 2.0, "A": 1.0},
                "primary_value": "Autonomy & Entrepreneurship",
                "evidence": "You prioritize creative freedom, entrepreneurial agency, and steering your own destiny."
            },
            {
                "key": "E",
                "label": "I held a respected institutional role with clear structure, lifetime stability, and civic authority.",
                "weights": {"value_stability": 4.0, "value_prestige": 3.0, "C": 1.5, "E": 1.0},
                "primary_value": "Institutional Stability & Public Honor",
                "evidence": "You value institutional longevity, public respect, and well-defined service frameworks."
            }
        ]
    },
    {
        "id": "q5_problem_type",
        "category": "Problem Archetype",
        "dimension": "PROBLEM_AFFINITY",
        "prompt": "If a national foundation funded you to work on ONE category of real-world problems for a year, which mission would excite you most?",
        "hint": "This identifies the societal impact sector you naturally gravitate toward.",
        "options": [
            {
                "key": "A",
                "label": "Developing cutting-edge software, algorithms, or automated systems that make industries 10x faster.",
                "weights": {"Technology": 4.0, "I": 2.0, "R": 1.0},
                "domain_affinity": "Technology & Computer Science",
                "evidence": "You enjoy technological transformation, digital architecture, and algorithmic automation."
            },
            {
                "key": "B",
                "label": "Combating disease, improving clinical therapies, or enhancing community public health.",
                "weights": {"Healthcare": 4.0, "I": 2.0, "S": 2.0},
                "domain_affinity": "Healthcare & Medical Sciences",
                "evidence": "You are drawn to healthcare solutions, biological discovery, and clinical patient outcomes."
            },
            {
                "key": "C",
                "label": "Designing physical infrastructure, clean energy grids, robotics, or advanced mobility.",
                "weights": {"Engineering": 4.0, "R": 3.0, "I": 1.0},
                "domain_affinity": "Engineering & Manufacturing",
                "evidence": "You are inspired by tangible engineering, energy systems, and modern infrastructure."
            },
            {
                "key": "D",
                "label": "Defending legal rights, advocating justice, or formulating ethical public policy and governance.",
                "weights": {"Law": 4.0, "Government": 3.0, "E": 2.0, "S": 1.0},
                "domain_affinity": "Law & Legal Services",
                "evidence": "You care about legal frameworks, ethical adjudication, and public constitutional rights."
            },
            {
                "key": "E",
                "label": "Analyzing markets, managing capital investments, or scaling sustainable commercial enterprises.",
                "weights": {"Finance": 4.0, "Business": 3.0, "C": 2.0, "E": 2.0},
                "domain_affinity": "Finance, Banking & Accounting",
                "evidence": "You have a natural mind for capital allocation, economic systems, and enterprise growth."
            },
            {
                "key": "F",
                "label": "Revitalizing agriculture, protecting wildlife and forests, or solving water and climate crises.",
                "weights": {"Agriculture": 4.0, "R": 2.0, "I": 2.0},
                "domain_affinity": "Agriculture, Food Technology & Environment",
                "evidence": "You feel an affinity for environmental ecosystems, food security, and natural resource stewardship."
            },
            {
                "key": "G",
                "label": "Creating films, multimedia experiences, architecture, or game worlds that inspire millions.",
                "weights": {"Design": 4.0, "A": 4.0},
                "domain_affinity": "Design, Animation & Creative Arts",
                "evidence": "You are driven by aesthetics, storytelling, and cultural or spatial design."
            }
        ]
    },
    {
        "id": "q6_work_environment",
        "category": "Work Style & Environment",
        "dimension": "ENVIRONMENT_FIT",
        "prompt": "Which physical day-to-day working environment do you think fits your temperament and energy best?",
        "hint": "Consider where you will feel productive 40 hours a week.",
        "options": [
            {
                "key": "A",
                "label": "A collaborative technology campus or corporate office with modern equipment and teams.",
                "weights": {"env_office": 3.0, "E": 1.0, "C": 1.0},
                "environment_code": "Office / Corporate",
                "evidence": "You prefer professional, well-equipped office spaces with structured team interaction."
            },
            {
                "key": "B",
                "label": "A hospital, diagnostic laboratory, or research institute where hygiene and scientific rigor matter.",
                "weights": {"env_lab": 4.0, "I": 2.0},
                "environment_code": "Hospital / Laboratory",
                "evidence": "You thrive in clinical, scientific, or laboratory environments requiring focus and precision."
            },
            {
                "key": "C",
                "label": "Out in the field, outdoors, visiting project sites, wildlife zones, or communities on the move.",
                "weights": {"env_field": 4.0, "R": 2.0},
                "environment_code": "Field Work / Outdoors",
                "evidence": "You prefer dynamic, mobile work in the open field rather than being bound to a desk all day."
            },
            {
                "key": "D",
                "label": "A creative studio, workshop, or fabrication space surrounded by design tools and prototypes.",
                "weights": {"env_studio": 4.0, "A": 2.0, "R": 1.0},
                "environment_code": "Studio / Workshop",
                "evidence": "You thrive in creative maker spaces, studios, or workshops with freedom to iterate."
            },
            {
                "key": "E",
                "label": "A quiet remote or hybrid desk with deep focus, autonomy over hours, and minimal bureaucracy.",
                "weights": {"env_remote": 4.0, "I": 1.0, "C": 1.0},
                "environment_code": "Remote / Independent",
                "evidence": "You value asynchronous autonomy, independent focus, and flexibility over work locations."
            }
        ]
    },
    {
        "id": "q7_failure_and_persistence",
        "category": "Career Adaptability & Resilience",
        "dimension": "ADAPTABILITY",
        "prompt": "When a project or academic preparation you care about encounters a major setback, what is your most common reaction?",
        "hint": "This reveals your cognitive persistence style when navigating difficult career thresholds.",
        "options": [
            {
                "key": "A",
                "label": "I break the problem down into small pieces, research alternative methodologies, and keep testing until it works.",
                "weights": {"persistence": 4, "I": 2.0},
                "style": "Analytical Problem Solver",
                "evidence": "You approach roadblocks systematically through analytical deconstruction and relentless testing."
            },
            {
                "key": "B",
                "label": "I seek out a mentor or someone with more experience, discuss where I went wrong, and implement their feedback.",
                "weights": {"adaptability": 4, "S": 2.0},
                "style": "Collaborative Learner",
                "evidence": "You accelerate recovery from setbacks by proactively seeking mentorship and collaborative insight."
            },
            {
                "key": "C",
                "label": "I discard the conventional approach and attempt a radically different, creative angle.",
                "weights": {"creativity": 3, "A": 2.0, "E": 1.0},
                "style": "Creative Pivoter",
                "evidence": "You instinctively pivot toward unconventional solutions rather than forcing rigid methods."
            },
            {
                "key": "D",
                "label": "I can feel discouraged if the barrier is high, so having a clear roadmap and predictable milestones helps me stay on track.",
                "weights": {"need_structure": 3, "C": 2.0},
                "style": "Structured Step-by-Step",
                "evidence": "You perform best with explicit milestones, structured accountability, and low-ambiguity roadmaps."
            }
        ]
    },
    {
        "id": "q8_study_investment_tolerance",
        "category": "Education Investment & Timeline",
        "dimension": "STUDY_TOLERANCE",
        "prompt": "How do you honestly feel about the duration and intensity of academic study required before you start working?",
        "hint": "Different careers demand vastly different preparation timelines.",
        "options": [
            {
                "key": "A",
                "label": "I am fully ready to commit 5.5 to 8+ years of intense academic study (e.g., MBBS + MD, PhD research, CA, Super-specializations) for high-mastery careers.",
                "weights": {"study_tolerance": 5, "I": 2.0},
                "tolerance_level": "very_high",
                "evidence": "You are prepared for long-duration, rigorous academic qualifications."
            },
            {
                "key": "B",
                "label": "A standard 3 to 4 year undergraduate degree (B.Tech, B.Sc, B.Com, BA, BCA, B.Des) followed immediately by work or internship is ideal.",
                "weights": {"study_tolerance": 3},
                "tolerance_level": "moderate",
                "evidence": "You prefer a standard 3-4 year degree pathway that leads promptly into the workforce."
            },
            {
                "key": "C",
                "label": "I want to start earning as early as possible (within 1 to 3 years) through a Diploma, vocational course, ITI, or skill certificate.",
                "weights": {"study_tolerance": 1, "R": 2.0, "earn_early": True},
                "tolerance_level": "early_entry",
                "evidence": "You value rapid workforce entry, hands-on skill credentials, and early financial contribution."
            },
            {
                "key": "D",
                "label": "I prefer starting with a solid foundation degree, working for 2 years, and then pursuing specialized executive or postgraduate studies.",
                "weights": {"study_tolerance": 3, "E": 1.0},
                "tolerance_level": "progressive",
                "evidence": "You favor phased progression: foundational degree first, workplace experience, then targeted higher study."
            }
        ]
    },
    {
        "id": "q9_exam_tolerance",
        "category": "Competitive Exam Tolerance",
        "dimension": "EXAM_TOLERANCE",
        "prompt": "What is your comfort level regarding high-stakes, competitive entrance exams (such as UPSC CSE, NEET, JEE Advanced, CAT, State PSCs) where selection rates are below 1%?",
        "hint": "This helps determine whether exam-first pathways or skill/portfolio pathways are better suited for you.",
        "options": [
            {
                "key": "A",
                "label": "I am eager and willing to dedicate 1-2 years of intensive, isolated competitive preparation.",
                "weights": {"exam_tolerance": 5, "Government": 3.0, "C": 1.0},
                "exam_profile": "high_competitive",
                "evidence": "You possess the appetite and discipline required for rigorous competitive examination marathons."
            },
            {
                "key": "B",
                "label": "I am open to attempting competitive exams, but I MUST have a strong alternative degree/career backup ready.",
                "weights": {"exam_tolerance": 3, "balanced": True},
                "exam_profile": "balanced_with_backup",
                "evidence": "You have a pragmatic perspective: willing to attempt competitive exams while maintaining safe parallel pathways."
            },
            {
                "key": "C",
                "label": "I prefer admissions and hiring based on continuous college marks, technical interviews, and practical skills.",
                "weights": {"exam_tolerance": 2, "skill_first": True},
                "exam_profile": "skill_and_interview",
                "evidence": "You prefer merit pathways determined by practical competency, academic GPA, and technical interviews."
            },
            {
                "key": "D",
                "label": "I strongly dislike written competitive testing; I want my work, design portfolio, or projects to speak for me.",
                "weights": {"exam_tolerance": 1, "A": 2.0, "portfolio_first": True},
                "exam_profile": "portfolio_driven",
                "evidence": "You excel in demonstration-driven domains where creative portfolios or coding repositories outweigh standardized tests."
            }
        ]
    },
    {
        "id": "q10_family_expectations",
        "category": "Social & Family Context",
        "dimension": "FAMILY_CONTEXT",
        "prompt": "Which of these matters most when your family thinks about your future career?",
        "hint": "Understanding external expectations helps us identify harmonious paths that satisfy both you and your family.",
        "options": [
            {
                "key": "A",
                "label": "Lifetime job security, pension, or a respected government/public-sector designation.",
                "weights": {"family_gov": 3.0, "Government": 2.0},
                "context": "Security & Government Service",
                "evidence": "Your family values institutional stability, pension protections, and government service dignity."
            },
            {
                "key": "B",
                "label": "A prestigious professional title (Doctor, Engineer, CA, Advocate, Architect).",
                "weights": {"family_prestige": 3.0},
                "context": "Recognized Professional Title",
                "evidence": "Your family places priority on time-tested, socially prestigious professional identities."
            },
            {
                "key": "C",
                "label": "High financial earning potential and quick return on education investment.",
                "weights": {"family_income": 3.0, "Finance": 1.0, "Technology": 1.0},
                "context": "Economic Mobility & High Income",
                "evidence": "Your family emphasizes strong economic returns and upward financial mobility."
            },
            {
                "key": "D",
                "label": "Staying geographically close to home or in our home state.",
                "weights": {"family_location": 3.0, "stay_local": True},
                "context": "Geographic Proximity & Home Base",
                "evidence": "Family continuity and remaining close to home or regional centers is a valued constraint."
            },
            {
                "key": "E",
                "label": "They fully trust and support whatever path makes me fulfilled and intellectually engaged.",
                "weights": {"family_support": 4.0},
                "context": "Full Autonomous Support",
                "evidence": "You enjoy strong family support for self-determined, passion-aligned career exploration."
            }
        ]
    },
    {
        "id": "q11_financial_constraints",
        "category": "Practical Feasibility & Funding",
        "dimension": "FINANCIAL_REALITY",
        "prompt": "What is your financial situation regarding funding higher education and training?",
        "hint": "This ensures we highlight fee-free pathways, scholarships, government colleges, and bank loan feasibility.",
        "options": [
            {
                "key": "A",
                "label": "We need affordable, low-fee options (Government colleges, state universities, or ITIs) and scholarship support.",
                "weights": {"need_scholarships": True, "low_cost": True},
                "budget_tier": "low_cost_scholarship",
                "evidence": "We prioritize government-subsidized universities, merit scholarships, and affordable tuition pathways."
            },
            {
                "key": "B",
                "label": "Moderate fees are manageable, or we are willing to take an education loan for high-placement professional courses.",
                "weights": {"moderate_cost": True, "loan_feasible": True},
                "budget_tier": "moderate_loan_eligible",
                "evidence": "Moderate tuition programs with clear ROI or educational loan viability are well-suited."
            },
            {
                "key": "C",
                "label": "I must start earning within 2 to 3 years to support my family financially.",
                "weights": {"earn_early": True, "low_cost": True},
                "budget_tier": "earn_early_urgent",
                "evidence": "High career urgency; we emphasize direct-employment diplomas, apprentice schemes, and early-paying roles."
            },
            {
                "key": "D",
                "label": "Tuition costs are not a primary constraint; we can comfortably invest in long or specialized private/international degrees.",
                "weights": {"high_investment": True},
                "budget_tier": "flexible_investment",
                "evidence": "Financial constraints are minimal, opening elite private and multi-year training pathways."
            }
        ]
    },
    {
        "id": "q12_current_academic_level",
        "category": "Academic Background",
        "dimension": "ELIGIBILITY_BASELINE",
        "prompt": "What is your current academic stage and stream?",
        "hint": "This establishes your immediate entry qualifications.",
        "options": [
            {
                "key": "A",
                "label": "Class 10 (Exploring stream selection for Class 11)",
                "stream": "Class 10 General",
                "level": "Class 10",
                "evidence": "You are at a pivotal stream-selection milestone where broad exploratory roadmaps are most valuable."
            },
            {
                "key": "B",
                "label": "Class 11 / 12 - Science (PCM / Physics, Chemistry, Math)",
                "stream": "Science (PCM)",
                "level": "Class 12",
                "evidence": "Your foundation in Physics, Chemistry, and Mathematics qualifies you for engineering, physical sciences, analytics, and architecture."
            },
            {
                "key": "C",
                "label": "Class 11 / 12 - Science (PCB / Physics, Chemistry, Biology)",
                "stream": "Science (PCB)",
                "level": "Class 12",
                "evidence": "Your foundation in Biology and Chemistry unlocks medicine, allied health sciences, biotechnology, and agricultural science."
            },
            {
                "key": "D",
                "label": "Class 11 / 12 - Commerce (with or without Math)",
                "stream": "Commerce",
                "level": "Class 12",
                "evidence": "Your foundation in commerce and finance opens chartered accountancy, corporate banking, economics, and business analytics."
            },
            {
                "key": "E",
                "label": "Class 11 / 12 - Humanities / Arts",
                "stream": "Arts",
                "level": "Class 12",
                "evidence": "Your foundation in humanities and social sciences enables law, civil services, psychology, media, and design."
            },
            {
                "key": "F",
                "label": "Polytechnic Diploma / ITI / Vocational Student",
                "stream": "Diploma",
                "level": "Diploma",
                "evidence": "Your technical diploma background offers lateral-entry degree bridges and skilled engineering pathways."
            },
            {
                "key": "G",
                "label": "Undergraduate Student / Recent Graduate",
                "stream": "Undergraduate",
                "level": "Undergraduate",
                "evidence": "You already hold higher educational credits and can target direct placements, competitive exams, or master's degrees."
            }
        ]
    },
    {
        "id": "q13_academic_strengths",
        "category": "Academic Strengths & Comfort",
        "dimension": "STRENGTH_ALIGNMENT",
        "prompt": "Which subject domain do you naturally grasp with the least friction or highest intuitive comfort?",
        "hint": "What feels natural to you, even if you don't always get top exam marks in it?",
        "options": [
            {
                "key": "A",
                "label": "Mathematics, Logic, Patterns & Quantitative Reasoning",
                "weights": {"strength_math": 3.0, "I": 2.0, "C": 1.0},
                "domain": "Quantitative & Logical",
                "evidence": "You possess natural quantitative intuition and comfort with mathematical abstractions."
            },
            {
                "key": "B",
                "label": "Life Sciences, Biology, Human Body & Ecological Systems",
                "weights": {"strength_bio": 3.0, "I": 2.0, "S": 1.0},
                "domain": "Biological & Ecological",
                "evidence": "You naturally absorb living systems, physiological mechanisms, and organic relationships."
            },
            {
                "key": "C",
                "label": "Languages, Literature, Debating & Persuasive Writing",
                "weights": {"strength_lang": 3.0, "A": 2.0, "S": 1.0, "E": 1.0},
                "domain": "Verbal & Communication",
                "evidence": "You have strong command of language, rhetoric, conceptual framing, and verbal expression."
            },
            {
                "key": "D",
                "label": "Economics, Business Trends, Commerce & Financial Ledger Logic",
                "weights": {"strength_commerce": 3.0, "C": 2.0, "E": 1.0},
                "domain": "Economic & Commercial",
                "evidence": "You understand market mechanics, commercial value chains, and economic principles with ease."
            },
            {
                "key": "E",
                "label": "Social Sciences, History, Human Behavior & Geopolitical Dynamics",
                "weights": {"strength_social": 3.0, "S": 2.0, "I": 1.0},
                "domain": "Social & Behavioral",
                "evidence": "You are attuned to human societies, historical context, social behavior, and political structures."
            },
            {
                "key": "F",
                "label": "Visual Arts, Spatial Reasoning, Design & 3D Construction",
                "weights": {"strength_spatial": 3.0, "A": 2.5, "R": 1.5},
                "domain": "Spatial & Creative",
                "evidence": "You have keen visual-spatial intuition, 3D imagination, and aesthetic perception."
            }
        ]
    },
    {
        "id": "q14_negative_preferences",
        "category": "Anti-Preferences & Deal Breakers",
        "dimension": "NEGATIVE_CONSTRAINTS",
        "prompt": "Which of these conditions would you STRONGLY DISLIKE having in your day-to-day career for the next 10 years?",
        "hint": "Identifying what you refuse to do is just as important as discovering what you like.",
        "options": [
            {
                "key": "A",
                "label": "Sitting at an isolated computer desk all day doing repetitive coding or spreadsheet data entry.",
                "dislike": "repetitive_desk_work",
                "penalty_clusters": ["Data", "Software", "Accounting"],
                "evidence": "You strongly dislike sedentary, isolated desk routines with repetitive screen time."
            },
            {
                "key": "B",
                "label": "Dealing with aggressive sales quotas, cold-calling, or constant commercial persuasion.",
                "dislike": "aggressive_sales",
                "penalty_clusters": ["Sales", "Business Development", "Real Estate"],
                "evidence": "You are averse to hard-sell commercial quotas and transactional persuasion."
            },
            {
                "key": "C",
                "label": "Dealing with blood, clinical surgery, patient emergencies, or hospital environments.",
                "dislike": "clinical_medical",
                "penalty_clusters": ["Doctor", "Surgeon", "Dentist", "Emergency Care"],
                "evidence": "You wish to avoid invasive clinical exposure, acute trauma, and hospital ward routines."
            },
            {
                "key": "D",
                "label": "Strenuous physical labor outdoors in extreme weather conditions (dust, heat, construction).",
                "dislike": "strenuous_outdoor",
                "penalty_clusters": ["Mining", "Field Construction", "Manual Agriculture"],
                "evidence": "You prefer clean, temperature-controlled indoor environments over harsh physical outdoor labor."
            },
            {
                "key": "E",
                "label": "Constant public speaking, stage appearances, or frequent contentious arguments.",
                "dislike": "constant_public_conflict",
                "penalty_clusters": ["Litigation Lawyer", "Television Journalism", "High-frequency Public Speaking"],
                "evidence": "You prefer measured, non-confrontational or written forms of communication."
            },
            {
                "key": "F",
                "label": "Unpredictable income without a fixed monthly salary (e.g. pure commission or high-risk startups).",
                "dislike": "unpredictable_income",
                "penalty_clusters": ["Freelancing", "Early Startup Founder", "Commission Brokerage"],
                "evidence": "You have a low tolerance for volatile compensation and require dependable monthly income."
            }
        ]
    },
    {
        "id": "q15_decision_making_style",
        "category": "Decision-Making Style",
        "dimension": "DECISION_STYLE",
        "prompt": "When making an important life or career decision, what gives you the greatest confidence to move forward?",
        "hint": "This helps us tailor your recommendation explanations.",
        "options": [
            {
                "key": "A",
                "label": "Clear empirical data, placement statistics, syllabus transparency, and verified facts.",
                "style": "Empirical & Data-Driven",
                "weights": {"I": 1.5, "C": 1.5},
                "evidence": "You trust structured data, statistical evidence, and transparent facts above emotional hype."
            },
            {
                "key": "B",
                "label": "Personal guidance from trusted mentors, senior professionals, and family elders.",
                "style": "Mentor & Elder Guided",
                "weights": {"S": 2.0},
                "evidence": "You place high value on seasoned counsel, lived wisdom, and trusted human guidance."
            },
            {
                "key": "C",
                "label": "Hands-on trial: doing a mini-project, shadowing a workplace, or talking to someone working the job.",
                "style": "Experiential & Experimental",
                "weights": {"R": 1.5, "A": 1.0},
                "evidence": "You learn best by direct contact, short experiments, and experiencing the environment firsthand."
            },
            {
                "key": "D",
                "label": "Inner alignment with what feels deeply meaningful, authentic, and socially purposeful.",
                "style": "Purpose & Value-Driven",
                "weights": {"A": 1.5, "S": 1.5},
                "evidence": "Your north star is internal alignment, moral authenticity, and social meaning."
            }
        ]
    },
    {
        "id": "q16_open_reflection",
        "category": "Student Voice & Unstructured Evidence",
        "dimension": "STUDENT_VOICE",
        "prompt": "In one or two sentences, tell us about something you can talk about for hours without getting tired, or a project you completed that made you feel proud.",
        "hint": "Optional reflection. Our engine uses this to detect latent passions and cross-domain connections.",
        "is_text": True,
        "placeholder": "e.g. 'I built a small weather station with Arduino' or 'I love organizing school debate tournaments' or 'I spend hours reading about how brain chemistry influences habits...'"
    }
]


def get_question_by_id(question_id: str):
    """Retrieve question definition by ID"""
    for q in DISCOVERY_QUESTIONS:
        if q["id"] == question_id:
            return q
    return None
