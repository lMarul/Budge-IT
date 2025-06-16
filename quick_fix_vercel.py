#!/usr/bin/env python3
"""
Quick Fix for Vercel Internal Server Error
This script helps diagnose and fix common Vercel deployment issues.
"""

import os
import sys
import subprocess

def check_environment():
    """Check if environment variables are set"""
    print("🔍 Checking Environment Variables...")
    
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'FLASK_ENV']
    missing_vars = []
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    return missing_vars

def generate_secret_key():
    """Generate a secure secret key"""
    import secrets
    return secrets.token_hex(32)

def setup_vercel_env():
    """Set up Vercel environment variables"""
    print("\n🚀 Setting up Vercel Environment Variables...")
    
    # Get Supabase connection string
    print("\n📋 Please provide your Supabase connection string:")
    print("Format: postgresql://postgres:[password]@[host]:5432/postgres")
    database_url = input("DATABASE_URL: ").strip()
    
    if not database_url:
        print("❌ DATABASE_URL is required!")
        return False
    
    # Generate secret key
    secret_key = generate_secret_key()
    print(f"🔑 Generated SECRET_KEY: {secret_key[:20]}...")
    
    # Check if Vercel CLI is available
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n✅ Vercel CLI found! Setting up environment variables...")
            
            # Set environment variables
            commands = [
                f'vercel env add DATABASE_URL production "{database_url}"',
                f'vercel env add SECRET_KEY production "{secret_key}"',
                'vercel env add FLASK_ENV production "production"'
            ]
            
            for cmd in commands:
                print(f"Running: {cmd}")
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"✅ Success: {cmd.split()[2]}")
                    else:
                        print(f"❌ Error: {result.stderr}")
                except Exception as e:
                    print(f"❌ Error running command: {e}")
            
            print("\n🎉 Environment variables set successfully!")
            print("Next step: Run 'vercel --prod' to redeploy")
            return True
            
        else:
            print("❌ Vercel CLI not working properly")
            return False
            
    except FileNotFoundError:
        print("\n⚠️ Vercel CLI not found. Please set environment variables manually:")
        print("1. Go to your Vercel project dashboard")
        print("2. Navigate to Settings → Environment Variables")
        print("3. Add the following variables:")
        print()
        print("DATABASE_URL:")
        print(f"  {database_url}")
        print()
        print("SECRET_KEY:")
        print(f"  {secret_key}")
        print()
        print("FLASK_ENV:")
        print("  production")
        return True

def test_local_setup():
    """Test the setup locally"""
    print("\n🧪 Testing Local Setup...")
    
    # Set environment variables for testing
    os.environ['FLASK_ENV'] = 'production'
    
    if not os.environ.get('DATABASE_URL'):
        print("⚠️ DATABASE_URL not set, skipping database test")
        return False
    
    try:
        # Test database connection
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models import User
            # Try to query the database
            user_count = User.query.count()
            print(f"✅ Database connection successful! Found {user_count} users.")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Quick Fix for Vercel Internal Server Error")
    print("=" * 50)
    
    # Check current environment
    missing_vars = check_environment()
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        setup_vercel_env()
    else:
        print("\n✅ All environment variables are set!")
    
    # Test local setup
    test_local_setup()
    
    print("\n📋 Next Steps:")
    print("1. If environment variables were set, redeploy with: vercel --prod")
    print("2. If using dashboard, go to Vercel and redeploy manually")
    print("3. Check the /test-env route on your deployed app to verify setup")
    print("4. If still having issues, check Vercel function logs")

if __name__ == "__main__":
    main() 