import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for fname in ["main.6a3f3221b4aecf63.js", "337.52e2d3e8e3776afe.js"]:
    url = "https://dashboard.aishe.gov.in/hedirectory/" + fname
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    # Search for variable assignments ending in baseUrl or masterUrl
    base_matches = re.findall(r'(\b\w*baseUrl\w*\s*=\s*["\'][^"\']+["\'])', content)
    print(f"baseUrl in {fname}:", base_matches)

    master_matches = re.findall(r'(\b\w*masterUrl\w*\s*=\s*["\'][^"\']+["\'])', content)
    print(f"masterUrl in {fname}:", master_matches)

    # Search around "https://pdf.aishe.nic.in"
    pos = content.find("pdf.aishe.nic.in")
    if pos != -1:
        print("Around pdf.aishe.nic.in:", content[max(0, pos-150):min(len(content), pos+250)])
