import os
import sys
import ssl
import time
import json
import base64
import urllib.request
from datetime import datetime

# Crypto for AISHE API parameter encryption
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA1

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "careerpathindia.db")

PASSPHRASE = b"0123456789123456"
BASE_URL = "https://pdf.aishe.nic.in/aisheinstitutemanagement"
MASTER_URL = "https://pdf.aishe.nic.in/aishemasterservice"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://dashboard.aishe.gov.in",
    "Referer": "https://dashboard.aishe.gov.in/"
}


# =========================================================================
# 1. AISHE PROTOCOL CRYPTO HELPERS
# =========================================================================

def encrypt_param(value_str):
    """Encrypt query parameter according to AISHE Angular frontend specification."""
    if not value_str:
        return ""
    iv = os.urandom(16)
    salt = os.urandom(32)
    key = PBKDF2(PASSPHRASE, salt, dkLen=16, count=1000, hmac_hash_module=SHA1)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(str(value_str).encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded)
    ct_b64 = base64.b64encode(encrypted).decode("utf-8")
    combined = f"{iv.hex()}::{salt.hex()}::{ct_b64}"
    return base64.b64encode(combined.encode("utf-8")).decode("utf-8")


def decrypt_response(enc_b64):
    """Decrypt encrypted response payload if returned by AISHE."""
    if not enc_b64:
        return enc_b64
    try:
        combined = base64.b64decode(enc_b64).decode("utf-8")
        parts = combined.split("::")
        if len(parts) != 3:
            return enc_b64
        iv = bytes.fromhex(parts[0])
        salt = bytes.fromhex(parts[1])
        ct = base64.b64decode(parts[2])
        key = PBKDF2(PASSPHRASE, salt, dkLen=16, count=1000, hmac_hash_module=SHA1)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8")
    except Exception:
        return enc_b64


def safe_request(url, max_retries=3, backoff_sec=1.5):
    """Perform robust HTTP request with exponential backoff for NIC servers."""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
                data = resp.read().decode("utf-8", errors="ignore")
                return json.loads(data)
        except Exception as e:
            if attempt == max_retries:
                print(f"Request failed after {max_retries} attempts: {url} -> {e}")
                return None
            time.sleep(backoff_sec * attempt)


# =========================================================================
# 2. NORMALIZATION & DATA QUALITY HELPERS
# =========================================================================

def clean_url(url_raw):
    """Normalize and validate website URL without hallucinations."""
    if not url_raw or not isinstance(url_raw, str):
        return None
    url = url_raw.strip()
    if url.lower() in ["", "na", "null", "none", "-", "not available", "nil", "under construction"]:
        return None
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return url


def normalize_management(mgmt_raw, name_raw=""):
    """Classify management and governance (Government vs Private)."""
    mgmt = (mgmt_raw or "").strip().lower()
    name = (name_raw or "").strip().lower()

    if any(k in mgmt for k in ["central government", "state government", "local body", "government"]) or \
       any(k in name for k in ["govt", "government", "indian institute of technology", "national institute of technology", "all india institute"]):
        gov_priv = "Government"
    elif "aided" in mgmt and "un-aided" not in mgmt:
        gov_priv = "Aided"
    elif "private" in mgmt or "un-aided" in mgmt:
        gov_priv = "Private"
    else:
        gov_priv = "Government"

    clean_mgmt = mgmt_raw.strip() if mgmt_raw else ("Central/State Government" if gov_priv == "Government" else "Private")
    return gov_priv, clean_mgmt


def parse_year(year_raw):
    """Parse integer establishment year safely."""
    if not year_raw:
        return None
    try:
        yr = int(str(year_raw).strip()[:4])
        if 1700 <= yr <= 2026:
            return yr
    except Exception:
        pass
    return None


# =========================================================================
# 3. AISHE IMPORTER ENGINE
# =========================================================================

class AisheImporter:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.stats = {
            "total_fetched": 0,
            "total_new": 0,
            "total_updated": 0,
            "total_duplicates": 0,
            "total_invalid": 0,
            "total_needs_review": 0,
            "total_failed": 0
        }
        self.logs = []

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry)
        self.logs.append(entry)

    def fetch_pm_vidyalaxmi(self):
        """Fetch 1,441 top quality institutions under MoE PM Vidyalaxmi scheme."""
        url = f"{BASE_URL}/institutionDirectory%20/pm-vidya-laxmi"
        self.log("Fetching PM Vidyalaxmi verified institution registry...")
        data = safe_request(url)
        if data and "pmVidyaLaxmiInstitutes" in data:
            records = data["pmVidyaLaxmiInstitutes"]
            self.log(f"Fetched {len(records)} PM Vidyalaxmi institutions.")
            return records
        return []

    def fetch_rnd_institutes(self):
        """Fetch national R&D institutions (ISRO, DRDO, CSIR, ICAR)."""
        url = f"{BASE_URL}/institutionDirectory%20/rnd-institute"
        self.log("Fetching national R&D institution registry...")
        data = safe_request(url)
        if data and "rnDInstitutions" in data:
            records = data["rnDInstitutions"]
            self.log(f"Fetched {len(records)} national R&D institutions.")
            return records
        return []

    def fetch_universities_by_state(self, state_code):
        """Fetch all recognized universities in a specific state."""
        st_enc = encrypt_param(str(state_code))
        yr_enc = encrypt_param("2020")
        url = f"{BASE_URL}/institutionDirectory%20/getUniversityList?stateCode={urllib.parse.quote(st_enc)}&surveyYear={urllib.parse.quote(yr_enc)}"
        data = safe_request(url)
        if data and "institutionDirectoryDto" in data:
            return data["institutionDirectoryDto"]
        return []

    def fetch_colleges_by_district(self, district_code):
        """Fetch colleges in a specific district."""
        dt_enc = encrypt_param(str(district_code))
        yr_enc = encrypt_param("2020")
        url = f"{BASE_URL}/institutionDirectory%20/getCollegeList?districtcode={urllib.parse.quote(dt_enc)}&surveyYear={urllib.parse.quote(yr_enc)}"
        data = safe_request(url)
        if data and "institutionDirectoryDto" in data:
            return data["institutionDirectoryDto"]
        return []

    def fetch_standalone_by_district(self, district_code):
        """Fetch standalone institutions (Polytechnics, Teacher Training) in a district."""
        dt_enc = encrypt_param(str(district_code))
        yr_enc = encrypt_param("2020")
        url = f"{BASE_URL}/institutionDirectory%20/getStandaloneList?districtcode={urllib.parse.quote(dt_enc)}&surveyYear={urllib.parse.quote(yr_enc)}"
        data = safe_request(url)
        if data and "institutionDirectoryDto" in data:
            return data["institutionDirectoryDto"]
        return []

    def process_and_save_records(self, raw_records, category_hint="Institution", source_url=None):
        """Process, normalize, deduplicate, and upsert records into SQLite."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        source_url_final = source_url or "https://dashboard.aishe.gov.in/hedirectory/#/hedirectory"

        for raw in raw_records:
            self.stats["total_fetched"] += 1

            # Extract fields handling different AISHE schema naming variants
            aishe_code = (raw.get("aisheCode") or raw.get("aishe_code") or "").strip()
            name = (raw.get("instituteName") or raw.get("name") or "").strip()

            if not name:
                self.stats["total_invalid"] += 1
                continue

            state = (raw.get("stateName") or raw.get("state") or "").strip()
            district = (raw.get("districtName") or raw.get("district") or "").strip()
            city = (raw.get("city") or district or state or "India").strip()
            address = (raw.get("address1") or raw.get("addressLine1") or raw.get("address") or "").strip()

            raw_mgmt = raw.get("managementType") or raw.get("manegement") or raw.get("management")
            gov_priv, mgmt_type = normalize_management(raw_mgmt, name)

            est_year = parse_year(raw.get("yearOfEstablishment") or raw.get("establishedYear"))
            website = clean_url(raw.get("website") or raw.get("webSite"))

            inst_type = (raw.get("institutionType") or raw.get("type") or category_hint).strip()
            univ_name = (raw.get("universityName") or raw.get("affiliatedUniversity") or "").strip()
            univ_id = (raw.get("universityId") or "").strip()

            category = "University" if "university" in inst_type.lower() or "university" in name.lower() else \
                       "Institute" if "institute" in inst_type.lower() or "institute" in name.lower() else \
                       "Standalone" if "standalone" in inst_type.lower() or "polytechnic" in inst_type.lower() else "College"

            # ---------------------------------------------------------
            # Duplicate Detection Strategy:
            # 1. By AISHE Code (Strongest primary identifier)
            # 2. By Normalized Name + State (Fallback)
            # ---------------------------------------------------------
            existing = None
            if aishe_code:
                cursor.execute("SELECT id, name, official_website FROM colleges WHERE aishe_code = ?", (aishe_code,))
                existing = cursor.fetchone()

            if not existing:
                cursor.execute("SELECT id, name, official_website FROM colleges WHERE LOWER(name) = ? AND LOWER(state) = ?", (name.lower(), state.lower()))
                existing = cursor.fetchone()

            if existing:
                # Record exists -> Enrich / Upsert
                existing_id = existing[0]
                cursor.execute("""
                    UPDATE colleges SET
                        aishe_code = COALESCE(aishe_code, ?),
                        district = COALESCE(NULLIF(?, ''), district),
                        address = COALESCE(NULLIF(?, ''), address),
                        management_type = ?,
                        government_private = ?,
                        institution_type = COALESCE(NULLIF(?, ''), institution_type),
                        institution_category = COALESCE(NULLIF(?, ''), institution_category),
                        established_year = COALESCE(NULLIF(?, ''), established_year),
                        official_website = COALESCE(NULLIF(?, ''), official_website),
                        affiliated_university = COALESCE(NULLIF(?, ''), affiliated_university),
                        source = 'Ministry of Education - AISHE Directory',
                        source_url = ?,
                        verification_status = 'VERIFIED',
                        last_verified_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    aishe_code or None, district, address, mgmt_type, gov_priv,
                    inst_type, category, est_year, website, univ_name,
                    source_url_final, existing_id
                ))
                self.stats["total_updated"] += 1
                self.stats["total_duplicates"] += 1
            else:
                # Brand new verified record
                cursor.execute("""
                    INSERT INTO colleges (
                        aishe_code, name, state, district, city, address,
                        institution_type, institution_category, government_private,
                        management_type, established_year, official_website,
                        affiliated_university, description, source, source_url,
                        verification_status, last_verified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Ministry of Education - AISHE Directory', ?, 'VERIFIED', CURRENT_TIMESTAMP)
                """, (
                    aishe_code or None, name, state, district, city, address,
                    inst_type, category, gov_priv, mgmt_type, est_year, website,
                    univ_name, f"Recognized higher education institution listed under Ministry of Education AISHE ({aishe_code}).",
                    source_url_final
                ))
                self.stats["total_new"] += 1

        conn.commit()
        conn.close()

    def run_import(self, include_pm_vidyalaxmi=True, include_rnd=True, states_to_import=None, sample_districts=None):
        """Execute structured, polite, verified data import."""
        self.log("=== INITIATING AUTHORITATIVE AISHE DIRECTORY IMPORTER ===")

        # 1. PM Vidyalaxmi Institutions (Nationwide quality dataset of 1,441 institutions)
        if include_pm_vidyalaxmi:
            records = self.fetch_pm_vidyalaxmi()
            if records:
                self.log(f"Processing and saving {len(records)} PM Vidyalaxmi institutions...")
                self.process_and_save_records(records, category_hint="Premier Institution", source_url="https://dashboard.aishe.gov.in/hedirectory/#/hedirectory")
            time.sleep(1.0)

        # 2. National R&D Institutions
        if include_rnd:
            rnd_records = self.fetch_rnd_institutes()
            if rnd_records:
                self.log(f"Processing and saving {len(rnd_records)} national R&D institutions...")
                self.process_and_save_records(rnd_records, category_hint="R&D Institute", source_url="https://dashboard.aishe.gov.in/hedirectory/#/hedirectory")
            time.sleep(1.0)

        # 3. State Universities
        if states_to_import:
            for st_code, st_name in states_to_import:
                self.log(f"Fetching recognized universities in {st_name} (Code: {st_code})...")
                univs = self.fetch_universities_by_state(st_code)
                if univs:
                    self.log(f"Found {len(univs)} universities in {st_name}.")
                    self.process_and_save_records(univs, category_hint="State/Central University")
                time.sleep(1.0)

        # 4. Colleges in Sample Districts
        if sample_districts:
            for dt_code, dt_name in sample_districts:
                self.log(f"Fetching colleges in {dt_name} (District Code: {dt_code})...")
                colleges = self.fetch_colleges_by_district(dt_code)
                if colleges:
                    self.log(f"Found {len(colleges)} colleges in {dt_name}.")
                    self.process_and_save_records(colleges, category_hint="Affiliated College")
                time.sleep(1.0)

        self.log("=== IMPORT SESSION COMPLETED ===")
        self.log(f"Statistics: {json.dumps(self.stats, indent=2)}")
        return self.stats


if __name__ == "__main__":
    # Test execution with PM Vidyalaxmi + R&D + MP State Universities + Guna District
    importer = AisheImporter()
    
    # Madhya Pradesh is state code 23; Guna district code is 418
    states = [(23, "Madhya Pradesh")]
    districts = [(418, "Guna")]

    stats = importer.run_import(
        include_pm_vidyalaxmi=True,
        include_rnd=True,
        states_to_import=states,
        sample_districts=districts
    )
    print("\nFinal Import Run Summary:")
    print(json.dumps(stats, indent=4))
