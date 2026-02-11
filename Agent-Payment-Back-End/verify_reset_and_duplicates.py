import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def verify_duplicate_prevention():
    print("\n--- Verifying Duplicate Prevention ---")
    
    # 1. Create an Agent
    agent_data = {"name": "Test Agent", "role": "Tester", "salary": 5000}
    try:
        response = requests.post(f"{BASE_URL}/agents/", json=agent_data)
        if response.status_code not in [200, 201]:
             print(f"Failed to create agent: {response.text}")
             return
        agent_id = response.json()["id"]
        print(f"Created Agent ID: {agent_id}")
    except Exception as e:
        print(f"Error creating agent: {e}")
        return

    # 2. Create First Payment
    payment_data = {
        "amount": 5000,
        "status": "Pending",
        "payment_date": "2025-05-15",
        "agent_id": agent_id
    }
    response = requests.post(f"{BASE_URL}/payments/", json=payment_data)
    if response.status_code == 200:
        print("Payment 1 created successfully.")
    else:
        print(f"Failed to create Payment 1: {response.text}")
        return

    # 3. Try to Create Duplicate Payment (Same Month)
    response = requests.post(f"{BASE_URL}/payments/", json=payment_data)
    if response.status_code == 400:
        print("SUCCESS: Duplicate payment blocked (400 Bad Request).")
        print(f"Message: {response.json()['detail']}")
    else:
        print(f"FAILURE: Duplicate payment NOT blocked. Status: {response.status_code}")

def verify_reset():
    print("\n--- Verifying Database Reset ---")
    try:
        response = requests.delete(f"{BASE_URL}/admin/reset-database")
        if response.status_code == 204:
            print("Reset request successful (204 No Content).")
        else:
            print(f"Reset request failed: {response.status_code} {response.text}")
            return

        # Check if agents are gone
        response = requests.get(f"{BASE_URL}/agents/")
        agents = response.json()
        if len(agents) == 0:
            print("SUCCESS: Agents table is empty.")
        else:
             print(f"FAILURE: Agents table not empty. Count: {len(agents)}")

        # Check ID Reset (Create new agent)
        agent_data = {"name": "New Start", "role": "Reset Check", "salary": 1000}
        response = requests.post(f"{BASE_URL}/agents/", json=agent_data)
        new_id = response.json()["id"]
        if new_id == 1:
             print(f"SUCCESS: Agent ID reset to 1. (New ID: {new_id})")
        else:
             print(f"FAILURE: Agent ID NOT reset. (New ID: {new_id})")

    except Exception as e:
        print(f"Error during reset verification: {e}")

if __name__ == "__main__":
    try:
        verify_duplicate_prevention()
        verify_reset()
    except ImportError:
        print("Requests library not found. Please install it with 'pip install requests'")
    except Exception as e:
        print(f"An error occurred: {e}")
