# Anthony 

# Import operating system module for environment variables
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database_url():
    """
    Get database URL with proper formatting for Render deployment.
    
    Render provides DATABASE_URL in the format:
    postgresql://user:password@host:port/database
    
    This function ensures the URL is properly formatted.
    """
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        # Convert postgres:// to postgresql:// for newer versions
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

class Config:
    """
    Base configuration class for the Budget Tracker application.
    
    This class contains all configuration settings for the Flask application,
    including security settings, database configuration, and environment-specific
    settings.
    """
    
    # Flask secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # SQLAlchemy Database configuration for Supabase
    SQLALCHEMY_DATABASE_URI = get_database_url() or \
        'postgresql://postgres:password@localhost:5432/budget_tracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Legacy JSON database file (for migration purposes)
    DATABASE_FILE = 'budget_tracker.json'
    
    # Application settings
    HOST = '127.0.0.1'
    PORT = 5001
    
    # Debug mode - should be False in production
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    This configuration enables debug mode and provides detailed error messages
    for development purposes.
    """
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    
    # Development database URL (can be local PostgreSQL or Supabase)
    SQLALCHEMY_DATABASE_URI = get_database_url() or \
        'postgresql://postgres:password@localhost:5432/budget_tracker_dev'

class ProductionConfig(Config):
    """
    Production environment configuration.
    
    This configuration disables debug mode for security and performance
    in production environments.
    """
    DEBUG = False
    HOST = '0.0.0.0'  # Bind to all interfaces for Render
    PORT = int(os.environ.get('PORT', 10000))  # Render default port
    
    # Use environment variable for secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-this'
    
    # Production database URL (should be Supabase)
    SQLALCHEMY_DATABASE_URI = get_database_url()

class TestingConfig(Config):
    """
    Testing environment configuration.
    
    This configuration enables debug mode and uses a test database
    for automated testing.
    """
    DEBUG = True
    DATABASE_FILE = 'test_budget_tracker.json'
    HOST = '127.0.0.1'
    PORT = 5002
    
    # Test database URL (can be SQLite for faster testing)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_budget_tracker.db'

# Configuration dictionary for easy environment switching
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 