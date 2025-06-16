# Production WSGI entry point for Render deployment
from app import create_app

# Create the application instance with production configuration
app = create_app()

if __name__ == "__main__":
    app.run()
