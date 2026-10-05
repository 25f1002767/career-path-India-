import urllib.request
import json

BASE_URL = "http://127.0.0.1:5001"

test_endpoints = [
    ("Colleges Directory", f"{BASE_URL}/colleges/"),
    ("Search IIT", f"{BASE_URL}/colleges/?search=IIT"),
    ("Filter MP", f"{BASE_URL}/colleges/?state=Madhya+Pradesh"),
    ("Filter Gov", f"{BASE_URL}/colleges/?gov_priv=Government"),
    ("Relational Course #1", f"{BASE_URL}/colleges/?course_id=1"),
    ("College Detail #1", f"{BASE_URL}/colleges/1"),
    ("Course-First Explorer #1", f"{BASE_URL}/colleges/course/1"),
    ("Compare Matrix", f"{BASE_URL}/colleges/compare?ids=1,2,3"),
    ("Find Colleges Wizard", f"{BASE_URL}/colleges/find")
]

def run_college_tests():
    print("=== 1. TESTING COLLEGE GET ENDPOINTS ===")
    all_pass = True
    for name, url in test_endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MPathCollegeTest/1.0"})
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode("utf-8")
                status = resp.status
                size = len(content)
                print(f"[PASS] {name:<26} -> Status {status} | Size {size:,} bytes")
        except Exception as e:
            print(f"[FAIL] {name:<26} -> Error: {e}")
            all_pass = False

    print("\n=== 2. TESTING AI COLLEGE DISCOVERY API ===")
    try:
        payload = json.dumps({
            "query": "B.Sc Mathematics government college",
            "state": "Madhya Pradesh",
            "gov_priv": "Government"
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/colleges/ai-discovery",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "MPathCollegeTest/1.0"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Status: {resp.status} | Success: {data.get('success')} | Results count: {data.get('count')}")
            for item in data.get("results", [])[:3]:
                print(f" - {item['name']} ({item['location']}): {item['reasons']}")
    except Exception as e:
        print(f"[FAIL] AI Discovery API -> Error: {e}")
        all_pass = False

    print("\n=== 3. BATCH TESTING 20 COLLEGE DETAIL PAGES ===")
    try:
        detail_errors = 0
        for cid in range(1, 21):
            url = f"{BASE_URL}/colleges/{cid}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "MPathCollegeTest/1.0"})
                with urllib.request.urlopen(req) as resp:
                    if resp.status != 200:
                        print(f"[FAIL] Detail #{cid}: status {resp.status}")
                        detail_errors += 1
            except Exception as e:
                print(f"[FAIL] Detail #{cid}: {e}")
                detail_errors += 1
        if detail_errors == 0:
            print("Successfully tested 20/20 college detail pages with 0 errors!")
        else:
            all_pass = False
    except Exception as e:
        print(f"Batch test error: {e}")
        all_pass = False

    if not all_pass:
        exit(1)
    print("\nAll College Explorer verification tests PASSED successfully!")


if __name__ == "__main__":
    run_college_tests()
