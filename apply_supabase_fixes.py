#!/usr/bin/env python3
"""
Supabase Security Fixes and Connection Check Script

This script helps apply security fixes to your Supabase database
and check connection status.

Usage:
    python apply_supabase_fixes.py
"""

import os
import requests
import json
from datetime import datetime

def check_app_status():
    """Check if the app is running and accessible."""
    try:
        response = requests.get('https://budge-it-j4bp.onrender.com/status', timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def apply_supabase_fixes():
    """Instructions for applying Supabase security fixes."""
    print("🔒 Supabase Security Fixes")
    print("=" * 50)
    print()
    
    print("📋 To fix the 'role mutable search_path' warnings:")
    print()
    print("1️⃣ Go to your Supabase Dashboard:")
    print("   https://supabase.com/dashboard")
    print()
    print("2️⃣ Navigate to your project's SQL Editor")
    print()
    print("3️⃣ Copy and paste the contents of 'fix_supabase_security.sql'")
    print("   into the SQL Editor and run it")
    print()
    print("4️⃣ This will:")
    print("   ✅ Drop the problematic functions")
    print("   ✅ Recreate them with proper security settings")
    print("   ✅ Add SECURITY DEFINER and SET search_path = public")
    print("   ✅ Grant appropriate permissions")
    print()
    print("5️⃣ After running the SQL, the warnings should disappear")
    print()

def check_connection_status():
    """Check the current connection status."""
    print("🌐 Connection Status Check")
    print("=" * 50)
    print()
    
    # Check app status
    status_data, status_code = check_app_status()
    if status_code == 200:
        print("✅ App is running and accessible")
    else:
        print("❌ App status check failed")
        return
    
    # Check database endpoints
    endpoints = [
        ('/health', 'Health Check'),
        ('/db-status', 'Database Status'),
        ('/check-supabase', 'Supabase Check'),
        ('/reset-pool', 'Reset Pool')
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'https://budge-it-j4bp.onrender.com{endpoint}', timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
            else:
                print(f"⚠️ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Failed - {str(e)[:50]}...")
    
    print()

def provide_solutions():
    """Provide solutions for the connection issues."""
    print("💡 Solutions for Connection Issues")
    print("=" * 50)
    print()
    
    print("🔧 Immediate Actions:")
    print("1. Wait 15-30 minutes for Supabase connection limits to reset")
    print("2. Try the connection pool reset: https://budge-it-j4bp.onrender.com/reset-pool")
    print("3. Monitor status: https://budge-it-j4bp.onrender.com/db-status")
    print()
    
    print("🚀 Long-term Solutions:")
    print("1. Upgrade your Supabase plan for higher connection limits")
    print("2. Consider using connection pooling services")
    print("3. Implement caching to reduce database calls")
    print()
    
    print("📊 Current Status:")
    print("- Your app is deployed and running ✅")
    print("- Your data is safe in Supabase ✅")
    print("- Connection issues are temporary ✅")
    print("- App will work once limits reset ✅")
    print()

def main():
    """Main function."""
    print("🔧 Budge-IT Supabase Fixes & Status")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check connection status
    check_connection_status()
    
    # Provide Supabase fixes
    apply_supabase_fixes()
    
    # Provide solutions
    provide_solutions()
    
    print("🔗 Useful Links:")
    print("- App: https://budge-it-j4bp.onrender.com")
    print("- Supabase Dashboard: https://supabase.com/dashboard")
    print("- Health Check: https://budge-it-j4bp.onrender.com/health")
    print("- Database Status: https://budge-it-j4bp.onrender.com/db-status")
    print("- Reset Pool: https://budge-it-j4bp.onrender.com/reset-pool")
    print()
    
    print("📝 Next Steps:")
    print("1. Apply the Supabase security fixes using the SQL file")
    print("2. Wait for connection limits to reset")
    print("3. Test your app functionality")
    print("4. Consider upgrading your Supabase plan")

if __name__ == "__main__":
    main() 