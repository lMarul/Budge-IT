# Testing Utilities for Budget Tracker
import os
import tempfile
import json
from datetime import datetime, date
from flask import Flask
from app import create_app, db
from app.models import User, Category, Transaction
from test_config import TestConfig, TEST_DATA

def create_test_app():
    """Create a Flask app configured for testing"""
    app = create_app()
    app.config.from_object(TestConfig)
    
    # Create a temporary database
    with app.app_context():
        db.create_all()
    
    return app

def setup_test_data(app):
    """Set up test data in the database"""
    with app.app_context():
        # Clear existing data
        Transaction.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # Create test users
        users = {}
        for user_data in TEST_DATA['users']:
            user = User(
                username=user_data['username'],
                email=user_data['email']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            db.session.flush()  # Get the ID
            users[user_data['username']] = user
        
        # Create test categories for each user
        categories = {}
        for user in users.values():
            for cat_data in TEST_DATA['categories']:
                category = Category(
                    user_id=user.id,
                    name=cat_data['name'],
                    category_type=cat_data['type'],
                    color=cat_data['color']
                )
                db.session.add(category)
                db.session.flush()
                categories[f"{user.username}_{cat_data['name']}"] = category
        
        # Create test transactions
        for trans_data in TEST_DATA['transactions']:
            # Assign to first user for simplicity
            user = users['testuser1']
            category_name = trans_data['category']
            category = categories.get(f"{user.username}_{category_name}")
            
            if category:
                transaction = Transaction(
                    user_id=user.id,
                    category_id=category.id,
                    amount=trans_data['amount'],
                    transaction_type=trans_data['type'],
                    date=datetime.strptime(trans_data['date'], '%Y-%m-%d').date(),
                    item_name=trans_data['item_name']
                )
                db.session.add(transaction)
        
        db.session.commit()
        return users, categories

def cleanup_test_data(app):
    """Clean up test data from database"""
    with app.app_context():
        Transaction.query.delete()
        Category.query.delete()
        User.query.delete()
        db.session.commit()

def create_test_client():
    """Create a test client with test data"""
    app = create_test_app()
    users, categories = setup_test_data(app)
    
    return app.test_client(), app, users, categories

def login_test_user(client, username='testuser1', password='testpass123'):
    """Helper function to login a test user"""
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def logout_test_user(client):
    """Helper function to logout a test user"""
    return client.get('/logout', follow_redirects=True)

def get_test_user_session(client, username='testuser1'):
    """Get a test user session"""
    login_test_user(client, username)
    return client

def create_sample_transaction_data():
    """Create sample transaction data for testing"""
    return {
        'amount': 150.00,
        'category_id': 1,
        'transaction_type': 'expense',
        'date': date.today().isoformat(),
        'item_name': 'Test Transaction'
    }

def create_sample_category_data():
    """Create sample category data for testing"""
    return {
        'name': 'Test Category',
        'category_type': 'expense',
        'color': '#ff0000'
    }

def assert_response_contains(response, text):
    """Assert that response contains specific text"""
    assert text in response.get_data(as_text=True)

def assert_response_redirects(response, expected_url):
    """Assert that response redirects to expected URL"""
    assert response.status_code in [301, 302]
    assert expected_url in response.location

def assert_json_response(response, expected_data):
    """Assert that JSON response contains expected data"""
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    for key, value in expected_data.items():
        assert data[key] == value

def generate_test_report():
    """Generate a test report with current test status"""
    app = create_test_app()
    
    with app.app_context():
        user_count = User.query.count()
        category_count = Category.query.count()
        transaction_count = Transaction.query.count()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'database_stats': {
                'users': user_count,
                'categories': category_count,
                'transactions': transaction_count
            },
            'test_config': {
                'testing': app.config.get('TESTING', False),
                'debug': app.config.get('DEBUG', False),
                'database_uri': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')
            }
        }
        
        return report

def run_basic_tests():
    """Run basic functionality tests"""
    print("Running basic tests...")
    
    # Test app creation
    app = create_test_app()
    print("✓ Test app created successfully")
    
    # Test database setup
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")
    
    # Test data setup
    users, categories = setup_test_data(app)
    print(f"✓ Test data created: {len(users)} users, {len(categories)} categories")
    
    # Test client creation
    client = app.test_client()
    print("✓ Test client created successfully")
    
    # Test basic routes
    response = client.get('/')
    assert response.status_code in [200, 302]  # 200 for login page, 302 for redirect
    print("✓ Root route accessible")
    
    response = client.get('/health')
    assert response.status_code == 200
    print("✓ Health check endpoint working")
    
    # Cleanup
    cleanup_test_data(app)
    print("✓ Test data cleaned up")
    
    print("All basic tests passed! ✅")

if __name__ == '__main__':
    run_basic_tests() 