import urllib.request
import re

endpoints = [
    ("Homepage", "http://127.0.0.1:5001/"),
    ("Exam Explorer", "http://127.0.0.1:5001/exams/"),
    ("Search UPSC", "http://127.0.0.1:5001/exams/?search=UPSC"),
    ("Category Engineering", "http://127.0.0.1:5001/exams/?category=Engineering"),
    ("Exam Detail #1", "http://127.0.0.1:5001/exams/1"),
    ("Exam Calendar", "http://127.0.0.1:5001/exams/calendar"),
    ("Eligibility Matcher", "http://127.0.0.1:5001/exams/eligibility"),
]

def run_live_tests():
    print("=== LIVE ENDPOINT VERIFICATION ===")
    for name, url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MPathTestBot/1.0"})
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode("utf-8")
                status = resp.status
                size = len(content)
                print(f"[OK] {name:<22} -> Status {status} | Size {size:,} bytes")
        except Exception as e:
            print(f"[FAIL] {name:<20} -> Error: {e}")


if __name__ == "__main__":
    run_live_tests()
