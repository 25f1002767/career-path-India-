import json

companies = [
    "Infosys", "TCS", "Wipro", "HCLTech", "Accenture",
    "Capgemini", "IBM India", "Deloitte India", "KPMG India",
    "Tech Mahindra", "Cognizant", "Amazon", "Google India",
    "Microsoft India", "Flipkart", "Paytm", "Zomato", "Swiggy",
    "Reliance Jio", "Oracle India"
]

roles = [
    ("Python Developer Intern", ["Python", "Flask", "SQL"]),
    ("Web Development Intern", ["HTML", "CSS", "JavaScript"]),
    ("Data Science Intern", ["Python", "SQL", "Machine Learning"]),
    ("AI / ML Intern", ["Python", "TensorFlow", "Machine Learning"]),
    ("Frontend Developer Intern", ["React", "JavaScript", "CSS"]),
    ("Backend Developer Intern", ["Python", "Django", "REST API"]),
    ("Cloud Engineering Intern", ["AWS", "Linux", "Cloud Computing"]),
    ("Cyber Security Intern", ["Networking", "Linux", "Security"]),
    ("Full Stack Developer Intern", ["Node.js", "MongoDB", "JavaScript"]),
    ("Business Analyst Intern", ["Excel", "SQL", "Power BI"])
]

cities = [
    "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Chennai",
    "Noida", "Gurugram", "Ahmedabad", "Kolkata", "Delhi"
]

internships = []

for i in range(400):
    role, skills = roles[i % len(roles)]
    company = companies[i % len(companies)]
    city = cities[i % len(cities)]

    internships.append({
        "title": role,
        "company": company,
        "location": city,
        "mode": ["Remote", "Hybrid", "Onsite"][i % 3],
        "stipend": f"₹{12000 + (i % 10) * 3000}/month",
        "duration": f"{2 + (i % 5)} Months",
        "skills": skills,
        "apply_link": f"https://www.{company.lower().replace(' ', '').replace('india', '')}.com/careers"
    })

with open(
    "knowledge/internships/technology_internships.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(internships, f, indent=2, ensure_ascii=False)

print("400 internships generated successfully!")