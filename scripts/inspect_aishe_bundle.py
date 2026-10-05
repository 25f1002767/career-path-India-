import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://dashboard.aishe.gov.in/hedirectory/main.6a3f3221b4aecf63.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

print(f"Total bundle length: {len(content):,} chars")

# Search for HttpClient calls, URLs, and environments
matches = re.findall(r'(?:get|post|put|delete)\s*\(\s*[`\'"]([^`\'"]+)[`\'"]', content, re.IGNORECASE)
print("\nDirect HTTP call strings (first 30):")
for m in set(matches[:40]):
    print("  ->", m)

# Search for variables like apiUrl, baseUrl, endpoint, domain, service
api_vars = re.findall(r'([a-zA-Z0-9_]*(?:api|url|endpoint|service|host|domain)[a-zA-Z0-9_]*\s*[:=]\s*[`\'"][^`\'"]+[`\'"])', content, re.IGNORECASE)
print("\nAPI variables / config found:")
for v in set(api_vars[:30]):
    print("  *", v)

# Search for strings containing aishe or nic.in or gov.in
gov_urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', content)
filtered_gov = [u for u in gov_urls if "gov.in" in u or "nic.in" in u or "aishe" in u]
print("\nGov/AISHE URLs in main bundle:")
for g in set(filtered_gov):
    print("  ==>", g)

# Look for component route definitions
routes = re.findall(r'path:\s*[\'"]([^\'"]+)[\'"]', content)
print("\nAngular Routes found in main bundle:")
for r in set(routes[:20]):
    print("  #", r)
