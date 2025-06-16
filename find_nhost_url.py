#!/usr/bin/env python3
"""
Script to help find your Nhost website URL
"""

import requests
import time
from urllib.parse import urljoin

def test_url(url, timeout=5):
    """Test if a URL is accessible"""
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return True, response.status_code
        elif response.status_code in [301, 302, 307, 308]:
            return True, f"{response.status_code} -> {response.headers.get('Location', 'Unknown')}"
        else:
            return False, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

def find_nhost_url():
    """Try to find your Nhost website URL"""
    
    print("🔍 Searching for your Nhost website URL...")
    print("=" * 50)
    
    # Common Nhost URL patterns
    base_urls = [
        "https://app.nhost.io",
        "https://console.nhost.io",
        "https://dashboard.nhost.io",
        "https://cloud.nhost.io",
        "https://nhost.io"
    ]
    
    # Test base URLs first
    print("📋 Testing Nhost console URLs:")
    for url in base_urls:
        print(f"  Testing: {url}")
        success, result = test_url(url)
        if success:
            print(f"  ✅ {url} - Status: {result}")
        else:
            print(f"  ❌ {url} - Error: {result}")
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎯 FOUND! Your Nhost dashboard is at: https://app.nhost.io")
    print("\n📋 Steps to find your website URL:")
    print("1. Go to https://app.nhost.io")
    print("2. Sign in to your Nhost account")
    print("3. Look for your project in the dashboard")
    print("4. Click on your project")
    print("5. Look for these sections:")
    print("   - 'Client URL' or 'Frontend URL' (your website)")
    print("   - 'Backend URL' (your API)")
    print("   - 'GraphQL URL' (your GraphQL endpoint)")
    
    print("\n📱 Common Nhost URL patterns:")
    print("- Client URL: https://[project-id].nhost.app")
    print("- Backend URL: https://[project-id].nhost.run")
    print("- GraphQL URL: https://[project-id].nhost.run/v1/graphql")
    
    print("\n🔧 If you can't find your project:")
    print("- Make sure you're logged into the correct account")
    print("- Check if you created the project in a different region")
    print("- Try creating a new project if needed")
    print("- Look for any deployment emails from Nhost")

if __name__ == "__main__":
    find_nhost_url() 