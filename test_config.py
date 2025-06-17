# Testing Configuration for Budget Tracker
import os
import tempfile

class TestConfig:
    """Configuration for testing environment"""
    
    # Flask Testing Configuration
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    
    # Use temporary database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Test secret key
    SECRET_KEY = 'test-secret-key-for-testing-only'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Test file upload settings
    UPLOAD_FOLDER = tempfile.mkdtemp()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Test email settings (if needed)
    MAIL_SUPPRESS_SEND = True
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    
    # Test logging
    LOG_LEVEL = 'DEBUG'
    
    # Test session settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # Test rate limiting (disabled for testing)
    RATELIMIT_ENABLED = False
    
    # Test cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Test security headers (relaxed for testing)
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    }

# Test data configuration
TEST_DATA = {
    'users': [
        {
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'testpass123'
        },
        {
            'username': 'testuser2', 
            'email': 'test2@example.com',
            'password': 'testpass456'
        },
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'adminpass123'
        }
    ],
    'categories': [
        {'name': 'Salary', 'type': 'income', 'color': '#28a745'},
        {'name': 'Freelance', 'type': 'income', 'color': '#17a2b8'},
        {'name': 'Food', 'type': 'expense', 'color': '#dc3545'},
        {'name': 'Transport', 'type': 'expense', 'color': '#ffc107'},
        {'name': 'Entertainment', 'type': 'expense', 'color': '#6f42c1'},
        {'name': 'Bills', 'type': 'expense', 'color': '#fd7e14'}
    ],
    'transactions': [
        {'amount': 5000, 'type': 'income', 'category': 'Salary', 'item_name': 'Monthly Salary', 'date': '2024-01-15'},
        {'amount': 1000, 'type': 'income', 'category': 'Freelance', 'item_name': 'Web Design Project', 'date': '2024-01-20'},
        {'amount': 200, 'type': 'expense', 'category': 'Food', 'item_name': 'Grocery Shopping', 'date': '2024-01-18'},
        {'amount': 50, 'type': 'expense', 'category': 'Transport', 'item_name': 'Gas Station', 'date': '2024-01-19'},
        {'amount': 100, 'type': 'expense', 'category': 'Entertainment', 'item_name': 'Movie Night', 'date': '2024-01-21'}
    ]
} 