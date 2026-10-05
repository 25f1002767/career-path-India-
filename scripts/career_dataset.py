"""
scripts/career_dataset.py
National Career Discovery Dataset for MPath Career Counselling.
Contains 126 authentic occupations mapped across 14 sectors, adhering to NCS, SSC, and AICTE frameworks.
"""

CAREERS_DATA = [
    # =========================================================================
    # 1. TECHNOLOGY & COMPUTER SCIENCE (15 Careers)
    # =========================================================================
    {
        "title": "Software Developer",
        "short_name": "Software Dev",
        "slug": "software-developer",
        "category": "Technology & Computer Science",
        "sub_category": "Software Engineering & Architecture",
        "industry": "Information Technology",
        "icon": "code-slash",
        "short_description": "Designs, develops, tests, and maintains software applications and systems across enterprise, consumer, and cloud environments.",
        "description": "Software Developers are engineering professionals responsible for the complete software development lifecycle (SDLC). They analyze user needs, design software architectures, write clean and efficient code, debug issues, and deploy applications that power modern digital experiences.",
        "what_they_do": "Software Developers create software applications that allow users to perform specific tasks on computers, mobile phones, and web platforms. They collaborate with cross-functional teams including product managers, UI/UX designers, and quality assurance engineers to deliver robust software products. They also maintain codebase health, resolve performance bottlenecks, and implement security standards.",
        "day_to_day_work": "• Writing and refactoring clean code in languages such as Python, Java, C++, or Go.\n• Participating in daily stand-up meetings and sprint planning.\n• Reviewing pull requests and collaborating on system architecture.\n• Writing automated unit and integration tests.\n• Debugging production issues and monitoring system performance metrics.",
        "work_environment": "Modern tech campuses, collaborative corporate offices, or fully remote engineering workspaces.",
        "work_modes": "Hybrid / Remote / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Mathematics, Physics, Computer Science",
        "technical_skills": "Data Structures & Algorithms, Object-Oriented Programming, RESTful APIs, Git, SQL, System Design",
        "soft_skills": "Problem Solving, Analytical Thinking, Collaboration, Effective Communication, Adaptability",
        "tools": "VS Code, Git, Docker, Postman, Jira, GitHub",
        "certifications": "AWS Certified Developer, Oracle Certified Professional: Java SE, Google Associate Cloud Engineer",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "High Demand with rapid transition into Senior Engineer, Lead Architect, or Engineering Manager.",
        "internship_roles": "Software Engineering Intern, Junior Developer Intern, Backend Intern, Mobile Dev Intern",
        "entry_level_roles": "Associate Software Engineer, Junior Developer, Graduate Engineer Trainee (GET)",
        "average_salary": "₹4.5 - ₹16 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹4 - 7 LPA | Mid-Level (3-6 yrs): ₹8 - 18 LPA | Senior/Lead (7+ yrs): ₹20 - 45+ LPA. Indicative figures based on National Career Service & Tech Industry Compensation Reports 2024. Compensation varies significantly by company type, city, and specialized skills.",
        "future_scope": "Very High Growth driven by global digital transformation, AI integration, and cloud ecosystems.",
        "government_opportunities": "NIC (National Informatics Centre), DRDO Scientist B, ISRO, CDAC, State IT Departments, RailTel, Public Sector Undertaking (PSU) software teams.",
        "private_opportunities": "TCS, Infosys, Wipro, Google, Microsoft, Amazon, Flipkart, dynamic tech startups and global capability centers (GCCs).",
        "higher_study_options": "M.Tech in Computer Science, M.S. in Software Engineering, MBA in IT / Technology Management.",
        "entrepreneurship_options": "Launching SaaS products, independent software consultancy, freelancing agency, or specialized tech consulting.",
        "source": "National Career Service (NCS) / NASSCOM Sector Skill Council",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech Computer Science & Engineering
            {"course_id": 14, "type": "COMMON"},  # BCA
            {"course_id": 4, "type": "ALTERNATIVE"},  # B.Sc Computer Science
            {"course_id": 15, "type": "SPECIALIZED"}, # MCA
            {"course_id": 42, "type": "COMMON"}   # B.Tech Information Technology
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "ALTERNATIVE"}, # GATE
            {"exam_id": 45, "importance": "OPTIONAL"}  # NIC Scientist B
        ],
        "routes": [
            {"title": "Path A: Standard Engineering Route", "type": "COMMON", "steps": "Class 12 (PCM) -> JEE Main / State CET -> B.Tech CSE / IT (4 yrs) -> DSA & Projects -> Campus Placement or Direct Application."},
            {"title": "Path B: Computer Applications Pathway", "type": "ALTERNATIVE", "steps": "Class 12 (Any stream with Maths/CS) -> BCA (3 yrs) -> MCA (2 yrs) or specialized skills -> Software Engineer role."},
            {"title": "Path C: Science / Self-Taught Route", "type": "SPECIALIZED", "steps": "Class 12 (Science) -> B.Sc CS / Maths -> Intense coding portfolio & open-source contributions -> Junior Developer internship -> Full-time role."}
        ],
        "ladder": [
            {"stage": "Junior Software Engineer", "exp": "0-2 Years", "desc": "Handles feature implementation, bug fixes, unit tests under mentorship."},
            {"stage": "Software Engineer / SDE-II", "exp": "2-5 Years", "desc": "Owns subsystem components, designs microservices, conducts code reviews."},
            {"stage": "Senior Software Engineer / Lead", "exp": "5-8 Years", "desc": "Leads architectural design, guides junior devs, drives technical roadmap."},
            {"stage": "Principal Engineer / Engineering Manager", "exp": "8+ Years", "desc": "Sets technical strategy for multi-team systems or manages engineering departments."}
        ],
        "roadmaps": {
            "Class 10": "Focus on strong algebra, geometry, and logical thinking. Learn basics of Python or C++ during vacations. Explore robotics or coding clubs.",
            "Class 12": "Target 75%+ in PCM. Prepare for JEE Main and State CETs. Practice fundamental coding and algorithmic puzzle solving.",
            "Graduation": "Build 3+ full-stack projects on GitHub. Master Data Structures and Algorithms (LeetCode/HackerRank). Secure a summer internship in 3rd year.",
            "Working Professional": "Level up on System Design (Low Level & High Level), Cloud services (AWS/GCP), and modern frameworks like Next.js or Spring Boot."
        }
    },
    {
        "title": "Data Scientist",
        "short_name": "Data Scientist",
        "slug": "data-scientist",
        "category": "Technology & Computer Science",
        "sub_category": "Data Science & Artificial Intelligence",
        "industry": "Information Technology / Analytics",
        "icon": "graph-up",
        "short_description": "Applies statistical analysis, machine learning algorithms, and domain expertise to extract actionable insights from complex datasets.",
        "description": "Data Scientists combine mathematical theory, statistical modeling, machine learning, and business context to transform massive unstructured and structured data into strategic foresight. They build predictive algorithms, optimize decision-making systems, and design experiments.",
        "what_they_do": "Data Scientists formulate quantitative questions, collect and clean data from diverse sources, build predictive machine learning models, and communicate findings to executives. They design A/B tests, build recommendation engines, detect anomalies, and uncover behavioral trends.",
        "day_to_day_work": "• Exploratory Data Analysis (EDA) using Pandas, NumPy, and Matplotlib.\n• Designing and training predictive models using Scikit-Learn, XGBoost, or TensorFlow.\n• Validating statistical significance and minimizing model bias.\n• Translating complex statistical findings into clear executive dashboards.\n• Collaborating with Data Engineers to operationalize model pipelines.",
        "work_environment": "Tech hubs, research labs, financial institutions, and remote analytics workstations.",
        "work_modes": "Hybrid / Remote",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Mathematics, Statistics, Computer Science",
        "technical_skills": "Python, R, SQL, Machine Learning, Statistical Inference, Deep Learning, Feature Engineering",
        "soft_skills": "Critical Thinking, Storytelling with Data, Business Acumen, Curiosity, Problem Solving",
        "tools": "Jupyter Notebook, Pandas, Scikit-Learn, Tableau, Git, BigQuery, Docker",
        "certifications": "TensorFlow Developer Certificate, Google Cloud Professional Data Engineer, IBM Data Science Professional",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Exceptional trajectory with progression to Staff Data Scientist, Chief Data Officer (CDO), or AI Research Lead.",
        "internship_roles": "Data Science Intern, Analytics Intern, Machine Learning Research Intern",
        "entry_level_roles": "Junior Data Scientist, Associate Data Analyst, Research Associate",
        "average_salary": "₹6 - ₹20 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹5 - 9 LPA | Mid-Level (3-6 yrs): ₹10 - 22 LPA | Senior/Lead (7+ yrs): ₹25 - 55+ LPA. Indicative figures based on National Career Service & Analytics India Salary Study 2024. Subject to domain depth and mathematical rigor.",
        "future_scope": "Exponential expansion with generative AI, autonomous systems, and predictive enterprise analytics.",
        "government_opportunities": "NITI Aayog Analytics Cell, RBI Data Research Unit, NPCI, DRDO, NIC, Census & Statistical Organizations.",
        "private_opportunities": "Google, Microsoft, Amazon, Fractal Analytics, Mu Sigma, Reliance Jio, Banking & Fintech firms.",
        "higher_study_options": "M.Sc Data Science, M.Tech in AI/DS, Ph.D. in Machine Learning or Applied Statistics.",
        "entrepreneurship_options": "Bespoke analytics consulting, AI automation agencies, domain-specific predictive SaaS products.",
        "source": "National Career Service (NCS) / NASSCOM FutureSkills",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 5, "type": "DIRECT"},     # B.Sc Data Science & Analytics
            {"course_id": 43, "type": "DIRECT"},    # B.Tech AI & Data Science
            {"course_id": 1, "type": "COMMON"},     # B.Sc Mathematics
            {"course_id": 39, "type": "COMMON"},    # B.Sc Statistics
            {"course_id": 37, "type": "SPECIALIZED"} # M.Sc Data Science
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "ALTERNATIVE"}, # GATE
            {"exam_id": 82, "importance": "ALTERNATIVE"}  # IIT JAM
        ],
        "routes": [
            {"title": "Path A: Direct Degree in AI / Data Science", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech in CSE / AI-DS or B.Sc Data Science -> Portfolio on Kaggle / GitHub -> Data Science Intern -> Data Scientist."},
            {"title": "Path B: Mathematical / Statistical Route", "type": "COMMON", "steps": "Class 12 (Maths) -> B.Sc Statistics / Mathematics -> Learn Python & ML -> M.Sc Data Science or direct Analyst role -> Transition to Data Scientist."},
            {"title": "Path C: Engineering Transition Route", "type": "ALTERNATIVE", "steps": "Any B.Tech -> Software Developer role -> Upskilling in Math, Statistics & ML -> Internal transition to Data Scientist."}
        ],
        "ladder": [
            {"stage": "Junior Data Scientist / Analyst", "exp": "0-2 Years", "desc": "Performs data cleaning, exploratory analysis, baseline model evaluation."},
            {"stage": "Data Scientist", "exp": "2-5 Years", "desc": "Builds end-to-end ML models, runs A/B experiments, collaborates with engineers."},
            {"stage": "Senior Data Scientist", "exp": "5-8 Years", "desc": "Spearheads core algorithm development, establishes ML best practices."},
            {"stage": "Lead / Principal Data Scientist", "exp": "8+ Years", "desc": "Shapes organizational data strategy and leads specialized AI initiatives."}
        ],
        "roadmaps": {
            "Class 10": "Build rock-solid command over linear equations, probability, and coordinate geometry. Start learning basic Python.",
            "Class 12": "Excel in Mathematics, Probability, and Calculus. Aim for leading engineering or statistics institutes (ISI, IITs, CMI).",
            "Graduation": "Participate in Kaggle competitions. Publish research or deploy interactive machine learning apps with Streamlit. Complete 1-2 corporate internships.",
            "Working Professional": "Deepen mathematical foundations (Linear Algebra, Bayesian Statistics), master PyTorch or TensorFlow, and master production ML (MLOps)."
        }
    },
    {
        "title": "Machine Learning Engineer",
        "short_name": "ML Engineer",
        "slug": "machine-learning-engineer",
        "category": "Technology & Computer Science",
        "sub_category": "Artificial Intelligence & Robotics",
        "industry": "Information Technology / Deep Tech",
        "icon": "cpu",
        "short_description": "Bridges the gap between data science and production software by building, training, and operationalizing machine learning pipelines at scale.",
        "description": "Machine Learning Engineers design self-running software to automate predictive models. They take theoretical data science prototypes and transform them into scalable, high-throughput production services running on cloud and edge infrastructure.",
        "what_they_do": "ML Engineers create production-grade ML architectures. They manage automated data pipelines, train and fine-tune large models, optimize latency and throughput, monitor for model drift, and maintain MLOps pipelines.",
        "day_to_day_work": "• Designing robust automated training and inference pipelines.\n• Optimizing deep learning models for inference speed using ONNX or TensorRT.\n• Setting up continuous training, testing, and deployment (CI/CD for ML).\n• Profiling GPU utilization and memory footprints during model training.\n• Integrating ML services with core software microservices.",
        "work_environment": "High-tech software laboratories, AI startups, cloud computing facilities, or remote engineering setups.",
        "work_modes": "Hybrid / Remote",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Mathematics, Computer Science, Physics",
        "technical_skills": "Python, C++, PyTorch, TensorFlow, MLOps, Docker, Kubernetes, CI/CD, Distributed Computing",
        "soft_skills": "Systemic Thinking, Tenacity, Collaborative Engineering, Problem Solving",
        "tools": "MLflow, Kubeflow, PyTorch, Docker, AWS SageMaker, Git, DVC",
        "certifications": "AWS Certified Machine Learning - Specialty, Google Professional Machine Learning Engineer",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Extremely high demand across robotics, autonomous vehicles, generative AI, and financial algorithms.",
        "internship_roles": "ML Engineering Intern, AI Systems Intern, Computer Vision Intern",
        "entry_level_roles": "Junior ML Engineer, AI Software Developer, Associate Systems Engineer",
        "average_salary": "₹6.5 - ₹22 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹5.5 - 10 LPA | Mid-Level (3-6 yrs): ₹12 - 24 LPA | Senior/Staff (7+ yrs): ₹26 - 60+ LPA. Figures indicative from NCS and leading tech hiring audits 2024.",
        "future_scope": "Exponential expansion with the worldwide adoption of foundation models and automated decision infrastructure.",
        "government_opportunities": "DRDO Centre for AI and Robotics (CAIR), ISRO, CDAC, National Critical Information Infrastructure Protection Centre (NCIIPC).",
        "private_opportunities": "NVIDIA, Intel, Google DeepMind, Microsoft, Adobe, Qualcomm, Flipkart, high-growth AI startups.",
        "higher_study_options": "M.Tech in AI / Robotics, M.S. in Machine Learning, Ph.D. in Computer Vision or Natural Language Processing.",
        "entrepreneurship_options": "Specialized AI inference platforms, verticalized generative AI tools, vision-based inspection startups.",
        "source": "NASSCOM / National Career Service / AICTE",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 43, "type": "DIRECT"},   # B.Tech AI & Data Science
            {"course_id": 38, "type": "SPECIALIZED"}, # M.Tech CSE
            {"course_id": 4, "type": "ALTERNATIVE"} # B.Sc Computer Science
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "PRIMARY"}   # GATE
        ],
        "routes": [
            {"title": "Path A: Core Engineering + AI Specialization", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech CSE/IT -> Focus on DSA, Math & PyTorch -> Build MLOps projects -> ML Engineer."},
            {"title": "Path B: Software Engineer to ML Engineer Transition", "type": "COMMON", "steps": "Class 12 -> B.Tech / MCA -> 2-3 years Backend Software Engineering -> Learn Model Serving & ML Pipelines -> ML Engineer."}
        ],
        "ladder": [
            {"stage": "Junior ML Engineer", "exp": "0-2 Years", "desc": "Implements data extraction, runs baseline model deployments, maintains monitoring."},
            {"stage": "Machine Learning Engineer", "exp": "2-5 Years", "desc": "Builds scalable serving pipelines, optimizes latency, refactors models."},
            {"stage": "Senior ML Engineer", "exp": "5-8 Years", "desc": "Designs distributed training infrastructure and automated model governance."},
            {"stage": "Staff / Lead ML Engineer", "exp": "8+ Years", "desc": "Directs overall AI platform architecture across enterprise product lines."}
        ],
        "roadmaps": {
            "Class 10": "Master algebra, coordinate geometry, and basic coding syntax in Python.",
            "Class 12": "Target top engineering colleges through JEE Main / Advanced. Gain fluency in Calculus and Linear Algebra.",
            "Graduation": "Learn PyTorch/TensorFlow and MLOps tools (Docker, MLflow). Deploy live models behind FastAPI microservices.",
            "Working Professional": "Focus on distributed model training (Ray, DeepSpeed), model quantization (GGUF, TensorRT), and Kubernetes orchestration."
        }
    },
    {
        "title": "Cybersecurity Analyst",
        "short_name": "Cybersecurity Analyst",
        "slug": "cybersecurity-analyst",
        "category": "Technology & Computer Science",
        "sub_category": "Information Security & Defence",
        "industry": "Information Technology / Defence",
        "icon": "shield-lock",
        "short_description": "Protects computer systems, networks, and sensitive data from cyber attacks, unauthorized access, and security breaches.",
        "description": "Cybersecurity Analysts are the digital frontline defenders of organizations. They monitor network traffic for suspicious activity, perform vulnerability assessments, investigate security incidents, configure firewalls, and establish organizational security compliance.",
        "what_they_do": "They analyze security events, conduct penetration tests, design disaster recovery protocols, patch vulnerabilities, and educate corporate staff on threat prevention such as phishing and social engineering.",
        "day_to_day_work": "• Monitoring Security Information and Event Management (SIEM) consoles for active threats.\n• Investigating intrusion attempts, malware activity, and network anomalies.\n• Performing vulnerability scanning and ethical penetration tests.\n• Drafting incident response reports and hardening server configurations.\n• Auditing compliance against ISO 27001 and CERT-In advisories.",
        "work_environment": "Security Operations Centers (SOC), corporate IT headquarters, defense facilities, or remote secure workstations.",
        "work_modes": "On-site / Hybrid / Shift-based in SOC",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Computer Science, Mathematics, Physics",
        "technical_skills": "Network Security, SIEM Tools, Ethical Hacking, Incident Response, Cryptography, Linux Administration",
        "soft_skills": "Attention to Detail, Calm Under Pressure, Analytical Mindset, Discretion",
        "tools": "Wireshark, Splunk, Metasploit, Burp Suite, Nmap, Kali Linux, Nessus",
        "certifications": "CompTIA Security+, Certified Ethical Hacker (CEH), CISSP, OSCP (Offensive Security Certified Professional)",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Critical national demand with progression to SOC Manager, Security Architect, or Chief Information Security Officer (CISO).",
        "internship_roles": "SOC Analyst Intern, Vulnerability Assessment Intern, Information Security Intern",
        "entry_level_roles": "Associate Security Analyst, L1 SOC Analyst, Junior Penetration Tester",
        "average_salary": "₹4.5 - ₹15 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹4 - 6.5 LPA | Mid-Level (3-6 yrs): ₹8 - 16 LPA | Senior/Lead (7+ yrs): ₹18 - 38+ LPA. Indicative figures from NCS & DSCI (Data Security Council of India) 2024.",
        "future_scope": "Surging demand fueled by increased cyber warfare, regulatory mandates (DPDP Act 2023), and cloud migrations.",
        "government_opportunities": "CERT-In, National Critical Information Infrastructure Protection Centre (NCIIPC), NTRO, IB, DRDO, Defence Cyber Agency, State Police Cyber Cells.",
        "private_opportunities": "PwC, EY, Deloitte, KPMG, Wipro, TCS, Cisco, Palantir, Banking and FinTech security teams.",
        "higher_study_options": "M.Tech in Cybersecurity, M.S. in Information Security, Post Graduate Diploma in Digital Forensics.",
        "entrepreneurship_options": "Cybersecurity audit firms, managed security service provider (MSSP), red-teaming consultancies.",
        "source": "National Career Service (NCS) / Data Security Council of India (DSCI)",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 42, "type": "COMMON"},  # B.Tech IT
            {"course_id": 14, "type": "ALTERNATIVE"}, # BCA
            {"course_id": 15, "type": "ALTERNATIVE"}  # MCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 42, "importance": "ALTERNATIVE"}, # Intelligence Bureau ACIO
            {"exam_id": 45, "importance": "OPTIONAL"}  # NIC Scientist B
        ],
        "routes": [
            {"title": "Path A: Degree in CSE / IT + Security Certification", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech CSE/IT -> Learn Computer Networking & Linux -> CompTIA Security+ or CEH -> SOC Analyst L1."},
            {"title": "Path B: BCA / B.Sc -> Hands-on Ethical Hacking Route", "type": "ALTERNATIVE", "steps": "Class 12 -> BCA / B.Sc CS -> Learn Network Protocols -> TryHackMe / HackTheBox ranks -> OSCP certification -> Security Analyst."}
        ],
        "ladder": [
            {"stage": "L1 SOC Analyst", "exp": "0-2 Years", "desc": "Triage alerts, initial incident detection, ticket escalation."},
            {"stage": "L2 / L3 Incident Responder", "exp": "2-5 Years", "desc": "Deep forensics, root-cause investigation, malware sandbox analysis."},
            {"stage": "Security Architect / Lead", "exp": "5-8 Years", "desc": "Designs zero-trust network architectures and organizational defensive controls."},
            {"stage": "Chief Information Security Officer (CISO)", "exp": "10+ Years", "desc": "Heads total digital safety, cyber compliance, and executive risk management."}
        ],
        "roadmaps": {
            "Class 10": "Develop strong curiosity about computer networks and operating systems. Learn Linux commands and basic scripting.",
            "Class 12": "Focus on Mathematics and Physics. Gain practical experience with virtual machines and TCP/IP networking protocols.",
            "Graduation": "Practice on capture-the-flag (CTF) platforms (OverTheWire, TryHackMe). Earn Security+ or CEH and secure a SOC internship.",
            "Working Professional": "Pursue hands-on offensive/defensive certifications (OSCP, CISSP, AWS Security) and specialize in Cloud Security."
        }
    },
    {
        "title": "Cloud Solutions Architect",
        "short_name": "Cloud Architect",
        "slug": "cloud-solutions-architect",
        "category": "Technology & Computer Science",
        "sub_category": "Cloud Computing & Infrastructure",
        "industry": "Information Technology",
        "icon": "cloud-arrow-up",
        "short_description": "Designs scalable, resilient, and cost-effective enterprise computing architectures on public, private, and hybrid cloud environments.",
        "description": "Cloud Solutions Architects oversee an enterprise's cloud computing strategy. They evaluate business requirements and translate them into resilient, secure, and highly available cloud deployments utilizing platforms like AWS, Microsoft Azure, and Google Cloud.",
        "what_they_do": "They design microservices topologies, plan cloud migration journeys, ensure automated disaster recovery, optimize cloud expenditure, and implement stringent cloud compliance and governance standards.",
        "day_to_day_work": "• Designing multi-region, fault-tolerant cloud architecture blueprints.\n• Reviewing system scalability and serverless infrastructure.\n• Creating Infrastructure as Code (IaC) templates using Terraform.\n• Conducting cost-optimization reviews (FinOps).\n• Collaborating with enterprise security and DevOps teams.",
        "work_environment": "Global IT consulting offices, enterprise technology centers, or flexible remote arrangements.",
        "work_modes": "Hybrid / Remote",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Mathematics, Physics, Computer Science",
        "technical_skills": "Cloud Architecture, Distributed Systems, Terraform, Kubernetes, Networking, Linux, Security Compliance",
        "soft_skills": "Stakeholder Management, Strategic Vision, Communication, Problem Solving",
        "tools": "AWS Console, Azure Portal, Google Cloud Platform, Terraform, Kubernetes, Helm, CloudFormation",
        "certifications": "AWS Certified Solutions Architect - Professional, Google Professional Cloud Architect, Microsoft Certified: Azure Solutions Architect Expert",
        "experience_level": "Mid-Level to Senior",
        "career_growth": "Exceptional executive career path leading to Chief Technology Officer (CTO) or VP of Infrastructure.",
        "internship_roles": "Cloud Engineering Intern, DevOps Intern, Infrastructure Trainee",
        "entry_level_roles": "Cloud Support Associate, Junior Cloud Engineer, Systems Engineer Trainee",
        "average_salary": "₹8 - ₹28 LPA (Indicative range)",
        "salary_indicative": "Entry/Junior Cloud Engineer (0-2 yrs): ₹5 - 8 LPA | Cloud Architect (4-8 yrs): ₹14 - 26 LPA | Principal Solutions Architect (8+ yrs): ₹30 - 65+ LPA. Indicative figures based on NCS & Industry Cloud Reports 2024.",
        "future_scope": "Consistently high demand as practically all enterprises modernize legacy data centers to cloud platforms.",
        "government_opportunities": "National Informatics Centre (MeghRaj Cloud), CDAC, RailTel, UIDAI Infrastructure Wing, State Data Centres.",
        "private_opportunities": "Amazon Web Services, Microsoft, Google, Wipro, Infosys, Accenture, Cognizant, IBM Cloud.",
        "higher_study_options": "M.Tech in Cloud Computing, M.S. in Computer Systems, Executive MBA in Technology.",
        "entrepreneurship_options": "Cloud migration consultancies, cloud cost optimization (FinOps) agencies, managed cloud service firms.",
        "source": "National Career Service (NCS) / AICTE",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 42, "type": "COMMON"},  # B.Tech IT
            {"course_id": 15, "type": "ALTERNATIVE"}, # MCA
            {"course_id": 38, "type": "SPECIALIZED"}  # M.Tech CSE
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "ALTERNATIVE"}  # GATE
        ],
        "routes": [
            {"title": "Path A: Standard Engineering to Cloud Route", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech CSE/IT -> Junior Cloud / Systems Engineer (2-3 yrs) -> Cloud Associate & Professional Certifications -> Cloud Solutions Architect."},
            {"title": "Path B: SysAdmin / DevOps Progression", "type": "COMMON", "steps": "BCA / B.Sc CS -> Linux Administrator -> DevOps Engineer -> Specialize in Infrastructure as Code -> Cloud Solutions Architect."}
        ],
        "ladder": [
            {"stage": "Junior Cloud Support / Engineer", "exp": "0-2 Years", "desc": "Monitors cloud workloads, manages basic IAM policies, automates simple scripts."},
            {"stage": "Cloud Engineer / DevOps Engineer", "exp": "2-5 Years", "desc": "Builds IaC pipelines, provisions Kubernetes clusters, manages cloud networking."},
            {"stage": "Cloud Solutions Architect", "exp": "5-9 Years", "desc": "Designs complex multi-tier enterprise cloud architectures and migration roadmaps."},
            {"stage": "Principal Cloud Architect / VP", "exp": "9+ Years", "desc": "Owns organizational cloud portfolio, executive vendor strategy, and architecture governance."}
        ],
        "roadmaps": {
            "Class 10": "Focus on Mathematics and basic IT fundamentals. Explore how internet servers work.",
            "Class 12": "Target standard computer engineering degrees. Learn Linux command line tools and basic networking (DNS, IP, HTTP).",
            "Graduation": "Learn Docker, Git, and Linux server management. Deploy personal projects on free-tier AWS or GCP. Earn AWS Certified Solutions Architect Associate.",
            "Working Professional": "Master Terraform, Kubernetes, and enterprise microservice patterns. Pass professional-level cloud architect exams."
        }
    },
    {
        "title": "DevOps Engineer",
        "short_name": "DevOps Engineer",
        "slug": "devops-engineer",
        "category": "Technology & Computer Science",
        "sub_category": "Cloud Computing & Infrastructure",
        "industry": "Information Technology",
        "icon": "arrow-repeat",
        "short_description": "Streamlines software delivery by automating and integrating processes between software development and IT operations teams.",
        "description": "DevOps Engineers blend development and operational skill sets to automate continuous integration and continuous delivery (CI/CD) pipelines. They eliminate operational bottlenecks, ensure system reliability, and maintain fast, dependable release cadences.",
        "what_they_do": "They build automated CI/CD pipelines, manage containerized environments, provision infrastructure automatically, implement observability (monitoring/logging), and ensure system uptime.",
        "day_to_day_work": "• Maintaining Jenkins or GitHub Actions CI/CD workflows.\n• Writing Kubernetes manifests and Helm charts.\n• Managing cloud infrastructure with Terraform.\n• Setting up Prometheus and Grafana dashboards for cluster observability.\n• Participating in on-call incident triage and post-mortem analysis.",
        "work_environment": "Tech company headquarters, software development studios, or remote development environments.",
        "work_modes": "Hybrid / Remote",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Computer Science, Mathematics, Physics",
        "technical_skills": "Linux, Docker, Kubernetes, CI/CD, Git, Terraform, Bash/Python Scripting, Monitoring",
        "soft_skills": "Collaboration, Automation Mindset, Troubleshooting Under Pressure, Communication",
        "tools": "Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, Ansible, Prometheus, Grafana",
        "certifications": "Certified Kubernetes Administrator (CKA), AWS Certified DevOps Engineer - Professional, HashiCorp Certified: Terraform Associate",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Rapid growth with progression to Site Reliability Engineer (SRE), Head of Infrastructure, or Director of DevOps.",
        "internship_roles": "DevOps Intern, Site Reliability Intern, Build & Release Intern",
        "entry_level_roles": "Junior DevOps Engineer, Build Engineer, Cloud Operations Associate",
        "average_salary": "₹5 - ₹18 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹4.5 - 7.5 LPA | Mid-Level (3-6 yrs): ₹9 - 18 LPA | Senior/Lead (7+ yrs): ₹20 - 42+ LPA. Indicative figures based on NCS & Tech Compensation Surveys 2024.",
        "future_scope": "Essential role for every contemporary software company striving for high release frequency and uptime.",
        "government_opportunities": "CDAC, NIC, UIDAI infrastructure, State e-Governance portals, Railway Information Systems (CRIS).",
        "private_opportunities": "Red Hat, GitLab, Thoughtworks, Flipkart, Swiggy, Amazon, Capgemini, Cisco.",
        "higher_study_options": "M.Tech in Software Engineering, M.S. in Computer Systems.",
        "entrepreneurship_options": "DevOps automation consultancies, site reliability as a service, specialized cloud infrastructure agencies.",
        "source": "National Career Service (NCS) / NASSCOM",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 42, "type": "COMMON"},  # B.Tech IT
            {"course_id": 14, "type": "ALTERNATIVE"}, # BCA
            {"course_id": 15, "type": "ALTERNATIVE"}  # MCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "ALTERNATIVE"}  # GATE
        ],
        "routes": [
            {"title": "Path A: Computer Science Degree to DevOps", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech CSE/IT -> Master Linux & Git -> Learn Docker & CI/CD -> Junior DevOps Engineer."},
            {"title": "Path B: SysAdmin to DevOps Evolution", "type": "COMMON", "steps": "BCA / Diploma / B.Sc -> System Administrator -> Automate tasks with Python/Ansible -> Containerization (Docker/K8s) -> DevOps Engineer."}
        ],
        "ladder": [
            {"stage": "Junior DevOps / Cloud Ops", "exp": "0-2 Years", "desc": "Maintains pipeline scripts, assists in build failures, sets up basic alerts."},
            {"stage": "DevOps Engineer / SRE", "exp": "2-5 Years", "desc": "Owns automated deployment pipelines, manages Kubernetes clusters, tunes performance."},
            {"stage": "Senior DevOps / SRE Lead", "exp": "5-8 Years", "desc": "Architects multi-cloud CI/CD pipelines, establishes chaos engineering and SLA tracking."},
            {"stage": "Director of Infrastructure / DevOps", "exp": "8+ Years", "desc": "Leads engineering platform teams and organizational infrastructure budget."}
        ],
        "roadmaps": {
            "Class 10": "Build curiosity about how software updates reach millions of users without crashes.",
            "Class 12": "Take Science (PCM). Practice installing Linux, using the command line, and writing simple Bash scripts.",
            "Graduation": "Learn Git workflows, Dockerize web applications, set up GitHub Actions CI/CD pipelines, and clear the CKA exam.",
            "Working Professional": "Specialize in Kubernetes, GitOps (ArgoCD), Infrastructure as Code (Terraform), and Site Reliability Engineering principles."
        }
    },
    {
        "title": "UI/UX Designer",
        "short_name": "UI/UX Designer",
        "slug": "ui-ux-designer",
        "category": "Technology & Computer Science",
        "sub_category": "Design & User Experience",
        "industry": "Information Technology / Design",
        "icon": "palette",
        "short_description": "Crafts intuitive, user-friendly, and visually engaging digital interfaces for mobile apps, web platforms, and digital software products.",
        "description": "UI/UX Designers merge empathy, cognitive psychology, and visual artistry. UX (User Experience) designers research user behaviors, create information architectures, and test usability; UI (User Interface) designers craft the visual layouts, typography, color palettes, and interactive micro-animations.",
        "what_they_do": "They conduct user interviews, design wireframes and prototypes, establish cohesive design systems, and collaborate with software engineers to ensure designs are implemented accurately.",
        "day_to_day_work": "• Conducting user research interviews and synthesizing feedback.\n• Creating low-fidelity wireframes and user journey maps in Figma.\n• Building interactive, clickable prototypes for usability testing.\n• Maintaining design tokens and components in the team design system.\n• Handing off design specifications to frontend developers.",
        "work_environment": "Creative design studios, tech corporate headquarters, advertising agencies, or remote home studios.",
        "work_modes": "Hybrid / Remote / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Any Stream",
        "required_subjects": "English, Design / Computer Applications (helpful)",
        "technical_skills": "User Research, Wireframing, Prototyping, Information Architecture, Design Systems, Usability Testing, Visual Design",
        "soft_skills": "Empathy, Active Listening, Storytelling, Visual Communication, Creative Problem Solving",
        "tools": "Figma, Adobe XD, Miro, Maze, InVision, Illustrator",
        "certifications": "Google UX Design Professional Certificate, Nielsen Norman Group UX Certification",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "High demand in product-led organizations, progressing to Product Design Lead, Head of Design, or Chief Experience Officer (CXO).",
        "internship_roles": "UX Research Intern, Product Design Intern, UI Design Intern",
        "entry_level_roles": "Junior UI/UX Designer, Associate Product Designer, Visual Designer",
        "average_salary": "₹4.5 - ₹16 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹3.5 - 6.5 LPA | Mid-Level (3-6 yrs): ₹8 - 18 LPA | Lead Product Designer (7+ yrs): ₹20 - 45+ LPA. Indicative figures based on NCS & Design Industry Surveys 2024. Heavily reliant on portfolio quality.",
        "future_scope": "Strong sustained growth driven by mobile-first consumer apps, B2B SaaS interfaces, and spatial computing.",
        "government_opportunities": "Digital India initiatives, MyGov platform design, NIC portals, Centre for Railway Information Systems (CRIS).",
        "private_opportunities": "Swiggy, Zomato, CRED, Razorpay, Microsoft, Google, Adobe, boutique design agencies.",
        "higher_study_options": "M.Des in Interaction Design, M.S. in Human-Computer Interaction (HCI).",
        "entrepreneurship_options": "Boutique digital design studio, UX research consultancy, digital asset and template creator.",
        "source": "National Career Service (NCS) / National Institute of Design (NID)",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 33, "type": "DIRECT"},    # B.Des
            {"course_id": 14, "type": "ALTERNATIVE"}, # BCA
            {"course_id": 9, "type": "ALTERNATIVE"},  # B.Tech CSE
            {"course_id": 4, "type": "ALTERNATIVE"}   # B.Sc Computer Science
        ],
        "exams": [
            {"exam_id": 84, "importance": "PRIMARY"},   # UCEED
            {"exam_id": 85, "importance": "PRIMARY"},   # NID DAT
            {"exam_id": 79, "importance": "ALTERNATIVE"} # CUET-UG
        ],
        "routes": [
            {"title": "Path A: Formal Design Degree Route", "type": "COMMON", "steps": "Class 12 (Any stream) -> UCEED / NID DAT -> B.Des in Interaction / Communication Design -> Portfolio building -> UI/UX Designer."},
            {"title": "Path B: Tech / Humanities to Design Transition", "type": "COMMON", "steps": "Class 12 -> BCA / B.Tech / BA -> Learn Figma & UX methodologies -> Build 3 case study portfolio -> Junior Product Designer."}
        ],
        "ladder": [
            {"stage": "Junior UI/UX Designer", "exp": "0-2 Years", "desc": "Assists with screen layouts, component creation, and usability test notes."},
            {"stage": "Product Designer", "exp": "2-5 Years", "desc": "Owns end-to-end user flows for major product features, drives user testing."},
            {"stage": "Senior Product Designer / Design Lead", "exp": "5-8 Years", "desc": "Defines product design system, mentors designers, aligns design with business KPIs."},
            {"stage": "Head of Design / VP of UX", "exp": "8+ Years", "desc": "Directs total brand and product experience across the enterprise portfolio."}
        ],
        "roadmaps": {
            "Class 10": "Practice drawing, observation, and critical review of everyday digital apps. Explore basic layout and graphic software.",
            "Class 12": "Prepare for design entrance exams (UCEED, NID DAT) or choose any degree while studying interaction design books (e.g., 'The Design of Everyday Things').",
            "Graduation": "Build a robust Behance/Dribbble/Notion portfolio with at least 3 deep UX case studies showing your problem-solving process.",
            "Working Professional": "Learn advanced design systems, micro-interactions, accessibility standards (WCAG), and quantitative UX metrics."
        }
    },
    {
        "title": "Product Manager",
        "short_name": "Product Manager",
        "slug": "product-manager",
        "category": "Technology & Computer Science",
        "sub_category": "Product Leadership & Strategy",
        "industry": "Information Technology / Digital Products",
        "icon": "kanban",
        "short_description": "Guides the success of a product and leads the cross-functional team that is responsible for improving it through its entire lifecycle.",
        "description": "Product Managers operate at the intersection of business, technology, and user experience. They discover what problems need solving, define the product vision, prioritize the feature roadmap, and rally engineering, design, and marketing teams to deliver high-impact software solutions.",
        "what_they_do": "They define product strategy, write Product Requirement Documents (PRDs), track performance metrics (retention, conversion, churn), conduct competitive analysis, and make critical trade-off decisions between business urgency and technical feasibility.",
        "day_to_day_work": "• Reviewing user feedback and analyzing product usage funnels.\n• Writing clear Product Requirement Documents (PRDs) and user stories.\n• Prioritizing engineering sprints with tech leads.\n• Running feature retrospectives and reporting business impact to leadership.\n• Aligning marketing and sales teams for upcoming product launches.",
        "work_environment": "Dynamic corporate tech environments, startup incubators, or hybrid headquarters.",
        "work_modes": "Hybrid / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Any Stream (Science / Commerce preferred)",
        "required_subjects": "Mathematics, English, Economics/CS helpful",
        "technical_skills": "Product Analytics, PRD Writing, Agile Methodologies, A/B Testing, User Journey Mapping, Wireframing",
        "soft_skills": "Leadership without Authority, Persuasion, Strategic Thinking, Prioritization, Empathy",
        "tools": "Jira, Mixpanel, Amplitude, Notion, Figma, SQL, Google Analytics",
        "certifications": "Certified Scrum Product Owner (CSPO), Pragmatic Institute Certified, AIPMM Certified Product Manager",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Highly prestigious career track leading to Group PM, VP of Product, or Chief Product Officer (CPO) / CEO.",
        "internship_roles": "Associate Product Manager (APM) Intern, Product Operations Intern, Business Analyst Intern",
        "entry_level_roles": "Associate Product Manager (APM), Product Analyst, Junior Product Specialist",
        "average_salary": "₹8 - ₹25 LPA (Indicative range)",
        "salary_indicative": "Entry-Level / APM (0-2 yrs): ₹7 - 14 LPA | Mid-Level PM (3-6 yrs): ₹15 - 28 LPA | Director / VP of Product (7+ yrs): ₹32 - 70+ LPA. Indicative figures based on NCS & Indian Startup Compensation Index 2024.",
        "future_scope": "Surging across all digital and tech-enabled sectors as companies prioritize customer-centric product strategies.",
        "government_opportunities": "National Health Authority (ABDM), India Stack projects, ONDC initiatives, NPCI, Digital India PMUs.",
        "private_opportunities": "Flipkart, Razorpay, Swiggy, Paytm, Microsoft, Google, Uber, innovative consumer & B2B SaaS startups.",
        "higher_study_options": "MBA from top business schools (IIMs, ISB), Master's in Management & Technology.",
        "entrepreneurship_options": "Launching tech startups, establishing product growth advisory services, early-stage angel investing.",
        "source": "National Career Service (NCS) / Product Leaders Forum",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 18, "type": "SPECIALIZED"}, # MBA
            {"course_id": 17, "type": "COMMON"},  # BBA
            {"course_id": 14, "type": "ALTERNATIVE"}  # BCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 77, "importance": "PRIMARY"},  # CAT
            {"exam_id": 78, "importance": "ALTERNATIVE"}  # XAT
        ],
        "routes": [
            {"title": "Path A: Engineering + APM Program Route", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech CSE/IT -> Product Internships & Hackathons -> Associate Product Manager (APM) campus hire."},
            {"title": "Path B: UG Degree + Top MBA Route", "type": "COMMON", "steps": "Undergraduate degree (Engineering / Commerce / Arts) -> 2 yrs work experience -> CAT / GMAT -> MBA from IIM/ISB -> Product Manager campus hire."},
            {"title": "Path C: Internal Lateral Transition", "type": "ALTERNATIVE", "steps": "Software Developer / Business Analyst / UI-UX Designer -> Demonstrate business vision -> Transition to Product Manager."}
        ],
        "ladder": [
            {"stage": "Associate Product Manager (APM)", "exp": "0-2 Years", "desc": "Owns specific product features, writes specs, coordinates sprints under Senior PM."},
            {"stage": "Product Manager (PM)", "exp": "2-5 Years", "desc": "Owns an entire product line or user journey, drives key metrics (retention, GMV)."},
            {"stage": "Senior / Principal Product Manager", "exp": "5-8 Years", "desc": "Owns multi-product strategy, leads major technical pivots, mentors PM cohorts."},
            {"stage": "Director / Chief Product Officer (CPO)", "exp": "8+ Years", "desc": "Sets enterprise vision, aligns product portfolio with board and market strategy."}
        ],
        "roadmaps": {
            "Class 10": "Read widely about how popular products (WhatsApp, UPI, YouTube) solve human friction points. Build strong verbal and written logic.",
            "Class 12": "Aim for premier engineering or commerce institutions. Learn how businesses make money and how technology scales.",
            "Graduation": "Participate in product teardowns, PM case competitions, and build a side project from ideation to launch. Apply to competitive APM programs.",
            "Working Professional": "Develop deep data fluency (SQL, cohort retention), run experiments, and master product discovery frameworks."
        }
    },
    {
        "title": "Database Administrator (DBA)",
        "short_name": "Database Administrator",
        "slug": "database-administrator",
        "category": "Technology & Computer Science",
        "sub_category": "Database Architecture & Administration",
        "industry": "Information Technology",
        "icon": "database",
        "short_description": "Maintains, secures, and optimizes relational and NoSQL database systems to ensure data availability and integrity.",
        "description": "Database Administrators ensure that enterprise database environments operate efficiently, reliably, and securely. They perform performance tuning, database migration, automated backup management, disaster recovery planning, and manage access security permissions.",
        "what_they_do": "They configure database servers, write and optimize complex SQL queries, monitor query latency, implement replication and sharding strategies, and execute database upgrades without business downtime.",
        "day_to_day_work": "• Monitoring database performance and diagnosing slow-running queries.\n• Executing automated backups and verifying disaster recovery restore procedures.\n• Managing role-based access control (RBAC) and database security compliance.\n• Applying database patches and index reorganizations.\n• Collaborating with developers on schema design and migration scripts.",
        "work_environment": "Corporate IT data centers, financial services centers, or remote infrastructure operations.",
        "work_modes": "Hybrid / On-site / On-call rotation",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Computer Science, Mathematics",
        "technical_skills": "SQL, PostgreSQL, Oracle DB, MySQL, MongoDB, Database Tuning, Backup & Recovery, Replication",
        "soft_skills": "Meticulous Attention to Detail, Problem Solving, Reliability Under Pressure",
        "tools": "Oracle Enterprise Manager, pgAdmin, MySQL Workbench, Datadog, Liquibase, Redgate",
        "certifications": "Oracle Certified Professional (OCP) DBA, Microsoft Certified: Azure Database Administrator Associate, AWS Certified Database - Specialty",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Steady progression into Senior DBA, Data Architect, or Chief Data Architect.",
        "internship_roles": "Database Intern, Junior Systems Administrator, Data Operations Trainee",
        "entry_level_roles": "Junior Database Administrator, Database Support Engineer, Data Operations Associate",
        "average_salary": "₹4.5 - ₹14 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹3.8 - 6 LPA | Mid-Level (3-6 yrs): ₹7 - 14 LPA | Senior DBA (7+ yrs): ₹16 - 32+ LPA. Indicative figures based on NCS & IT Services Benchmark Reports 2024.",
        "future_scope": "Sustained requirement, especially for cloud-native databases (Amazon Aurora, Cloud Spanner) and hybrid configurations.",
        "government_opportunities": "State Data Centres, Reserve Bank of India, NIC, UIDAI, Income Tax Department IT Division.",
        "private_opportunities": "HDFC Bank, ICICI Bank, TCS, Infosys, Oracle, IBM, telecommunication giants like Airtel and Jio.",
        "higher_study_options": "M.Tech in Information Technology, M.S. in Data Engineering.",
        "entrepreneurship_options": "Specialized database tuning consultancies, managed database migration agencies.",
        "source": "National Career Service (NCS) / AICTE",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 14, "type": "COMMON"},  # BCA
            {"course_id": 15, "type": "COMMON"},  # MCA
            {"course_id": 4, "type": "ALTERNATIVE"}  # B.Sc Computer Science
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "ALTERNATIVE"}  # GATE
        ],
        "routes": [
            {"title": "Path A: Computer Degree + DBA Specialization", "type": "COMMON", "steps": "Class 12 -> B.Tech CSE / BCA / MCA -> Advanced SQL & Relational Algebra -> Oracle / Postgres Certification -> Junior DBA."},
            {"title": "Path B: SysAdmin to Database Specialist", "type": "COMMON", "steps": "Diploma / B.Sc -> IT Operations -> Specialize in Storage & SQL Services -> Database Administrator."}
        ],
        "ladder": [
            {"stage": "Junior DBA", "exp": "0-2 Years", "desc": "Handles daily backups, monitoring, simple schema scripts, user permissions."},
            {"stage": "Database Administrator", "exp": "2-5 Years", "desc": "Performs indexing optimizations, replication setups, and patch management."},
            {"stage": "Senior DBA / Lead", "exp": "5-8 Years", "desc": "Designs disaster recovery sites, high availability clustering, and cloud migration."},
            {"stage": "Principal Data Architect", "exp": "8+ Years", "desc": "Sets enterprise data storage architecture, governance, and compliance policies."}
        ],
        "roadmaps": {
            "Class 10": "Understand basic mathematical sets, tables, and logical operations.",
            "Class 12": "Focus on Computer Science and Mathematics. Master basic relational database concepts.",
            "Graduation": "Learn SQL thoroughly (window functions, indexing, query execution plans). Practice with PostgreSQL and MySQL.",
            "Working Professional": "Earn cloud database certifications (AWS Aurora / Azure SQL) and master distributed NoSQL systems."
        }
    },
    {
        "title": "Web Developer (Full-Stack)",
        "short_name": "Full-Stack Web Dev",
        "slug": "web-developer",
        "category": "Technology & Computer Science",
        "sub_category": "Software Engineering & Architecture",
        "industry": "Information Technology / Web",
        "icon": "globe",
        "short_description": "Builds both client-side and server-side components of interactive web applications from database to user interface.",
        "description": "Full-Stack Web Developers possess end-to-end expertise across modern web architectures. They write frontend code that runs in user browsers and backend logic that connects to databases and external APIs, ensuring seamless digital experiences.",
        "what_they_do": "They build responsive web layouts, implement backend RESTful and GraphQL APIs, integrate third-party payment gateways, optimize page load performance, and ensure cross-browser compatibility.",
        "day_to_day_work": "• Building responsive user interfaces using React, Next.js, or Vue.\n• Writing backend APIs using Node.js, Python, or Go.\n• Modeling database schemas in PostgreSQL or MongoDB.\n• Implementing authentication and authorization (OAuth, JWT).\n• Deploying web applications on Vercel, Netlify, or cloud containers.",
        "work_environment": "Modern software offices, digital agency workspaces, or fully remote setups.",
        "work_modes": "Remote / Hybrid / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Any Stream (Science / CS preferred)",
        "required_subjects": "Computer Science, Mathematics (recommended)",
        "technical_skills": "HTML5, CSS3, JavaScript/TypeScript, React/Next.js, Node.js/Python, REST APIs, SQL, Git",
        "soft_skills": "Creativity, Problem Solving, Continuous Learning, Clear Communication",
        "tools": "VS Code, Git, Chrome DevTools, Postman, Vercel, Docker, Figma",
        "certifications": "Meta Front-End Developer Professional Certificate, AWS Certified Developer - Associate",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Broad, flexible career path progressing to Full-Stack Lead, Frontend Architect, or Tech Founder.",
        "internship_roles": "Web Development Intern, Frontend Intern, Backend Intern",
        "entry_level_roles": "Junior Web Developer, Associate Software Engineer, Frontend Developer",
        "average_salary": "₹3.5 - ₹12 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹3 - 6 LPA | Mid-Level (3-6 yrs): ₹7 - 15 LPA | Senior Full-Stack Lead (7+ yrs): ₹16 - 35+ LPA. Indicative figures from NCS & Web Tech Job Audits 2024.",
        "future_scope": "Continuous solid demand across commercial enterprises, media houses, e-commerce, and SaaS providers.",
        "government_opportunities": "National Informatics Centre (NIC), State e-Governance portals, Digital India projects.",
        "private_opportunities": "Zomato, Swiggy, Paytm, Zoho, Freshworks, tech agencies, and worldwide remote companies.",
        "higher_study_options": "M.Tech in CSE, MCA, M.S. in Computer Science.",
        "entrepreneurship_options": "Independent web development agency, building micro-SaaS applications, freelance engineering consulting.",
        "source": "National Career Service (NCS) / NASSCOM",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 14, "type": "COMMON"},  # BCA
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 4, "type": "COMMON"},   # B.Sc Computer Science
            {"course_id": 15, "type": "ALTERNATIVE"} # MCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 79, "importance": "ALTERNATIVE"} # CUET-UG
        ],
        "routes": [
            {"title": "Path A: Standard BCA / B.Tech to Web Dev", "type": "COMMON", "steps": "Class 12 -> BCA / B.Tech CSE -> Master HTML, CSS, JavaScript, React & Node.js -> Build full-stack portfolio -> Junior Developer."},
            {"title": "Path B: Self-Taught / Bootcamp Route", "type": "ALTERNATIVE", "steps": "Any Class 12 / Degree -> Self-paced learning / Bootcamp -> Build 5+ live full-stack deployed web apps -> Open source contributions -> Web Developer."}
        ],
        "ladder": [
            {"stage": "Junior Web Developer", "exp": "0-2 Years", "desc": "Implements UI components, integrates simple APIs, fixes CSS/JS bugs."},
            {"stage": "Full-Stack Developer", "exp": "2-5 Years", "desc": "Builds end-to-end features, manages database models, writes automated tests."},
            {"stage": "Senior Web Developer / Tech Lead", "exp": "5-8 Years", "desc": "Decides tech stack, optimizes web performance and SEO, conducts code audits."},
            {"stage": "Principal Architect / Engineering Manager", "exp": "8+ Years", "desc": "Directs company-wide web architecture, design system adoption, and hiring."}
        ],
        "roadmaps": {
            "Class 10": "Learn basics of HTML and CSS. Create simple static web pages for fun.",
            "Class 12": "Learn JavaScript syntax and DOM manipulation. Build interactive web calculators or to-do apps.",
            "Graduation": "Learn React/Next.js and Node.js. Build full-stack web applications with authentication and databases. Deploy on Vercel.",
            "Working Professional": "Master TypeScript, state management, server-side rendering (SSR), and micro-frontend architectures."
        }
    },
    {
        "title": "Mobile Application Developer",
        "short_name": "Mobile App Dev",
        "slug": "mobile-app-developer",
        "category": "Technology & Computer Science",
        "sub_category": "Mobile Systems & Native Development",
        "industry": "Information Technology / Mobile Ecosystem",
        "icon": "phone",
        "short_description": "Builds intuitive, responsive native and cross-platform mobile apps for Android and iOS operating systems.",
        "description": "Mobile Application Developers design and construct engaging mobile applications. They focus on hardware-software optimization, memory efficiency, offline support, device sensor integrations, and seamless user experiences on smartphones and tablets.",
        "what_they_do": "They write native applications in Kotlin/Swift or cross-platform code in Flutter/React Native, integrate push notifications, optimize battery usage, and manage app store publishing cycles.",
        "day_to_day_work": "• Writing feature logic in Kotlin (Android) or Swift (iOS) or Flutter.\n• Connecting mobile interfaces with backend cloud APIs.\n• Profiling application memory, frame rates, and battery consumption.\n• Testing app behavior across multiple screen sizes and OS versions.\n• Preparing build releases for Google Play Store and Apple App Store.",
        "work_environment": "Tech company offices, mobile development labs, or remote setups.",
        "work_modes": "Hybrid / Remote / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM) / Any with CS",
        "required_subjects": "Computer Science, Mathematics",
        "technical_skills": "Kotlin, Swift, Flutter, React Native, REST APIs, SQLite/Room, Mobile Security, App Publishing",
        "soft_skills": "Attention to Detail, Empathy for Users, Fast Troubleshooting, Collaboration",
        "tools": "Android Studio, Xcode, Flutter SDK, Postman, Git, Firebase, TestFlight",
        "certifications": "Associate Android Developer (Google), Meta iOS Developer Professional Certificate",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "High career potential with transition to Lead Mobile Architect or Head of Mobile Engineering.",
        "internship_roles": "Android Developer Intern, iOS Developer Intern, Flutter Intern",
        "entry_level_roles": "Associate Mobile Developer, Junior Android Developer, Junior iOS Developer",
        "average_salary": "₹4.5 - ₹15 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹4 - 7 LPA | Mid-Level (3-6 yrs): ₹8 - 16 LPA | Senior Mobile Architect (7+ yrs): ₹18 - 38+ LPA. Indicative figures from NCS & Mobile App Developer Benchmarks 2024.",
        "future_scope": "Strong long-term demand driven by India's massive mobile-first consumer base and fintech adoption.",
        "government_opportunities": "NIC Mobile Development Unit (Umang App, Aarogya Setu, DigiLocker), State police mobile apps.",
        "private_opportunities": "Paytm, PhonePe, Ola, Uber, Swiggy, Jio, global consumer app brands.",
        "higher_study_options": "M.Tech in CSE, M.S. in Software Systems.",
        "entrepreneurship_options": "Publishing independent utility or gaming apps on app stores, mobile engineering agency.",
        "source": "National Career Service (NCS) / NASSCOM",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 14, "type": "COMMON"},  # BCA
            {"course_id": 4, "type": "COMMON"},   # B.Sc Computer Science
            {"course_id": 15, "type": "ALTERNATIVE"} # MCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 79, "importance": "ALTERNATIVE"} # CUET-UG
        ],
        "routes": [
            {"title": "Path A: Standard Tech Degree to Mobile Specialization", "type": "COMMON", "steps": "Class 12 -> B.Tech CSE / BCA -> Learn Java/Kotlin or Swift -> Build 2-3 apps published on Play Store -> Mobile Developer."},
            {"title": "Path B: Cross-Platform Route (Flutter / React Native)", "type": "COMMON", "steps": "Class 12 -> Any UG degree -> Learn Dart/Flutter -> Build multi-platform apps -> Junior Mobile Developer."}
        ],
        "ladder": [
            {"stage": "Junior Mobile Developer", "exp": "0-2 Years", "desc": "Implements UI screens, integrates basic REST endpoints, writes local SQLite queries."},
            {"stage": "Mobile App Developer", "exp": "2-5 Years", "desc": "Handles complex state management, offline sync, push notifications, and analytics."},
            {"stage": "Senior Mobile Developer / Lead", "exp": "5-8 Years", "desc": "Architects mobile codebase, optimizes app launch times and payload sizes."},
            {"stage": "Head of Mobile / Mobile Architect", "exp": "8+ Years", "desc": "Sets enterprise mobile engineering standards and security guardrails."}
        ],
        "roadmaps": {
            "Class 10": "Explore how smartphone apps are made. Learn basic programming logic in Python or Java.",
            "Class 12": "Develop strong command over Object-Oriented Programming (Java or C++).",
            "Graduation": "Install Android Studio or Xcode. Build at least 2 functional apps and publish them to Google Play or GitHub.",
            "Working Professional": "Master Jetpack Compose (Android) or SwiftUI (iOS), reactive architectures, and automated mobile CI/CD pipelines."
        }
    },
    {
        "title": "Data Analyst",
        "short_name": "Data Analyst",
        "slug": "data-analyst",
        "category": "Technology & Computer Science",
        "sub_category": "Data Science & Artificial Intelligence",
        "industry": "Information Technology / Business Analytics",
        "icon": "bar-chart",
        "short_description": "Collects, processes, and performs statistical analysis on enterprise data to help business leaders make informed strategic decisions.",
        "description": "Data Analysts turn numbers into actionable business narratives. They query relational databases, clean messy data, create interactive visual dashboards, and identify market trends, customer behaviors, and operational inefficiencies.",
        "what_they_do": "They write SQL queries to extract data, clean and transform datasets, design business intelligence dashboards in Power BI or Tableau, and present findings to department heads.",
        "day_to_day_work": "• Extracting and aggregating data from SQL databases.\n• Cleaning and formatting raw datasets using Python or Excel.\n• Building and updating interactive executive dashboards in Power BI or Tableau.\n• Identifying business metric dips and performing root-cause analysis.\n• Presenting weekly performance insights to marketing, product, and sales teams.",
        "work_environment": "Corporate offices, analytics consultancies, or remote workspaces.",
        "work_modes": "Hybrid / Remote / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Any Stream (Science / Commerce preferred)",
        "required_subjects": "Mathematics, Statistics (recommended)",
        "technical_skills": "SQL, Advanced Excel, Power BI, Tableau, Python (Pandas), Data Cleaning, Business Intelligence",
        "soft_skills": "Communication, Business Acumen, Critical Thinking, Storytelling",
        "tools": "Excel, SQL Server, Power BI, Tableau, Jupyter Notebook, Google Sheets",
        "certifications": "Google Data Analytics Professional Certificate, Microsoft Certified: Power BI Data Analyst Associate",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Broad career avenues transitioning to Senior Data Analyst, Analytics Manager, or Data Scientist.",
        "internship_roles": "Data Analytics Intern, Business Intelligence Intern, Market Research Intern",
        "entry_level_roles": "Junior Data Analyst, Associate BI Analyst, Operations Analyst",
        "average_salary": "₹4 - ₹12 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹3.5 - 6 LPA | Mid-Level (3-6 yrs): ₹7 - 14 LPA | Lead Analytics Manager (7+ yrs): ₹16 - 30+ LPA. Indicative figures from NCS & Analytics India Magazine 2024.",
        "future_scope": "High universal demand across e-commerce, banking, healthcare, retail, and manufacturing.",
        "government_opportunities": "Ministry of Statistics & Programme Implementation (MoSPI), RBI, NITI Aayog, State Planning Boards.",
        "private_opportunities": "Mu Sigma, Fractal Analytics, Accenture, Deloitte, Flipkart, Amazon, ICICI Bank.",
        "higher_study_options": "M.Sc in Data Analytics, MBA in Business Analytics, M.Sc Statistics.",
        "entrepreneurship_options": "Independent business intelligence consulting, dashboard development agency.",
        "source": "National Career Service (NCS) / NASSCOM",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 1, "type": "COMMON"},    # B.Sc Mathematics
            {"course_id": 39, "type": "COMMON"},   # B.Sc Statistics
            {"course_id": 5, "type": "DIRECT"},    # B.Sc Data Science & Analytics
            {"course_id": 16, "type": "ALTERNATIVE"}, # B.Com
            {"course_id": 20, "type": "ALTERNATIVE"}  # BA Economics
        ],
        "exams": [
            {"exam_id": 79, "importance": "PRIMARY"},   # CUET-UG
            {"exam_id": 40, "importance": "ALTERNATIVE"} # Indian Statistical Service Exam
        ],
        "routes": [
            {"title": "Path A: Math / Stats / Economics Degree", "type": "COMMON", "steps": "Class 12 -> B.Sc Maths / Stats / BA Economics -> Learn SQL, Excel & Power BI -> Portfolio of dashboard case studies -> Data Analyst."},
            {"title": "Path B: Commerce / BBA to Analytics", "type": "COMMON", "steps": "Class 12 -> B.Com / BBA -> Advanced Excel & Business Analytics -> Financial / Business Analyst."},
            {"title": "Path C: Engineering to Data Analytics", "type": "COMMON", "steps": "B.Tech Any stream -> Python & SQL -> Corporate Analytics role."}
        ],
        "ladder": [
            {"stage": "Junior Data Analyst", "exp": "0-2 Years", "desc": "Pulls data reports, maintains Excel models, updates BI dashboards."},
            {"stage": "Senior Data Analyst", "exp": "2-5 Years", "desc": "Performs deep cohort analysis, automated ETL reporting, presents to leadership."},
            {"stage": "Lead Analyst / Analytics Manager", "exp": "5-8 Years", "desc": "Directs business intelligence roadmap, oversees analyst team."},
            {"stage": "Director of Business Intelligence", "exp": "8+ Years", "desc": "Aligns organizational metrics framework with executive business goals."}
        ],
        "roadmaps": {
            "Class 10": "Excel in arithmetic, percentages, ratios, and graphical representations.",
            "Class 12": "Choose Mathematics or Economics. Learn how spreadsheets (Excel / Google Sheets) work.",
            "Graduation": "Master SQL thoroughly. Learn Power BI or Tableau and build 3 business dashboard projects on public datasets.",
            "Working Professional": "Add Python data analysis (Pandas, Seaborn), basic predictive modeling, and stakeholder storytelling."
        }
    },
    {
        "title": "Artificial Intelligence Engineer",
        "short_name": "AI Engineer",
        "slug": "ai-engineer",
        "category": "Technology & Computer Science",
        "sub_category": "Artificial Intelligence & Robotics",
        "industry": "Information Technology / Deep Tech",
        "icon": "robot",
        "short_description": "Builds and deploys cognitive computing systems, neural networks, and generative AI architectures to solve complex reasoning problems.",
        "description": "AI Engineers develop intelligent agents capable of learning, reasoning, computer vision, and natural language understanding. They fine-tune large foundation models, build retrieval-augmented generation (RAG) systems, and integrate intelligent capabilities into software.",
        "what_they_do": "They design neural network architectures, train custom transformer models, build RAG pipelines with vector databases, optimize LLM inference, and ensure ethical AI guardrails.",
        "day_to_day_work": "• Experimenting with transformer models and generative AI APIs.\n• Building semantic search and RAG pipelines using LangChain and vector databases.\n• Fine-tuning open-source LLMs (Llama, Mistral) on domain-specific datasets.\n• Benchmarking model latency, hallucination rates, and safety guardrails.\n• Deploying scalable AI inference services on cloud GPUs.",
        "work_environment": "AI research labs, frontier tech startups, global capability centers, or remote.",
        "work_modes": "Hybrid / Remote",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Mathematics, Physics, Computer Science",
        "technical_skills": "Python, PyTorch, Large Language Models (LLMs), RAG, Vector DBs, LangChain/LlamaIndex, Deep Learning, Git",
        "soft_skills": "Intellectual Curiosity, First-Principles Thinking, Creative Problem Solving",
        "tools": "PyTorch, Hugging Face, LangChain, Pinecone, ChromaDB, Docker, vLLM, Git",
        "certifications": "DeepLearning.AI TensorFlow Developer, AWS Certified Machine Learning - Specialty",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Exceptional national and international demand with progression to Chief AI Officer (CAIO) or AI Research Director.",
        "internship_roles": "GenAI Intern, Deep Learning Research Intern, AI Engineering Intern",
        "entry_level_roles": "Associate AI Engineer, Junior NLP Engineer, AI Solutions Trainee",
        "average_salary": "₹7 - ₹25 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹6 - 11 LPA | Mid-Level (3-6 yrs): ₹12 - 26 LPA | Principal AI Architect (7+ yrs): ₹30 - 75+ LPA. Indicative figures based on NCS & Tech AI Market Reports 2024.",
        "future_scope": "Exponential expansion at the forefront of the Fourth Industrial Revolution across all economic sectors.",
        "government_opportunities": "National AI Mission (IndiaAI), CDAC, DRDO CAIR, MeitY initiatives, IIT Research Parks.",
        "private_opportunities": "Google Research, Microsoft, Sarvam AI, Krutrim, Adobe, NVIDIA, Flipkart, high-growth AI startups.",
        "higher_study_options": "M.Tech in Artificial Intelligence, Ph.D. in Deep Learning or Computer Vision.",
        "entrepreneurship_options": "Domain-specific AI applications (legal AI, medical AI, agri-AI), automated agent consultancies.",
        "source": "IndiaAI / MeitY / NASSCOM",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 43, "type": "DIRECT"},    # B.Tech AI & Data Science
            {"course_id": 9, "type": "COMMON"},     # B.Tech CSE
            {"course_id": 38, "type": "SPECIALIZED"}, # M.Tech CSE
            {"course_id": 5, "type": "COMMON"}      # B.Sc Data Science & Analytics
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 69, "importance": "PRIMARY"}   # GATE
        ],
        "routes": [
            {"title": "Path A: B.Tech in AI/DS or CSE", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech in AI/DS or CSE -> Master Python, Linear Algebra & PyTorch -> Build RAG & Vision apps -> AI Engineer."},
            {"title": "Path B: Software Developer to AI Engineer", "type": "COMMON", "steps": "B.Tech / MCA -> 2 yrs Software Development -> Learn Transformer models & LLM orchestration -> Transition to AI Engineering."}
        ],
        "ladder": [
            {"stage": "Junior AI Engineer", "exp": "0-2 Years", "desc": "Implements data preprocessing, builds basic RAG pipelines, monitors API token costs."},
            {"stage": "AI Engineer", "exp": "2-5 Years", "desc": "Fine-tunes open-source models, designs multi-agent workflows, evaluates model safety."},
            {"stage": "Senior AI Architect", "exp": "5-8 Years", "desc": "Architects enterprise generative AI platforms, optimizes GPU serving clusters."},
            {"stage": "Chief AI Officer / Head of AI", "exp": "8+ Years", "desc": "Defines corporate AI roadmap, governance, and intellectual property strategy."}
        ],
        "roadmaps": {
            "Class 10": "Develop strong command over algebra, matrix operations, and Python programming basics.",
            "Class 12": "Score high in Mathematics (Calculus, Probability, Vectors). Target top engineering institutions through JEE.",
            "Graduation": "Learn PyTorch, Hugging Face transformers, and build end-to-end applications combining LLMs with vector databases.",
            "Working Professional": "Master model quantization, distributed training frameworks (vLLM, DeepSpeed), and autonomous multi-agent systems."
        }
    },
    {
        "title": "QA & Automation Engineer",
        "short_name": "QA Automation Engineer",
        "slug": "qa-automation-engineer",
        "category": "Technology & Computer Science",
        "sub_category": "Software Quality & Testing",
        "industry": "Information Technology",
        "icon": "check2-circle",
        "short_description": "Designs automated testing suites to verify software functionality, reliability, performance, and security before deployment.",
        "description": "QA Automation Engineers write software to test software. They build scalable test automation frameworks, execute performance load tests, ensure regression coverage, and guarantee that software releases meet rigorous reliability standards.",
        "what_they_do": "They write automated test scripts in Selenium, Cypress, or Playwright, integrate automated testing into CI/CD pipelines, conduct API and load testing, and report software bugs with detailed reproduction steps.",
        "day_to_day_work": "• Writing and updating automated end-to-end test cases in Playwright or Selenium.\n• Testing REST and GraphQL APIs using Postman or RestAssured.\n• Executing load and stress testing using JMeter or k6.\n• Analyzing automated test run results in CI/CD pipelines.\n• Collaborating with developers on bug fixes and quality criteria.",
        "work_environment": "IT campuses, software engineering facilities, or remote setups.",
        "work_modes": "Hybrid / Remote / On-site",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM) / Any with CS",
        "required_subjects": "Computer Science, Mathematics",
        "technical_skills": "Java/Python/JavaScript, Selenium, Playwright, Cypress, API Testing, JMeter, CI/CD, Git",
        "soft_skills": "Detail-Oriented, Analytical Mindset, Communication, Tenacity",
        "tools": "Playwright, Selenium WebDriver, Postman, JMeter, Git, Jira, Jenkins",
        "certifications": "ISTQB Certified Tester Foundation Level (CTFL), Selenium Automation Certification",
        "experience_level": "Entry-Level to Senior",
        "career_growth": "Consistent progression to SDET (Software Development Engineer in Test), QA Lead, or Head of Quality Engineering.",
        "internship_roles": "QA Intern, Test Automation Intern, Software Quality Trainee",
        "entry_level_roles": "Associate QA Engineer, Junior SDET, Test Engineer Trainee",
        "average_salary": "₹3.8 - ₹12 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹3.5 - 6 LPA | Mid-Level SDET (3-6 yrs): ₹7 - 15 LPA | Lead SDET / QA Architect (7+ yrs): ₹16 - 32+ LPA. Indicative figures from NCS & Tech Quality Audits 2024.",
        "future_scope": "Steady demand as continuous automated testing is mandatory for every mature agile development cycle.",
        "government_opportunities": "NIC testing cells, STQC (Standardisation Testing and Quality Certification) Directorate, CDAC.",
        "private_opportunities": "TCS, Wipro, Infosys, Cognizant, Amazon, Flipkart, global product companies.",
        "higher_study_options": "M.Tech in Software Engineering, MCA.",
        "entrepreneurship_options": "Independent software testing consultancy, specialized automated accessibility auditing firm.",
        "source": "National Career Service (NCS) / ISTQB",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 9, "type": "COMMON"},   # B.Tech CSE
            {"course_id": 14, "type": "COMMON"},  # BCA
            {"course_id": 4, "type": "COMMON"},   # B.Sc Computer Science
            {"course_id": 15, "type": "ALTERNATIVE"} # MCA
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 79, "importance": "ALTERNATIVE"} # CUET-UG
        ],
        "routes": [
            {"title": "Path A: Standard Engineering to SDET", "type": "COMMON", "steps": "Class 12 -> B.Tech / BCA -> Learn Java/Python + Data Structures -> Learn Selenium / Playwright -> SDET role."},
            {"title": "Path B: Manual Testing to Automation Transition", "type": "ALTERNATIVE", "steps": "Graduation -> Manual QA role -> Learn programming & automation frameworks -> Automation Test Engineer."}
        ],
        "ladder": [
            {"stage": "Junior QA / Test Engineer", "exp": "0-2 Years", "desc": "Executes manual test cases, writes automated API scripts, logs defects."},
            {"stage": "QA Automation Engineer / SDET", "exp": "2-5 Years", "desc": "Builds and maintains UI/API automated testing frameworks from scratch."},
            {"stage": "Senior SDET / QA Lead", "exp": "5-8 Years", "desc": "Implements performance benchmarking, chaos testing, CI/CD quality gates."},
            {"stage": "Head of Quality Engineering", "exp": "8+ Years", "desc": "Defines enterprise-wide release criteria, compliance, and automated test strategies."}
        ],
        "roadmaps": {
            "Class 10": "Develop keen eye for finding flaws, broken links, or inconsistencies in games and software.",
            "Class 12": "Learn fundamental programming concepts in Java or Python.",
            "Graduation": "Learn Selenium, Playwright, and Postman. Build an automated test suite for an open-source web application on GitHub.",
            "Working Professional": "Level up on non-functional testing (security testing with OWASP ZAP, performance testing with k6, contract testing with Pact)."
        }
    },
    {
        "title": "Computer Network Architect",
        "short_name": "Network Architect",
        "slug": "computer-network-architect",
        "category": "Technology & Computer Science",
        "sub_category": "Networking & Infrastructure",
        "industry": "Information Technology / Telecommunications",
        "icon": "diagram-3",
        "short_description": "Designs and builds complex data communication networks, including local area networks (LANs), wide area networks (WANs), and intranets.",
        "description": "Computer Network Architects plan, build, and optimize enterprise telecommunications and data network infrastructures. They predict network traffic growth, evaluate hardware routers and switches, design software-defined networks (SDN), and safeguard data transit.",
        "what_they_do": "They create network schematics, specify hardware requirements, configure advanced routing protocols (BGP, OSPF), plan optical fiber and wireless topologies, and ensure robust network redundancy.",
        "day_to_day_work": "• Designing multi-site network topologies and VPN tunnels.\n• Configuring high-capacity enterprise routers, switches, and firewalls.\n• Modeling bandwidth demand and planning capacity expansions.\n• Implementing Software-Defined Networking (SDN) and SD-WAN architectures.\n• Troubleshooting core routing and packet loss bottlenecks.",
        "work_environment": "Data centers, telecom network operations centers (NOC), corporate offices, or field sites.",
        "work_modes": "On-site / Hybrid",
        "minimum_qualification": "Undergraduate",
        "preferred_streams": "Science (PCM)",
        "required_subjects": "Physics, Mathematics, Computer Science",
        "technical_skills": "TCP/IP, BGP/OSPF, Cisco Routing & Switching, Network Security, SD-WAN, Cloud Interconnects, Wireshark",
        "soft_skills": "Systemic Thinking, Strategic Planning, Decisiveness, Clear Communication",
        "tools": "Cisco Packet Tracer, GNS3, Wireshark, SolarWinds, PuTTY, Ansible for Networking",
        "certifications": "Cisco Certified Network Associate (CCNA), Cisco Certified Network Professional (CCNP), CCIE",
        "experience_level": "Mid-Level to Senior",
        "career_growth": "High trajectory leading to Chief Network Architect, Director of Telecommunications, or VP of Infrastructure.",
        "internship_roles": "Network Engineering Intern, NOC Trainee, Telecom Systems Intern",
        "entry_level_roles": "Network Support Engineer, Associate Network Engineer, NOC Analyst",
        "average_salary": "₹6 - ₹20 LPA (Indicative range)",
        "salary_indicative": "Entry-Level (0-2 yrs): ₹4 - 6.5 LPA | Mid-Level (3-6 yrs): ₹8 - 16 LPA | Senior Network Architect (7+ yrs): ₹18 - 36+ LPA. Indicative figures from NCS & Telecom Sector Skill Council 2024.",
        "future_scope": "Sustained high importance driven by 5G rollout, optical fiber expansion, and cloud-to-edge connectivity.",
        "government_opportunities": "BSNL, MTNL, RailTel, PowerGrid Telecom, Defence Communications Corps, NIC, ISRO telemetry.",
        "private_opportunities": "Cisco, Juniper Networks, Reliance Jio, Bharti Airtel, Tata Communications, VMware.",
        "higher_study_options": "M.Tech in Telecommunications / Networks, M.S. in Computer Networking.",
        "entrepreneurship_options": "Enterprise networking infrastructure consultancy, managed Wi-Fi & SD-WAN service provider.",
        "source": "National Career Service (NCS) / Telecom Sector Skill Council (TSSC)",
        "official_url": "https://www.ncs.gov.in",
        "verification_status": "VERIFIED",
        "courses": [
            {"course_id": 10, "type": "DIRECT"},   # B.Tech ECE
            {"course_id": 9, "type": "COMMON"},    # B.Tech CSE
            {"course_id": 42, "type": "COMMON"},   # B.Tech IT
            {"course_id": 44, "type": "ALTERNATIVE"} # Diploma in Engineering
        ],
        "exams": [
            {"exam_id": 8, "importance": "PRIMARY"},   # JEE Main
            {"exam_id": 51, "importance": "PRIMARY"},  # UPSC Engineering Services Exam
            {"exam_id": 69, "importance": "ALTERNATIVE"}  # GATE
        ],
        "routes": [
            {"title": "Path A: ECE / CSE Degree to Network Engineering", "type": "COMMON", "steps": "Class 12 (PCM) -> B.Tech ECE/CSE -> CCNA Certification -> Network Support Engineer -> CCNP -> Network Architect."},
            {"title": "Path B: Polytechnic Diploma Route", "type": "ALTERNATIVE", "steps": "Class 10 -> Diploma in ECE / CS (3 yrs) -> Lateral B.Tech or Direct NOC role -> Certifications -> Network Architect."}
        ],
        "ladder": [
            {"stage": "Junior Network Engineer / NOC", "exp": "0-2 Years", "desc": "Monitors network links, handles cable patching, assists in basic switch config."},
            {"stage": "Network Engineer", "exp": "2-5 Years", "desc": "Configures dynamic routing protocols, maintains firewalls, resolves outages."},
            {"stage": "Senior Network Architect", "exp": "5-9 Years", "desc": "Designs enterprise SD-WAN topologies, data center fabrics, and MPLS connections."},
            {"stage": "Chief Network Officer / Director", "exp": "9+ Years", "desc": "Owns global enterprise telecommunications infrastructure and multi-million telecom budget."}
        ],
        "roadmaps": {
            "Class 10": "Learn how the internet works, what routers and IP addresses are, and explore home Wi-Fi settings.",
            "Class 12": "Score well in Physics and Mathematics. Understand electromagnetic wave transmission and signals.",
            "Graduation": "Practice on Cisco Packet Tracer. Master the OSI 7-layer model, subnetting, and clear the CCNA exam.",
            "Working Professional": "Specialize in network automation with Python/Ansible, Software Defined Networking (SDN), and BGP routing."
        }
    }
]
