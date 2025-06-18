from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Logging: suppress noisy DB warnings
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
    logging.getLogger('psycopg2').setLevel(logging.ERROR)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    app.config['DEBUG'] = False

    # Database config: Supabase or fallback to SQLite
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        if 'connect_timeout' not in database_url:
            database_url += ('&' if '?' in database_url else '?') + 'connect_timeout=5'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 1,
            'pool_recycle': 300,
            'pool_pre_ping': True,
            'max_overflow': 0,
            'pool_timeout': 5,
            'connect_args': {
                'connect_timeout': 5,
                'application_name': 'budge-it-app'
            }
        }
        print("✅ Using Supabase database")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        print("✅ Using SQLite database (fallback)")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Jinja2 filters
    from .utils.database import datetimeformat, amount_color
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['amount_color'] = amount_color

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            from .models import User
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Error loading user {user_id}: {e}")
            return None

    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"⚠️ Database warning: {e}")
            print("✅ App will still work!")

    print("✅ Flask application created successfully")
    return app
