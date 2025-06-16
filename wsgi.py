# Production WSGI entry point for Vercel deployment
import os
import sys
import traceback

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    
    # Create the application instance with production configuration
    app = create_app()
    
    # Ensure we're in production mode
    if not app.debug:
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Budget Tracker startup')
        
    # Add a test route to check environment variables
    @app.route('/test-env')
    def test_env():
        return {
            'database_url': bool(os.environ.get('DATABASE_URL')),
            'secret_key': bool(os.environ.get('SECRET_KEY')),
            'flask_env': os.environ.get('FLASK_ENV'),
            'python_path': os.environ.get('PYTHONPATH'),
            'app_debug': app.debug
        }
        
except Exception as e:
    print(f"Error creating app: {e}")
    print("Full traceback:")
    traceback.print_exc()
    raise

if __name__ == "__main__":
    app.run() 