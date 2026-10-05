import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://dashboard.aishe.gov.in",
    "Referer": "https://dashboard.aishe.gov.in/"
}

def test_endpoint(name, url, method="GET", body=None):
    print(f"\n--- Testing: {name} ---")
    print(f"URL: {url}")
    try:
        data = json.dumps(body).encode("utf-8") if body else None
        headers = dict(HEADERS)
        if body:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            print(f"Status: {resp.status} | Content Length: {len(content):,} chars")
            try:
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    print(f"Parsed JSON List with {len(parsed)} items. Sample item 0:")
                    print(json.dumps(parsed[0], indent=2)[:500])
                elif isinstance(parsed, dict):
                    print(f"Parsed JSON Dict with keys: {list(parsed.keys())}")
                    # Print sample values
                    sample = {k: parsed[k] for k in list(parsed.keys())[:5]}
                    print(json.dumps(sample, indent=2)[:500])
            except Exception as e:
                print("Raw content preview:", content[:300])
            return True, content
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

if __name__ == "__main__":
    # 1. Survey Years
    test_endpoint("Get Survey Years", "https://pdf.aishe.nic.in/aisheinstitutemanagement/apis/getSurveyYear")

    # 2. States Master
    test_endpoint("States Master", "https://pdf.aishe.nic.in/aishemasterservice/api/state")

    # 3. PM Vidya Laxmi Institutions
    test_endpoint("PM Vidya Laxmi List", "https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/pm-vidya-laxmi")

    # 4. R&D Institutes
    test_endpoint("R&D Institutes", "https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/rnd-institute")
