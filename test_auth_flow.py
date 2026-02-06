#!/usr/bin/env python3
"""
Test script to verify the authentication flow works correctly
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
EMAIL = "testuser@example.com"
PASSWORD = "password123"
NAME = "Test User"

def test_registration():
    """Test user registration"""
    print("Testing registration...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": EMAIL,
                "password": PASSWORD,
                "name": NAME
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Registration successful: {data['email']}")
            return data
        elif response.status_code == 400 and "already exists" in response.text:
            print("✓ User already exists (expected)")
            # Try to login instead
            return test_login()
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return None

def test_login():
    """Test user login"""
    print("Testing login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": EMAIL,
                "password": PASSWORD
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Login successful: {data['email']}")
            print(f"  Token: {data['token'][:50]}..." if 'token' in data else "  No token returned")
            return data
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_protected_route(token):
    """Test accessing a protected route"""
    print("Testing protected route access...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Protected route access successful: {data}")
            return True
        else:
            print(f"✗ Protected route failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Protected route error: {e}")
        return False

def main():
    print("Starting authentication flow test...\n")

    # Test registration
    reg_result = test_registration()
    if not reg_result:
        print("\nFailed to register or login user")
        sys.exit(1)

    # Extract token if available in registration result
    token = reg_result.get('token')
    if not token:
        # Try login if registration didn't return a token
        login_result = test_login()
        if not login_result:
            print("\nFailed to login user")
            sys.exit(1)
        token = login_result.get('token')

    if not token:
        print("\nNo token obtained from auth flow")
        sys.exit(1)

    # Test protected route access
    success = test_protected_route(token)

    if success:
        print("\n✓ All authentication tests passed!")
        print(f"  - User: {reg_result.get('email', 'Unknown')}")
        print(f"  - Token length: {len(token)} characters")
    else:
        print("\n✗ Authentication tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()