#!/usr/bin/env python3
"""
Simple script to help find your Nhost website URL
"""

import webbrowser
import requests
import time

def main():
    print("🌐 Budge-IT Website URL Finder")
    print("=" * 40)
    
    # Common Nhost URL patterns
    possible_urls = [
        "https://budge-it.nhost.run",
        "https://budge-it-app.nhost.run", 
        "https://budgit.nhost.run",
        "https://budget-tracker.nhost.run",
        "https://final-system.nhost.run"
    ]
    
    print("🔍 Testing common Nhost URLs...")
    print()
    
    working_urls = []
    
    for url in possible_urls:
        try:
            print(f"Testing: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ FOUND! Your website is at: {url}")
                working_urls.append(url)
            else:
                print(f"❌ Not found (Status: {response.status_code})")
        except requests.exceptions.RequestException:
            print(f"❌ Not accessible")
        print()
    
    if working_urls:
        print("🎉 SUCCESS! Your website is live at:")
        for url in working_urls:
            print(f"   {url}")
        
        # Ask if user wants to open the URL
        choice = input("Do you want to open your website now? (y/n): ")
        if choice.lower() == 'y':
            webbrowser.open(working_urls[0])
    else:
        print("❌ Could not find your website automatically.")
        print()
        print("📋 Manual Steps:")
        print("1. Go to https://console.nhost.io")
        print("2. Click on your project")
        print("3. Look for 'Client URL' or 'Frontend URL'")
        print("4. Copy that URL and test it")
        
        # Open Nhost console
        choice = input("Do you want to open Nhost console? (y/n): ")
        if choice.lower() == 'y':
            webbrowser.open("https://console.nhost.io")

if __name__ == "__main__":
    main() 