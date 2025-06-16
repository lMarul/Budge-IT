#!/usr/bin/env python3
"""
Comprehensive Fix Script for Render Deployment
"""

import os
import sys

def fix_requirements():
    """Ensure requirements.txt has all necessary dependencies"""
    print("🔧 Fixing requirements.txt...")
    
    requirements = """# Budget Tracker Flask Application - Render Optimized
# Core Flask Framework
Flask==3.0.0
Werkzeug==3.0.1

# Template Engine
Jinja2==3.1.2
MarkupSafe==2.1.3

# Security & Serialization
itsdangerous==2.1.2

# Command Line Interface
click==8.1.7

# Event Handling
blinker==1.7.0

# Database - SQLAlchemy and PostgreSQL for Supabase
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
Flask-Login==0.6.3

# Production Deployment
gunicorn==21.2.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ requirements.txt fixed")

def fix_wsgi():
    """Ensure wsgi.py is properly configured"""
    print("🔧 Fixing wsgi.py...")
    
    wsgi_content = """# Production WSGI entry point for Render deployment
from app import create_app

# Create the application instance with production configuration
app = create_app()

if __name__ == "__main__":
    app.run()
"""
    
    with open('wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    print("✅ wsgi.py fixed")

def fix_app_init():
    """Ensure app/__init__.py is properly configured"""
    print("🔧 Fixing app/__init__.py...")
    
    init_content = """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    # Create Flask app with explicit template and static folder paths
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configure the app - prioritize DATABASE_URL environment variable
    if os.environ.get('DATABASE_URL'):
        # Production configuration with cloud database
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        print(f"🔗 Using cloud database: {os.environ.get('DATABASE_URL')[:50]}...")
    else:
        # Development configuration with local SQLite
        app.config['SECRET_KEY'] = 'dev-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
        print("💾 Using local SQLite database")
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Import models to ensure they're registered
    from .models import User, Category, Transaction

    # Flask-Login user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified successfully!")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
    
    return app
"""
    
    with open('app/__init__.py', 'w') as f:
        f.write(init_content)
    
    print("✅ app/__init__.py fixed")

def create_render_config():
    """Create Render-specific configuration"""
    print("🔧 Creating Render configuration...")
    
    render_config = """# Render deployment configuration
# This file helps Render understand how to deploy your app

# Build command: pip install -r requirements.txt
# Start command: gunicorn wsgi:app

# Environment variables needed:
# DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
# SECRET_KEY=your-secret-key-here
# FLASK_ENV=production
"""
    
    with open('RENDER_CONFIG.md', 'w') as f:
        f.write(render_config)
    
    print("✅ Render configuration created")

def test_fixes():
    """Test that all fixes work"""
    print("🧪 Testing fixes...")
    
    try:
        # Test imports
        import flask
        import flask_sqlalchemy
        import flask_login
        import gunicorn
        print("✅ All imports successful")
        
        # Test app creation
        from app import create_app
        app = create_app()
        print("✅ App creation successful")
        
        # Test WSGI
        from wsgi import app as wsgi_app
        print("✅ WSGI import successful")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🚀 Comprehensive Deployment Fix")
    print("=" * 40)
    
    # Run all fixes
    fixes = [
        fix_requirements,
        fix_wsgi,
        fix_app_init,
        create_render_config
    ]
    
    for fix in fixes:
        try:
            fix()
        except Exception as e:
            print(f"❌ Fix failed: {e}")
    
    # Test fixes
    if test_fixes():
        print("\n🎉 All fixes applied successfully!")
        print("\n📋 Your app is now ready for Render deployment:")
        print("1. Go to render.com → New + → Web Service")
        print("2. Connect your GitHub repository")
        print("3. Set configuration:")
        print("   - Name: budget-tracker")
        print("   - Environment: Python 3")
        print("   - Build Command: pip install -r requirements.txt")
        print("   - Start Command: gunicorn wsgi:app")
        print("4. Set environment variables:")
        print("   - DATABASE_URL (your Supabase connection string)")
        print("   - SECRET_KEY (your secret key)")
        print("   - FLASK_ENV=production")
        print("5. Deploy!")
    else:
        print("\n❌ Some fixes failed. Please check the errors above.")

if __name__ == "__main__":
    main() 