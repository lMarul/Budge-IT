# Production WSGI entry point for Nhost deployment
import os
from app import create_app

# Create the application instance with production configuration
app = create_app()

# Configure for Nhost environment
if os.environ.get('NHOST_BACKEND_URL'):
    app.config['NHOST_BACKEND_URL'] = os.environ.get('NHOST_BACKEND_URL')
    app.config['NHOST_GRAPHQL_URL'] = os.environ.get('NHOST_GRAPHQL_URL')
    app.config['NHOST_STORAGE_URL'] = os.environ.get('NHOST_STORAGE_URL')
    app.config['NHOST_AUTH_URL'] = os.environ.get('NHOST_AUTH_URL')

if __name__ == "__main__":
    app.run() 