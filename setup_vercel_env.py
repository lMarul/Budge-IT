#!/usr/bin/env python3
"""
Vercel Environment Variables Setup Script
This script helps you set up environment variables for Vercel deployment.
"""

import os
import subprocess
import sys

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def setup_environment_variables():
    """Set up environment variables for Vercel"""
    print("🚀 Vercel Environment Variables Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("📁 Found .env file")
        with open('.env', 'r') as f:
            env_content = f.read()
        print("Current .env contents:")
        print(env_content)
        print()
    
    # Get environment variables from user
    print("Please provide the following environment variables:")
    
    database_url = input("DATABASE_URL (Supabase connection string): ").strip()
    secret_key = input("SECRET_KEY (Flask secret key): ").strip()
    
    if not database_url or not secret_key:
        print("❌ Error: Both DATABASE_URL and SECRET_KEY are required!")
        return False
    
    # Check if Vercel CLI is available
    if check_vercel_cli():
        print("\n✅ Vercel CLI found! Setting up environment variables...")
        
        # Set environment variables using Vercel CLI
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
                    print(f"✅ Success: {cmd}")
                else:
                    print(f"❌ Error: {result.stderr}")
            except Exception as e:
                print(f"❌ Error running command: {e}")
        
        print("\n🎉 Environment variables set successfully!")
        print("You can now deploy with: vercel --prod")
        
    else:
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

def create_env_template():
    """Create a template .env file for local development"""
    template_content = """# Local Development Environment Variables
# Copy this file to .env and fill in your values

# Database Configuration (Supabase)
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development

# Optional: Debug mode
DEBUG=True
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    
    print("📝 Created .env.template file for local development")

if __name__ == "__main__":
    print("Vercel Environment Setup Tool")
    print("=" * 30)
    
    # Create template file
    create_env_template()
    
    # Setup environment variables
    setup_environment_variables()
    
    print("\n📋 Next Steps:")
    print("1. If using Vercel CLI: Run 'vercel --prod' to deploy")
    print("2. If using dashboard: Go to Vercel and deploy your project")
    print("3. For local development: Copy .env.template to .env and fill in values") 