import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.scholarship import Scholarship, ScholarshipCycle

NSP_OFFICIAL_APP_URL = "https://scholarships.gov.in/ApplicationForm/"
NSP_OTR_REG_URL = "https://scholarships.gov.in/otrapplication/#/login-page"
MP_ACTIVE_APP_URL = "https://www.mptechedu.org/scholarship"

with app.app_context():
    # 1. Update all NSP scholarships using outdated newstdRegfrmInstruction
    nsp_schs = Scholarship.query.filter(
        Scholarship.official_application_url.contains("newstdRegfrmInstruction")
    ).all()
    
    print(f"Updating {len(nsp_schs)} NSP scholarships to active portal {NSP_OFFICIAL_APP_URL}...")
    for s in nsp_schs:
        s.official_application_url = NSP_OFFICIAL_APP_URL
        s.application_url_status = "VALID"
        s.final_application_url = NSP_OFFICIAL_APP_URL
        if s.active_cycle:
            s.active_cycle.official_application_url = NSP_OFFICIAL_APP_URL
            s.active_cycle.application_url_status = "VALID"

    # 2. Update MP scholarships with unreachable nic.in subdomains
    mp_schs = Scholarship.query.filter(
        Scholarship.official_application_url.contains("scholarshipportal.mp.nic.in")
    ).all()
    print(f"Updating {len(mp_schs)} MP scholarships to active portal {MP_ACTIVE_APP_URL}...")
    for s in mp_schs:
        s.official_application_url = MP_ACTIVE_APP_URL
        s.application_url_status = "VALID"
        s.final_application_url = MP_ACTIVE_APP_URL
        if s.active_cycle:
            s.active_cycle.official_application_url = MP_ACTIVE_APP_URL
            s.active_cycle.application_url_status = "VALID"

    db.session.commit()
    print("[OK] Successfully migrated all outdated application links to active 2026-27 portals!")
