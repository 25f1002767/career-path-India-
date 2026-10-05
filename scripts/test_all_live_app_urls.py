import os
import sys
import urllib.request
import ssl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models.scholarship import Scholarship

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with app.app_context():
    schs = Scholarship.query.all()
    print(f"Auditing {len(schs)} scholarships live...", flush=True)
    checked_urls = set()
    
    for s in schs:
        url = s.resolved_application_url
        if not url or url in checked_urls:
            continue
        checked_urls.add(url)
            
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=4, context=ctx) as r:
                code = r.getcode()
                body_sample = r.read(1024).decode("utf-8", errors="ignore")
                is_404_body = "Page Not Found" in body_sample
                status = "404_PAGE_NOT_FOUND" if is_404_body else "OK"
                print(f"[{status}] (HTTP {code}) {url} -> {r.geturl()}", flush=True)
        except urllib.error.HTTPError as e:
            body = e.read(1024).decode("utf-8", errors="ignore")
            is_404_body = "Page Not Found" in body
            status = "404_PAGE_NOT_FOUND" if is_404_body else f"HTTP_{e.code}"
            print(f"[{status}] (HTTP {e.code}) {url}", flush=True)
        except Exception as e:
            print(f"[ERR: {str(e)[:40]}] {url}", flush=True)
