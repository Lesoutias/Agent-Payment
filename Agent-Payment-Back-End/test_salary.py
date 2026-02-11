import requests
import sys

try:
    # 1. Create agent with salary
    agent_data = {"name": "Test Agent", "role": "Tester", "salary": 5000.0}
    response = requests.post("http://127.0.0.1:8000/agents/", json=agent_data)
    if response.status_code == 200:
        new_agent = response.json()
        print(f"Created Agent: {new_agent}")
        if "salary" in new_agent and new_agent["salary"] == 5000.0:
            print("SUCCESS: Salary field present in creation response.")
        else:
            print("FAILED: Salary missing or incorrect in creation response.")
            sys.exit(1)
            
        # 2. Get all agents
        response = requests.get("http://127.0.0.1:8000/agents/")
        agents = response.json()
        found = False
        for a in agents:
            if a["id"] == new_agent["id"] and "salary" in a:
                found = True
                print(f"Verified Agent in List: {a}")
                break
        
        if found:
            print("SUCCESS: Salary field present in list response.")
        else:
            print("FAILED: Salary missing in list response.")
            sys.exit(1)
            
        # Cleanup
        requests.delete(f"http://127.0.0.1:8000/agents/{new_agent['id']}")
        print("Cleanup: Deleted test agent.")

    else:
        print(f"FAILED to create agent: {response.status_code} {response.text}")
        sys.exit(1)

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
