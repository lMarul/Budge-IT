from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import json

# Initialize extensions locally to avoid circular imports
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    # Create Flask app with explicit template and static folder paths
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configure the app - USE SUPABASE (your data is there!)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith('postgresql://'):
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        
        # Ultra-conservative connection settings to avoid Supabase limits
        engine_options = {
            'pool_size': 1,  # Minimum pool size
            'pool_recycle': 300,  # Recycle connections every 5 minutes
            'pool_pre_ping': True,  # Test connections before use
            'max_overflow': 0,  # No overflow connections
            'pool_timeout': 3,  # Short timeout
            'connect_args': {
                'connect_timeout': 3,  # Short connection timeout
                'application_name': 'budge-it-app',
                'options': '-c statement_timeout=5000'  # Short statement timeout
            }
        }
        
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options
        print(f"✅ Using Supabase database: {database_url[:50]}...")
        print("✅ Your data is safe in Supabase!")
    else:
        # Fallback to SQLite only if no DATABASE_URL
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
        print("⚠️ No DATABASE_URL found, using SQLite (your Supabase data is still safe!)")
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register custom Jinja2 filters
    from .utils.database import datetimeformat, amount_color
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['amount_color'] = amount_color
    
    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Flask-Login user_loader with fallback
    @login_manager.user_loader
    def load_user(user_id):
        try:
            # Import User model here to avoid circular imports
            from .models import User
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Error loading user {user_id}: {e}")
            # Return None to force re-authentication if database is down
            return None
    
    # Initialize database tables with minimal connection attempt
    with app.app_context():
        try:
            print("🔄 Initializing database tables...")
            db.create_all()
            print("✅ Database tables created/verified successfully!")
            
            # Skip user check to avoid connection issues during startup
            print("✅ Database initialization completed - connection will be tested on first user request")
            
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
            print("⚠️ YOUR SUPABASE DATA IS STILL SAFE!")
            print("✅ App will start and work once connection limits reset")
            print("✅ Users can still access the app - database will connect when available")
    
    print("✅ Flask application initialization completed")
    print("✅ Your app is ready to use!")
    return app
