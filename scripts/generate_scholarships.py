"""
National Scholarships Dataset Validator & Formatter
===================================================
NOTE: Synthetic generation of dummy scholarships ("National Scholarship {i}")
is strictly deprecated and disabled to protect platform data credibility.
This script validates knowledge/scholarships/all_india_scholarships.json
ensuring all records have segregated official_website and official_application_url.
"""
import json
from pathlib import Path

knowledge_file = Path("knowledge/scholarships/all_india_scholarships.json")

if not knowledge_file.exists():
    print(f"Error: {knowledge_file} does not exist.")
    exit(1)

with open(knowledge_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Validating {len(data)} verified national scholarships...")
valid_count = 0
for idx, sch in enumerate(data, 1):
    title = sch.get("name")
    web = sch.get("official_website")
    app = sch.get("official_application_url")

    # Safety check against synthetic dummy records
    if "national scholarship " in title.lower() and title.split()[-1].isdigit():
        print(f"Warning: Synthetic dummy scholarship detected: {title}. Must be flagged!")
        continue

    if not app:
        print(f"Record #{idx} '{title}' is missing official_application_url")
    elif app == web:
        print(f"Record #{idx} '{title}' has identical website and application_url: {app}")
    else:
        valid_count += 1

print(f"[OK] Completed validation: {valid_count}/{len(data)} scholarships have segregated authentic application links.")