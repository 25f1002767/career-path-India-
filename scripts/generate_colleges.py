import json
from pathlib import Path

college_groups = [
    ("IIT", "Engineering"),
    ("NIT", "Engineering"),
    ("IIIT", "Engineering"),
    ("AIIMS", "Medical"),
    ("Government Medical College", "Medical"),
    ("Indian Institute of Management", "Management"),
    ("National Law University", "Law"),
    ("Government Arts College", "Arts"),
    ("Government Commerce College", "Commerce"),
    ("State Science College", "Science"),
    ("Agriculture University", "Agriculture"),
    ("Institute of Design", "Design"),
    ("College of Pharmacy", "Pharmacy"),
    ("College of Nursing", "Nursing"),
    ("Hotel Management Institute", "Hotel Management"),
    ("School of Architecture", "Architecture"),
    ("Veterinary Science College", "Veterinary"),
    ("Teacher Education College", "Education")
]

states = [
    "Madhya Pradesh",
    "Maharashtra",
    "Karnataka",
    "Tamil Nadu",
    "Uttar Pradesh",
    "Delhi",
    "Rajasthan",
    "Gujarat",
    "West Bengal",
    "Telangana",
    "Kerala",
    "Punjab",
    "Haryana",
    "Odisha",
    "Bihar",
    "Assam",
    "Chhattisgarh",
    "Andhra Pradesh",
    "Jharkhand",
    "Uttarakhand"
]

cities = [
    "Bhopal", "Indore", "Gwalior", "Mumbai", "Pune",
    "Bengaluru", "Chennai", "Hyderabad", "Lucknow", "Delhi",
    "Jaipur", "Ahmedabad", "Kolkata", "Kochi", "Chandigarh",
    "Bhubaneswar", "Patna", "Ranchi", "Dehradun", "Visakhapatnam"
]

colleges = []

for i in range(1, 401):

    group, course = college_groups[i % len(college_groups)]

    city = cities[i % len(cities)]

    state = states[i % len(states)]

    name = f"{group} {city}"

    colleges.append({

        "name": name,

        "city": city,

        "state": state,

        "course": course,

        "fees": f"₹{5000 + (i % 20) * 10000} per year",

        "placement": f"{50 + (i % 45)}% Average Placement",

        "description": (
            f"{name} is a reputed institution offering "
            f"{course} education with experienced faculty, "
            "modern infrastructure, and career opportunities."
        ),

        "official_website": (
            "https://www.education.gov.in"
        )

    })

output_path = Path(
    "knowledge/colleges/top_india_colleges.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(
        colleges,
        f,
        indent=2,
        ensure_ascii=False
    )

print("400 colleges generated successfully!")
print("File created:", output_path)