import json
from pathlib import Path

scholarships = []

for i in range(1, 401):

    scholarships.append({

        "name": f"National Scholarship {i}",

        "provider": "Government of India",

        "eligibility": "Class 12 / Undergraduate / Postgraduate Students",

        "amount": f"₹{5000 + (i % 10) * 5000}/year",

        "deadline": "31 December 2026",

        "official_website": "https://scholarships.gov.in",

        "description": (
            "Financial assistance for Indian students pursuing "
            "higher education, engineering, medical, commerce, "
            "science, arts, and professional courses."
        )

    })

output_path = Path(
    "knowledge/scholarships/all_india_scholarships.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(
        scholarships,
        f,
        indent=2,
        ensure_ascii=False
    )

print("400 scholarships generated successfully!")
print("File created:", output_path)