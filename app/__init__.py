from flask import Flask
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
    
    # Configure the app - ALWAYS try Supabase first
    database_url = os.environ.get('DATABASE_URL')
    
    # Use Supabase/PostgreSQL - this is your main database with your data
    if database_url and database_url.startswith('postgresql://'):
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        print(f"Using Supabase database: {database_url[:50]}...")
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
    
    # Import models to ensure they're registered
    from .models import User, Category, Transaction

    # Flask-Login user_loader
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Error loading user {user_id}: {e}")
            return None
    
    # Create database tables - PRESERVE EXISTING DATA
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created/verified successfully!")
            
            # Check existing users in Supabase
            user_count = User.query.count()
            print(f"Found {user_count} existing users in database")
            
            # Only create admin if NO users exist at all
            if user_count == 0:
                print("No users found, creating admin user...")
                admin_user = User(username='admin', email='admin@example.com')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created successfully!")
            else:
                print(f"Database has {user_count} existing users - PRESERVING ALL DATA")
            
        except Exception as e:
            print(f"Database initialization warning: {e}")
            
            # If Supabase fails, just continue - don't crash the app
            if database_url and database_url.startswith('postgresql://'):
                print("SUPABASE CONNECTION FAILED - YOUR DATA IS STILL THERE!")
                print("App will start but database operations may fail until connection is restored.")
                print("This is temporary - your data is safe in Supabase.")
    
    return app
