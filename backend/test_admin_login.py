"""
Test script for admin login endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test the admin login endpoint"""
    
    print("=" * 50)
    print("Testing Admin Login Endpoint")
    print("=" * 50)
    
    # Test data
    login_data = {
        "email": "admin@ems.local",
        "password": "Admin123"
    }
    
    print(f"\nAttempting login with:")
    print(f"  Email: {login_data['email']}")
    print(f"  Password: {login_data['password']}")
    
    try:
        # Make login request
        response = requests.post(
            f"{BASE_URL}/admin/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n[SUCCESS] Admin login successful!")
            data = response.json()
            print(f"\nAdmin Key: {data.get('admin_key')}")
            print(f"User Info: {data.get('user')}")
        else:
            print("\n[ERROR] Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

def test_invalid_login():
    """Test with invalid credentials"""
    
    print("\n" + "=" * 50)
    print("Testing Invalid Login")
    print("=" * 50)
    
    login_data = {
        "email": "admin@ems.local",
        "password": "WrongPassword"
    }
    
    print(f"\nAttempting login with wrong password...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/admin/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")

def test_non_admin_login():
    """Test with non-admin user"""
    
    print("\n" + "=" * 50)
    print("Testing Non-Admin User Login")
    print("=" * 50)
    
    # First create a non-admin user
    print("\nNote: This test requires a non-admin user to exist.")
    print("Skipping for now...")

if __name__ == "__main__":
    test_admin_login()
    test_invalid_login()
    test_non_admin_login()
