import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def test_api():
    print("1. Testing Login...")
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_payload)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"   SUCCESS: Login successful. Token obtained.")
        else:
            print(f"   FAILED: Login failed with status {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"   FAILED: Could not connect to {login_url}. Error: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("\n2. Testing Get Areas...")
    areas_url = f"{BASE_URL}/areas"
    response = requests.get(areas_url, headers=headers)
    if response.status_code == 200:
        print(f"   SUCCESS: Retrieved areas.")
        print(f"   Data: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   FAILED: Get Areas failed with status {response.status_code}")
        print(response.text)

    print("\n3. Testing Create Area...")
    create_area_payload = {
        "name": "Test Area 1",
        "description": "This is a test area",
        "link": "http://example.com",
        "is_active": True
    }
    response = requests.post(areas_url, json=create_area_payload, headers=headers)
    if response.status_code == 201:
        print(f"   SUCCESS: Created area.")
        area_data = response.json().get('data')
        area_id = area_data.get('id')
        print(f"   Area ID: {area_id}")
    elif response.status_code == 409:
        print("   INFO: Area already exists.")
        # Try to find it to get ID
        response = requests.get(areas_url, headers=headers)
        areas = response.json().get('data', [])
        for area in areas:
            if area['name'] == "Test Area 1":
                area_id = area['id']
                break
    else:
        print(f"   FAILED: Create Area failed with status {response.status_code}")
        print(response.text)
        return

    if 'area_id' in locals():
        print(f"\n4. Testing Update Area {area_id}...")
        update_payload = {
            "description": "Updated description"
        }
        response = requests.put(f"{areas_url}/{area_id}", json=update_payload, headers=headers)
        if response.status_code == 200:
            print(f"   SUCCESS: Updated area.")
        else:
            print(f"   FAILED: Update Area failed with status {response.status_code}")
            print(response.text)

        print(f"\n5. Testing Delete Area {area_id}...")
        response = requests.delete(f"{areas_url}/{area_id}", headers=headers)
        if response.status_code == 200:
            print(f"   SUCCESS: Deleted area.")
        else:
            print(f"   FAILED: Delete Area failed with status {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_api()
