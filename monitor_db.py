#!/usr/bin/env python3
"""
Database Monitoring Script for Budge-IT App

This script helps monitor the database connection status and provides
information about Supabase connection issues.

Usage:
    python monitor_db.py
"""

import requests
import json
import time
from datetime import datetime

def check_app_status(base_url):
    """Check the overall app status."""
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def check_health(base_url):
    """Check the health endpoint."""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def check_database_status(base_url):
    """Check detailed database status."""
    try:
        response = requests.get(f"{base_url}/db-status", timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def check_supabase(base_url):
    """Check Supabase-specific connection."""
    try:
        response = requests.get(f"{base_url}/check-supabase", timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def reset_connection_pool(base_url):
    """Reset the connection pool to help with pool exhaustion."""
    try:
        response = requests.get(f"{base_url}/reset-pool", timeout=15)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def main():
    """Main monitoring function."""
    base_url = "https://budge-it-j4bp.onrender.com"
    
    print("🔍 Budge-IT Database Monitor")
    print("=" * 50)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 App URL: {base_url}")
    print()
    
    # Check app status
    print("1️⃣ Checking app status...")
    status_data, status_code = check_app_status(base_url)
    if status_code == 200:
        print(f"   ✅ App is running: {status_data.get('message', 'Unknown')}")
    else:
        print(f"   ❌ App status check failed: {status_data}")
    print()
    
    # Check health
    print("2️⃣ Checking health endpoint...")
    health_data, health_code = check_health(base_url)
    if health_code == 200:
        print(f"   ✅ Health: {health_data.get('status', 'Unknown')}")
        print(f"   📊 Database: {health_data.get('database', 'Unknown')}")
        print(f"   💬 Message: {health_data.get('message', 'No message')}")
    else:
        print(f"   ❌ Health check failed: {health_data}")
    print()
    
    # Check detailed database status
    print("3️⃣ Checking detailed database status...")
    db_data, db_code = check_database_status(base_url)
    if db_code == 200:
        print(f"   ✅ Database Status: {db_data.get('status', 'Unknown')}")
        if db_data.get('status') == 'connected':
            print(f"   ⚡ Response Time: {db_data.get('response_time', 'Unknown')}s")
            print(f"   🗄️ Database: {db_data.get('database_url', 'Unknown')}")
            pool_info = db_data.get('connection_pool_info', {})
            if isinstance(pool_info, dict):
                print(f"   📦 Pool Size: {pool_info.get('pool_size', 'Unknown')}")
                print(f"   🔄 Checked In: {pool_info.get('checked_in', 'Unknown')}")
                print(f"   📤 Checked Out: {pool_info.get('checked_out', 'Unknown')}")
                print(f"   🌊 Overflow: {pool_info.get('overflow', 'Unknown')}")
        else:
            print(f"   ❌ Connection Error: {db_data.get('error', 'Unknown error')}")
            print(f"   💬 Message: {db_data.get('message', 'No message')}")
            if db_data.get('suggestion'):
                print(f"   💡 Suggestion: {db_data.get('suggestion')}")
    else:
        print(f"   ❌ Database status check failed: {db_data}")
    print()
    
    # Check Supabase specifically
    print("4️⃣ Checking Supabase connection...")
    supabase_data, supabase_code = check_supabase(base_url)
    if supabase_code == 200:
        print(f"   ✅ Supabase Status: {supabase_data.get('status', 'Unknown')}")
        print(f"   💬 Message: {supabase_data.get('message', 'No message')}")
        if supabase_data.get('user_count'):
            print(f"   👥 Users Found: {supabase_data.get('user_count', 'Unknown')}")
    else:
        print(f"   ❌ Supabase check failed: {supabase_data}")
    print()
    
    # Summary and recommendations
    print("📋 Summary:")
    print("-" * 30)
    
    if status_code == 200 and health_code == 200:
        print("✅ App is running and accessible")
    else:
        print("❌ App has issues")
    
    if db_code == 200 and db_data.get('status') == 'connected':
        print("✅ Database connection is working")
    else:
        print("❌ Database connection issues detected")
        print("   💡 This is likely due to Supabase connection limits")
        print("   💡 Your data is safe in Supabase")
        print("   💡 Try again in 15-30 minutes")
        
        # Offer to reset connection pool
        print("\n🔄 Connection Pool Reset Options:")
        print("   You can try resetting the connection pool:")
        print(f"   🌐 Visit: {base_url}/reset-pool")
        print("   📝 Or run: python -c \"import requests; print(requests.get('https://budge-it-j4bp.onrender.com/reset-pool').json())\"")
    
    if supabase_code == 200 and supabase_data.get('status') == 'connected':
        print("✅ Supabase connection is working")
    else:
        print("❌ Supabase connection issues")
        print("   💡 This is normal during high traffic periods")
    
    print()
    print("🔗 Useful URLs:")
    print(f"   App: {base_url}")
    print(f"   Health: {base_url}/health")
    print(f"   DB Status: {base_url}/db-status")
    print(f"   Supabase Check: {base_url}/check-supabase")
    print(f"   Reset Pool: {base_url}/reset-pool")
    
    print()
    print("📚 SQLAlchemy Connection Pool Info:")
    print("   Based on the SQLAlchemy documentation, your app is experiencing")
    print("   'QueuePool limit reached' errors, which means the connection pool")
    print("   is exhausted. The ultra-conservative settings should help prevent this.")
    print("   If issues persist, consider upgrading your Supabase plan.")

if __name__ == "__main__":
    main() 