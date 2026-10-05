import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://dashboard.aishe.gov.in/hedirectory/main.6a3f3221b4aecf63.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Find dynamic import statements like import("./...") or lazy chunk names
imports = re.findall(r'import\([\'"]([^\'"]+)[\'"]\)', content)
print("Dynamic imports found:", imports)

# Find any .js files referenced
js_files = re.findall(r'[\'"]([a-zA-Z0-9_\-\.]+\.[a-f0-9]{16}\.js)[\'"]', content)
print("Lazy JS chunks found:", set(js_files))

# Find occurrences of 'hedirectory'
pos = 0
found = []
while True:
    pos = content.find("hedirectory", pos)
    if pos == -1: break
    snippet = content[max(0, pos-80):min(len(content), pos+150)]
    found.append(snippet)
    pos += 11
    if len(found) > 8: break

print("\nSnippets with hedirectory:")
for s in found:
    print("---")
    print(s)
