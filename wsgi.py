# Production WSGI entry point for Render deployment
import os
import sys

# Set environment for production
os.environ['FLASK_ENV'] = 'production'

try:
    from app import create_app
    
    # Create the application instance with production configuration
    app = create_app()
    
    # Ensure app is properly configured
    if not app:
        print("ERROR: Failed to create Flask application")
        sys.exit(1)
    
    print("✅ Flask application created successfully")
    
except Exception as e:
    print(f"ERROR: Failed to initialize application: {e}")
    # Create a minimal app to prevent deployment failure
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def health():
        return {'status': 'degraded', 'error': str(e)}, 503
    
    @app.route('/health')
    def health_check():
        return {'status': 'degraded', 'error': str(e)}, 503

if __name__ == "__main__":
    app.run()
