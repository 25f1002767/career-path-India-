import os
import re

template_dir = "templates"
pattern = re.compile(r'href=[\"\']\{\{\s*(s|scholarship)\.(official_url|official_website|website)\s*\}\}[\"\']', re.IGNORECASE)

violations = []
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line_no, line in enumerate(f, 1):
                    if pattern.search(line):
                        if "apply" in line.lower():
                            violations.append((path, line_no, line.strip()))

print(f"Total templates scanned. Violations where official_website is used as Apply: {len(violations)}")
for v in violations:
    print(f"{v[0]}:{v[1]} -> {v[2]}")
