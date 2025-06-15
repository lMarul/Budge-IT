from flask import Flask
from config import config
from database.utils import initialize_database, create_user

def create_admin():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    initialize_database(app)
    with app.app_context():
        username = "admin"
        email = "admin@example.com"
        password = "admin123"
        user = create_user(username, email, password)
        if user:
            print(f"✅ Admin account created: {username} / {email}")
        else:
            print("⚠️ Admin account already exists or could not be created.")

if __name__ == "__main__":
    create_admin()