import json
from pathlib import Path

exam_groups = [

    # UPSC
    ("UPSC Civil Services", "UPSC"),
    ("UPSC Engineering Services", "UPSC"),
    ("UPSC CDS", "UPSC"),
    ("UPSC NDA", "UPSC"),
    ("UPSC CAPF", "UPSC"),

    # SSC
    ("SSC CGL", "SSC"),
    ("SSC CHSL", "SSC"),
    ("SSC MTS", "SSC"),
    ("SSC CPO", "SSC"),
    ("SSC GD Constable", "SSC"),

    # Banking
    ("IBPS PO", "Banking"),
    ("IBPS Clerk", "Banking"),
    ("SBI PO", "Banking"),
    ("SBI Clerk", "Banking"),
    ("RBI Assistant", "Banking"),
    ("RBI Grade B", "Banking"),

    # Railway
    ("RRB NTPC", "Railway"),
    ("RRB Group D", "Railway"),
    ("RRB JE", "Railway"),
    ("RRB ALP", "Railway"),

    # Teaching
    ("CTET", "Teaching"),
    ("UGC NET", "Teaching"),
    ("KVS Recruitment", "Teaching"),
    ("NVS Recruitment", "Teaching"),
    ("State TET", "Teaching"),

    # Defence
    ("Indian Army Agniveer", "Defence"),
    ("Indian Navy Agniveer", "Defence"),
    ("Indian Air Force Agniveer", "Defence"),

    # Police
    ("State Police SI", "Police"),
    ("State Police Constable", "Police"),
    ("CRPF Recruitment", "Police"),
    ("BSF Recruitment", "Police"),

    # State PSC
    ("MPPSC", "State PSC"),
    ("UPPSC", "State PSC"),
    ("RPSC", "State PSC"),
    ("BPSC", "State PSC"),
    ("MPSC", "State PSC"),

    # Engineering / Technical
    ("GATE", "Engineering"),
    ("ISRO Scientist Exam", "Engineering"),
    ("DRDO CEPTAM", "Engineering"),
    ("BHEL Engineer Trainee", "Engineering"),

    # Medical
    ("NEET UG", "Medical"),
    ("AIIMS Nursing", "Medical"),
    ("NORCET", "Medical")
]

eligibility_map = {
    "UPSC": "Graduation",
    "SSC": "12th / Graduation",
    "Banking": "Graduation",
    "Railway": "10th / 12th / Diploma / Graduation",
    "Teaching": "Graduation + B.Ed",
    "Defence": "10th / 12th Pass",
    "Police": "10th / 12th / Graduation",
    "State PSC": "Graduation",
    "Engineering": "Engineering Degree",
    "Medical": "12th PCB / Nursing Qualification"
}

websites = {
    "UPSC": "https://www.upsc.gov.in",
    "SSC": "https://ssc.gov.in",
    "Banking": "https://www.ibps.in",
    "Railway": "https://www.rrbcdg.gov.in",
    "Teaching": "https://ctet.nic.in",
    "Defence": "https://joinindianarmy.nic.in",
    "Police": "https://www.crpf.gov.in",
    "State PSC": "https://mppsc.mp.gov.in",
    "Engineering": "https://gate2026.iitr.ac.in",
    "Medical": "https://neet.nta.nic.in"
}

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

exams = []

for i in range(1, 401):

    title, category = exam_groups[i % len(exam_groups)]

    exams.append({

        "name": f"{title} {i}",

        "category": category,

        "eligibility": eligibility_map[category],

        "age_limit": "18-32 Years",

        "conducted_by": category + " Authority",

        "official_website": websites[category],

        "notification_month": months[i % len(months)],

        "description": (
            f"{title} is a competitive examination conducted in India "
            f"for recruitment in the {category.lower()} sector. "
            "Candidates should regularly check the official website "
            "for notifications, syllabus, eligibility, and application dates."
        )

    })

output_path = Path(
    "knowledge/exams/all_india_exams.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(
        exams,
        f,
        indent=2,
        ensure_ascii=False
    )

print("400 exams generated successfully!")
print("File created:", output_path)