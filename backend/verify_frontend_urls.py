import requests
import sys

sys.stdout.reconfigure(line_buffering=True)

urls = [
    "http://localhost:3000",
    "http://localhost:3000/admin",
    "http://localhost:3000/admin/documents"
]

print("==========================================================================")
print("VERIFYING FRONTEND APPLICATION ROUTES")
print("==========================================================================")

all_ok = True
for url in urls:
    try:
        res = requests.get(url, timeout=10.0)
        if res.status_code == 200:
            print(f"[OK] {url} -> Status 200 (Length: {len(res.text)} bytes)")
        else:
            print(f"[FAIL] {url} -> Status {res.status_code}")
            all_ok = False
    except Exception as e:
        print(f"[FAIL] {url} -> Error: {e}")
        all_ok = False

print("==========================================================================")
if all_ok:
    print("ALL FRONTEND ROUTES VERIFIED WORKING PERFECTLY!")
else:
    print("SOME ROUTES FAILED VERIFICATION")
print("==========================================================================")
