# Anthony - Updated for SQLAlchemy

# Import Flask framework for web application
from flask import Flask, render_template
# Import configuration settings
from config import config
# Import SQLAlchemy database initialization
from database.utils import initialize_database, datetimeformat
# Import route blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
import os

def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances.
    
    This function creates and configures a Flask application with the specified
    configuration, initializes the database, and registers all blueprints.
    
    Args:
        config_name: Name of the configuration to use ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(config[config_name])
    
    # Register Jinja2 custom filter for date formatting
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    
    # Initialize database on application startup
    initialize_database(app)
    
    # Register blueprints for route organization
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Handles 404 errors by rendering a custom error page.
        
        Args:
            error: The 404 error object
        
        Returns:
            str: Rendered 404 error template
        """
        return render_template('404.html'), 404
    
    # Error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        """
        Handles 500 errors by rendering a custom error page.
        
        Args:
            error: The 500 error object
        
        Returns:
            str: Rendered 500 error template
        """
        return render_template('500.html'), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Run application with configuration from config.py
    # For Render deployment, use environment variables
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False for production
    )


