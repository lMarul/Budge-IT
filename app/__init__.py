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
    
    # Configure the app - prioritize Nhost environment variables
    if os.environ.get('NHOST_BACKEND_URL'):
        # Nhost production configuration
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or os.environ.get('NHOST_POSTGRES_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        app.config['NHOST_BACKEND_URL'] = os.environ.get('NHOST_BACKEND_URL')
        app.config['NHOST_GRAPHQL_URL'] = os.environ.get('NHOST_GRAPHQL_URL')
        app.config['NHOST_STORAGE_URL'] = os.environ.get('NHOST_STORAGE_URL')
        app.config['NHOST_AUTH_URL'] = os.environ.get('NHOST_AUTH_URL')
        print(f"🚀 Using Nhost backend: {os.environ.get('NHOST_BACKEND_URL')[:50]}...")
    elif os.environ.get('DATABASE_URL'):
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