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
    
    # Configure the app - ALWAYS try Supabase first
    database_url = os.environ.get('DATABASE_URL')
    
    # Use Supabase/PostgreSQL - this is your main database with your data
    if database_url and database_url.startswith('postgresql://'):
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        
        # Configure database connection pooling for Supabase with better timeout handling
        engine_options = {
            'pool_size': 1,  # Minimal pool size to avoid connection limits
            'pool_recycle': 1800,  # Recycle connections every 30 minutes
            'pool_pre_ping': True,  # Test connections before use
            'max_overflow': 2,  # Minimal overflow to avoid connection limits
            'pool_timeout': 10,  # Wait up to 10 seconds for a connection
            'connect_args': {
                'connect_timeout': 10,  # Minimal connection timeout
                'application_name': 'budge-it-app',
                'options': '-c statement_timeout=15000'  # 15 second statement timeout
            }
        }
        
        # Override with environment variable if provided
        sqlalchemy_options = os.environ.get('SQLALCHEMY_ENGINE_OPTIONS')
        if sqlalchemy_options:
            try:
                env_options = json.loads(sqlalchemy_options)
                engine_options.update(env_options)
            except json.JSONDecodeError:
                print("Warning: Invalid SQLALCHEMY_ENGINE_OPTIONS JSON")
        
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options
        print(f"Using Supabase database: {database_url[:50]}...")
        print(f"Database pool configuration: {engine_options}")
    else:
        # Only use SQLite if NO DATABASE_URL is provided
        app.config['SECRET_KEY'] = 'dev-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
        print("No DATABASE_URL found, using SQLite for development only")
    
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
    
    # Initialize database tables
    with app.app_context():
        try:
            print("🔄 Initializing database tables...")
            db.create_all()
            print("✅ Database tables created/verified successfully!")
            
            # Check existing users in Supabase with retry logic (non-blocking)
            try:
                print("🔄 Checking existing users...")
                from .models import User
                user_count = User.query.count()
                print(f"✅ Found {user_count} existing users in database")
                
                # Only create admin if NO users exist at all
                if user_count == 0:
                    print("🔄 No users found, creating admin user...")
                    admin_user = User(username='admin', email='admin@example.com')
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)
                    db.session.commit()
                    print("✅ Admin user created successfully!")
                else:
                    print(f"✅ Database has {user_count} existing users - PRESERVING ALL DATA")
                    
            except Exception as db_error:
                print(f"⚠️ Database query failed: {db_error}")
                print("This is likely due to Supabase connection limits.")
                print("Your data is safe - the app will work once connections are restored.")
                print("Users will need to log in again once database is available.")
            
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
            
            # If Supabase fails, just continue - don't crash the app
            if database_url and database_url.startswith('postgresql://'):
                print("⚠️ SUPABASE CONNECTION FAILED - YOUR DATA IS STILL THERE!")
                print("App will start but database operations may fail until connection is restored.")
                print("This is temporary - your data is safe in Supabase.")
                print("Connection error details:", str(e))
                print("Solutions:")
                print("1. Wait 15-30 minutes for connection limits to reset")
                print("2. Upgrade your Supabase plan for higher connection limits")
                print("3. Monitor status at: https://budge-it-j4bp.onrender.com/check-supabase")
                print("4. Check auth health at: https://budge-it-j4bp.onrender.com/auth-health")
    
    print("✅ Flask application initialization completed")
    return app
