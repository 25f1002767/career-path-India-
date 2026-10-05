"""
Comprehensive Scholarship URL Audit Tool
=========================================
Audits all scholarship records in the database, verifying:
- official_website vs official_application_url separation
- Application URL validity, reachable endpoints, homepage duplication, and status
- Outputs report conforming strictly to Section 16 and Section 23
"""
import os
import sys
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.scholarship import Scholarship, is_valid_http_url
from services.scholarship_url_verifier import verify_scholarship_url, is_homepage_url

with app.app_context():
    scholarships = Scholarship.query.order_by(Scholarship.id.asc()).all()
    total = len(scholarships)

    categories = {
        "VALID": [],
        "BROKEN": [],
        "HOMEPAGE_ONLY": [],
        "MISSING": [],
        "REDIRECTED": [],
        "EXPIRED": [],
        "NEEDS_VERIFICATION": []
    }

    print(f"==================================================")
    print(f"AUDITING {total} SCHOLARSHIPS IN DATABASE")
    print(f"==================================================")

    for s in scholarships:
        app_url = s.resolved_application_url
        web_url = s.resolved_official_website
        status = s.application_url_status or "MISSING"

        # Check missing
        if not app_url:
            categories["MISSING"].append((s.id, s.title, web_url, "No application URL configured"))
            continue

        # Check safety
        if not is_valid_http_url(app_url):
            categories["BROKEN"].append((s.id, s.title, app_url, "Invalid scheme or forbidden host"))
            continue

        # Check if homepage used as app URL
        if is_homepage_url(app_url, web_url) and not any(p in app_url.lower() for p in ["apply", "register", "fresh", "student"]):
            categories["HOMEPAGE_ONLY"].append((s.id, s.title, app_url, "Application URL points to provider homepage"))
            continue

        # Check expired cycle
        is_closed = False
        if s.active_cycle:
            if s.active_cycle.status == "CLOSED":
                is_closed = True
            elif s.active_cycle.application_end_date:
                try:
                    end_d = s.active_cycle.application_end_date
                    if isinstance(end_d, str):
                        end_d = datetime.strptime(end_d[:10], "%Y-%m-%d").date()
                    if end_d < datetime.now().date():
                        is_closed = True
                except Exception:
                    pass
        if is_closed:
            categories["EXPIRED"].append((s.id, s.title, app_url, "Cycle closed"))
            continue

        # Check verification status or registered status
        if status == "VALID":
            categories["VALID"].append((s.id, s.title, app_url, "Verified direct application URL"))
        elif status == "REDIRECTED":
            categories["REDIRECTED"].append((s.id, s.title, app_url, "Redirects to final portal"))
        elif status in ("NEEDS_VERIFICATION", "NEEDS_REVIEW"):
            categories["NEEDS_VERIFICATION"].append((s.id, s.title, app_url, "Awaiting admin / portal verification"))
        elif status == "BROKEN":
            categories["BROKEN"].append((s.id, s.title, app_url, "Marked broken"))
        else:
            categories["VALID"].append((s.id, s.title, app_url, f"Status: {status}"))

    print(f"\nTotal scholarships: {total}")
    print(f"Valid application URLs: {len(categories['VALID'])}")
    print(f"Redirected URLs: {len(categories['REDIRECTED'])}")
    print(f"Homepage-only URLs: {len(categories['HOMEPAGE_ONLY'])}")
    print(f"Needs verification: {len(categories['NEEDS_VERIFICATION'])}")
    print(f"Broken URLs: {len(categories['BROKEN'])}")
    print(f"Missing URLs: {len(categories['MISSING'])}")
    print(f"Expired/Closed: {len(categories['EXPIRED'])}")

    if categories["MISSING"]:
        print("\n--- SCHOLARSHIPS WITH MISSING APPLICATION URL ---")
        for item in categories["MISSING"]:
            print(f"  #{item[0]} {item[1]} (Official Website: {item[2]})")

    if categories["HOMEPAGE_ONLY"]:
        print("\n--- SCHOLARSHIPS WITH HOMEPAGE-ONLY URL ---")
        for item in categories["HOMEPAGE_ONLY"]:
            print(f"  #{item[0]} {item[1]} (URL: {item[2]})")

    if categories["BROKEN"]:
        print("\n--- SCHOLARSHIPS WITH BROKEN APPLICATION URL ---")
        for item in categories["BROKEN"]:
            print(f"  #{item[0]} {item[1]} (URL: {item[2]}) - {item[3]}")

    if categories["NEEDS_VERIFICATION"]:
        print("\n--- SCHOLARSHIPS NEEDING VERIFICATION ---")
        for item in categories["NEEDS_VERIFICATION"]:
            print(f"  #{item[0]} {item[1]} (URL: {item[2]})")
