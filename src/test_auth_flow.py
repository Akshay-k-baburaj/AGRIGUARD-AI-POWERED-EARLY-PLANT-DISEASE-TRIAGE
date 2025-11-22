import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_auth_flow():
    # 1. Register
    print("Testing Registration...")
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test Farmer",
        "farm_location": "Test Farm"
    }
    # distinct username/email for re-runs if DB persists
    timestamp = int(time.time())
    register_data["email"] = f"test{timestamp}@example.com"
    register_data["username"] = f"testuser{timestamp}"

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ Registration Successful")
        else:
            print(f"❌ Registration Failed: {response.text}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is it running?")
        sys.exit(1)

    # 2. Login
    print("Testing Login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login Successful, Token received")
    else:
        print(f"❌ Login Failed: {response.text}")
        sys.exit(1)

    # 3. Get Profile
    print("Testing Get Profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data["username"] == register_data["username"]:
            print("✅ Profile Retrieval Successful")
        else:
            print("❌ Profile Mismatch")
            sys.exit(1)
    else:
        print(f"❌ Profile Retrieval Failed: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # Wait a bit for server to start if running in CI/CD style
    time.sleep(2) 
    test_auth_flow()
