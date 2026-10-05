import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://dashboard.aishe.gov.in/hedirectory/337.52e2d3e8e3776afe.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

print(f"Chunk 337 size: {len(content):,} chars")

# Search for URLs or endpoints
endpoints = re.findall(r'[\'"`](https?://[^\'"`]+)[\'"`]', content)
print("Full URLs found:")
for u in set(endpoints):
    print("  *", u)

# Search for service methods or REST endpoints
paths = re.findall(r'[\'"`](/[a-zA-Z0-9_\-\./]+)[\'"`]', content)
service_paths = [p for p in paths if any(k in p.lower() for k in ["api", "hedirectory", "institution", "college", "university", "state", "district", "get", "post", "search", "list"])]
print("\nCandidate service paths:")
for p in set(service_paths):
    print("  ->", p)

# Search for HttpClient post/get calls
calls = re.findall(r'this\.http\.(?:post|get)\s*\(\s*([^,\)]+)', content)
print("\nthis.http calls:")
for c in set(calls):
    print("  #", c)

# Let's search for parameter names like aisheCode, stateCode, districtCode, instType, etc.
params = re.findall(r'([a-zA-Z0-9_]*(?:aishe|state|district|inst|univ|college|page|limit)[a-zA-Z0-9_]*\s*[:=])', content, re.IGNORECASE)
print("\nCandidate parameter names:")
for pr in set(params[:30]):
    print("  ~", pr)
