import requests
import random
import string

API_URL = "http://127.0.0.1:8000"

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_scan_flow():
    # 1. Register a new user
    username = f"user_{get_random_string(5)}"
    password = "testpassword"
    email = f"{username}@example.com"
    
    print(f"Registering user: {username}")
    response = requests.post(f"{API_URL}/auth/register", json={
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Test User",
        "farm_location": "Test Farm"
    })
    if response.status_code != 200:
        print(f"Registration failed: {response.text}")
        return
    print("Registration successful")

    # 2. Login
    print("Logging in...")
    response = requests.post(f"{API_URL}/auth/token", data={
        "username": username,
        "password": password
    })
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")

    # 3. Create a scan
    print("Creating a scan...")
    scan_data = {
        "image_hash": "dummy_hash_123",
        "disease_name": "Test Disease",
        "confidence": 0.95,
        "recommendation": "Use test fungicide"
    }
    response = requests.post(f"{API_URL}/scans", json=scan_data, headers=headers)
    if response.status_code != 200:
        print(f"Create scan failed: {response.text}")
        return
    print("Scan created successfully")

    # 4. Retrieve scans
    print("Retrieving scans...")
    response = requests.get(f"{API_URL}/scans", headers=headers)
    if response.status_code != 200:
        print(f"Get scans failed: {response.text}")
        return
    scans = response.json()
    print(f"Retrieved {len(scans)} scans")
    
    if len(scans) > 0:
        scan = scans[0]
        if scan["disease_name"] == "Test Disease" and scan["confidence"] == 0.95:
            print("Verification SUCCESS: Scan data matches.")
        else:
            print("Verification FAILED: Scan data mismatch.")
    else:
        print("Verification FAILED: No scans found.")

if __name__ == "__main__":
    try:
        test_scan_flow()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend. Make sure it is running.")
