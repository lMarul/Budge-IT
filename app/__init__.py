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
    
    # Configure the app - prioritize DATABASE_URL environment variable
    database_url = os.environ.get('DATABASE_URL')
    
    # Try to use cloud database, but fallback to SQLite if connection fails
    if database_url and database_url.startswith('postgresql://'):
        # Production configuration with cloud database
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        print(f"Using cloud database: {database_url[:50]}...")
    else:
        # Development configuration with local SQLite
        app.config['SECRET_KEY'] = 'dev-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
        print("Using local SQLite database")
    
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
    
    # Create database tables with fallback to SQLite if cloud database fails
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created/verified successfully!")
            
            # Create admin user if it doesn't exist
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(username='admin', email='admin@example.com')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created successfully!")
            
        except Exception as e:
            print(f"Database initialization warning: {e}")
            
            # If cloud database fails, fallback to SQLite
            if database_url and database_url.startswith('postgresql://'):
                print("Cloud database connection failed, falling back to SQLite...")
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
                db.init_app(app)
                
                try:
                    db.create_all()
                    print("SQLite database tables created successfully!")
                    
                    # Create admin user in SQLite
                    admin_user = User.query.filter_by(username='admin').first()
                    if not admin_user:
                        admin_user = User(username='admin', email='admin@example.com')
                        admin_user.set_password('admin123')
                        db.session.add(admin_user)
                        db.session.commit()
                        print("Admin user created in SQLite successfully!")
                        
                except Exception as sqlite_error:
                    print(f"SQLite fallback also failed: {sqlite_error}")
    
    return app
