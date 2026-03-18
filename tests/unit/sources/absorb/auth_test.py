"""
Auth verification test for Absorb connector.
Run this script to verify your credentials are correctly configured.

Usage:
    python tests/unit/sources/absorb/auth_test.py
"""
import sys
import os
import json
from pathlib import Path

import requests


PORTAL_URL_MAP = {
    "US": "https://rest.myabsorb.com",
    "CA": "https://rest.myabsorb.ca",
    "EU": "https://rest.myabsorb.eu",
    "AU": "https://rest.myabsorb.com.au",
}


def load_config():
    """Load configuration from dev_config.json."""
    config_path = Path(__file__).parent / "configs" / "dev_config.json"
    with open(config_path, "r") as f:
        return json.load(f)


def test_auth():
    """Verify that credentials in dev_config.json are valid by making a simple API call."""
    config = load_config()

    private_api_key = config.get("private_api_key")
    username = config.get("username")
    password = config.get("password")
    portal_url = config.get("portal_url", "US").upper()

    if not private_api_key or not username or not password:
        print("Missing required credentials in dev_config.json")
        print("Required: private_api_key, username, password, portal_url")
        return False

    base_url = PORTAL_URL_MAP.get(portal_url, PORTAL_URL_MAP["US"])

    # Step 1: Authenticate to get token
    auth_response = requests.post(
        f"{base_url}/authenticate",
        headers={
            "x-api-key": private_api_key,
            "x-api-version": "2",
            "Content-Type": "application/json"
        },
        json={
            "username": username,
            "password": password,
            "privateKey": private_api_key
        },
        timeout=30,
        verify=False  # Skip SSL verification for testing
    )

    if auth_response.status_code == 400:
        print("Authentication failed: Missing required parameters (HTTP 400)")
        print("   Check your credentials in tests/unit/sources/absorb/configs/dev_config.json")
        return False
    elif auth_response.status_code == 403:
        print("Authentication failed: Portal disabled (HTTP 403)")
        return False
    elif auth_response.status_code != 200:
        print(f"Authentication failed: HTTP {auth_response.status_code}")
        print(f"   Body: {auth_response.text}")
        return False

    token = auth_response.text.strip('"')

    # Step 2: Verify token works by calling a simple endpoint
    verify_response = requests.get(
        f"{base_url}/users",
        headers={
            "x-api-key": private_api_key,
            "x-api-version": "2",
            "Authorization": f"Bearer {token}"
        },
        params={"_limit": "1"},
        timeout=30,
        verify=False  # Skip SSL verification for testing
    )

    if verify_response.status_code == 200:
        print(f"Authentication successful! Connected to Absorb LMS ({portal_url}).")
        data = verify_response.json()
        print(f"   Total users: {data.get('totalItems', 'N/A')}")
        return True
    elif verify_response.status_code == 401:
        print("Authentication failed: Invalid token (HTTP 401)")
        return False
    elif verify_response.status_code == 403:
        print("Authorization failed: Insufficient permissions (HTTP 403)")
        return False
    else:
        print(f"Unexpected response: HTTP {verify_response.status_code}")
        print(f"   Body: {verify_response.text}")
        return False


if __name__ == "__main__":
    success = test_auth()
    sys.exit(0 if success else 1)
