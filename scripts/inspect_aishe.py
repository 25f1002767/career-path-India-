import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://dashboard.aishe.gov.in/hedirectory/"

req = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', html)
print("Found scripts in HTML:")
for s in scripts:
    print(" -", s)

# Let's inspect main JS bundles
for s in scripts:
    if "main" in s or "bundle" in s or "vendor" in s or "runtime" in s:
        script_url = BASE_URL + s if not s.startswith("http") else s
        print(f"\nFetching {script_url} ...")
        try:
            s_req = urllib.request.Request(
                script_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(s_req, context=ctx, timeout=20) as s_resp:
                s_content = s_resp.read().decode("utf-8", errors="ignore")
                print(f"Loaded {s}, size: {len(s_content):,} chars")

                # Find any API endpoints or URLs
                endpoints = re.findall(r'https?://[^\s\'"<>]+', s_content)
                aishe_urls = [u for u in endpoints if "aishe" in u.lower() or "hedirectory" in u.lower() or "api" in u.lower()]
                print("Matching URLs/Endpoints in bundle:")
                for u in set(aishe_urls):
                    print("   *", u)

                # Look for REST path strings like /api/, /directory/, /get, etc.
                api_paths = re.findall(r'[\'"](/[a-zA-Z0-9_\-\./]*?(?:institution|college|university|directory|state|district|search|download)[a-zA-Z0-9_\-\./]*)[\'"]', s_content)
                if api_paths:
                    print("Sample relative paths:")
                    for p in set(api_paths[:25]):
                        print("   ->", p)

        except Exception as e:
            print("Error fetching script:", e)
