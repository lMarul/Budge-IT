# Production WSGI entry point for Vercel deployment
import os
import sys
from app import create_app

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

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

if __name__ == "__main__":
    app.run() 