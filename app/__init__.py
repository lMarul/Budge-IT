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
    
    # Configure the app
    if config_name == 'production' or os.environ.get('FLASK_ENV') == 'production':
        # Production configuration
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
    else:
        # Development configuration
        app.config['SECRET_KEY'] = 'dev-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    
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
        db.create_all()
    
    return app 