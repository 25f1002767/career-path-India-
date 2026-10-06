"""
Script to fix and update all internship application URLs in the database
with authentic, verified student portals and official statutory program links.
Eliminates dead links (like reliancejio.com) and generic corporate landing pages.
"""

import sys
import os
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.internship import Internship
from models.organisation import Organisation

# Exact verified student & internship portal mappings
PORTAL_MAP = {
    "infosys": "https://career.infosys.com/",
    "tcs": "https://www.tcs.com/careers",
    "wipro": "https://careers.wipro.com/early-careers",
    "hcltech": "https://www.hcltech.com/careers",
    "accenture": "https://www.accenture.com/in-en/careers",
    "capgemini": "https://www.capgemini.com/in-en/careers/",
    "ibm": "https://www.ibm.com/careers/early-career",
    "deloitte": "https://www.deloitte.com/in/en/careers.html",
    "kpmg": "https://kpmg.com/in/en/home/careers.html",
    "tech mahindra": "https://careers.techmahindra.com/",
    "cognizant": "https://www.cognizant.com/in/en/careers",
    "amazon": "https://www.amazon.jobs/en/business_categories/student-programs",
    "google": "https://careers.google.com/students/",
    "microsoft": "https://careers.microsoft.com/v2/global/en/students-and-graduates.html",
    "flipkart": "https://www.flipkartcareers.com/",
    "paytm": "https://paytm.com/careers/",
    "zomato": "https://www.zomato.com/careers",
    "swiggy": "https://careers.swiggy.com/",
    "reliance jio": "https://careers.jio.com/",
    "jio": "https://careers.jio.com/",
    "oracle": "https://www.oracle.com/careers/",
    "tulip": "https://internship.aicte-india.org/internships",
    "army": "https://internship.aicte-india.org/dashboards/indianarmy/internship-list",
    "nhai": "https://nhai.gov.in/",
    "cdac": "https://www.cdac.in/index.aspx?id=career_opportunities",
    "c-dac": "https://www.cdac.in/index.aspx?id=career_opportunities",
    "drdo": "https://rac.gov.in/",
    "cair": "https://rac.gov.in/",
    "isro": "https://www.vssc.gov.in/",
    "vssc": "https://www.vssc.gov.in/",
    "niti aayog": "https://www.niti.gov.in/",
    "rbi": "https://opportunities.rbi.org.in/",
    "supreme court": "https://www.sci.gov.in/recruitment/",
    "icmr": "https://icmr.gov.in/",
    "cdri": "https://cdri.res.in/",
    "csir": "https://cdri.res.in/",
    "maharashtra": "https://internship.aicte-india.org/",
    "k-tech": "https://internship.aicte-india.org/",
    "ktech": "https://internship.aicte-india.org/",
    "karnataka": "https://internship.aicte-india.org/",
    "tata motors": "https://www.tatamotors.com/careers/",
    "larsen": "https://www.larsentoubro.com/corporate/careers/",
    "l&t": "https://www.larsentoubro.com/corporate/careers/",
    "zoho": "https://www.zoho.com/careers/",
    "bel": "https://bel-india.in/",
}


def get_correct_portal(name: str, current_url: str = None) -> str:
    name_low = (name or "").lower().strip()
    for key, portal in PORTAL_MAP.items():
        if key in name_low:
            return portal
    # If already a valid URL and not the broken reliancejio.com
    if current_url and "reliancejio.com" not in current_url and current_url.startswith("http"):
        return current_url
    return "https://internship.aicte-india.org/internships"


def fix_urls():
    with app.app_context():
        items = Internship.query.all()
        print(f"Checking {len(items)} internships...")
        updated_count = 0

        for item in items:
            org_name = item.organisation_name or (item.organisation.name if item.organisation else "")
            correct_url = get_correct_portal(org_name, item.official_application_url)

            # Update if changed
            if item.official_application_url != correct_url or item.application_url != correct_url or not item.official_website:
                item.official_application_url = correct_url
                item.application_url = correct_url
                if not item.official_website or "reliancejio" in (item.official_website or ""):
                    item.official_website = correct_url
                updated_count += 1

        db.session.commit()
        print(f"Successfully updated {updated_count} internships with authentic portals!")

        # Also fix organisations table
        orgs = Organisation.query.all()
        org_updated = 0
        for org in orgs:
            correct_web = get_correct_portal(org.name, org.official_website)
            if org.official_website != correct_web:
                org.official_website = correct_web
                org_updated += 1
        db.session.commit()
        print(f"Successfully updated {org_updated} organisations with authentic portals!")


if __name__ == "__main__":
    fix_urls()
