import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "https://scholarships.gov.in/Students",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
)

try:
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        html = r.read().decode("utf-8", errors="ignore")
        print("Page fetched successfully. Length:", len(html))
        
        # Look for buttons, anchors, onclicks
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE)
        print(f"Total links found: {len(anchors)}")
        for href, text in anchors:
            clean_text = re.sub(r'<[^>]+>', '', text).strip()
            print(f"  LINK: {href} | TEXT: {clean_text}")

except Exception as e:
    print("Error:", e)
