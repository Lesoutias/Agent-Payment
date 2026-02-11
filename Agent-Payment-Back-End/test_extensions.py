import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/reports/dashboard")
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS: Dashboard endpoint is working!")
        print(f"Data received: {data}")
        # Validate structure
        required_keys = ["total_agents", "monthly_payments", "pending_count", "recent_payments"]
        if all(key in data for key in required_keys):
            print("Validation Passed: All keys present.")
        else:
            print(f"Validation Failed: Missing keys. Found: {list(data.keys())}")
            sys.exit(1)
    else:
        print(f"FAILED: Status Code {response.status_code}")
        print(response.text)
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
