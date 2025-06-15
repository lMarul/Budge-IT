#!/usr/bin/env python3
"""
Test script to test the chart data API endpoint.
"""

import sys
import os
import requests
import json

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, session
from config import config
from database.models import db, User, Category, Transaction
from database.utils import get_transactions_by_user, get_categories_by_user_and_type

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def test_chart_data():
    """Test the chart data generation logic."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a non-admin user
            user = User.query.filter(User.username != 'admin').first()
            if not user:
                print("No non-admin users found")
                return
            
            print(f"Testing with user: {user.username} (ID: {user.id})")
            
            # Simulate session
            with app.test_request_context():
                session['user_id'] = user.id
                session['username'] = user.username
                
                print(f"Session user_id: {session.get('user_id')}")
                
                # Test chart data generation
                from routes.main import get_chart_data
                
                # Test income chart data
                print("\n--- Testing Income Chart Data ---")
                income_data = get_chart_data('income')
                print(f"Income data: {income_data}")
                
                # Test expense chart data
                print("\n--- Testing Expense Chart Data ---")
                expense_data = get_chart_data('expense')
                print(f"Expense data: {expense_data}")
                
                # Test individual mode
                print("\n--- Testing Individual Mode ---")
                individual_income = get_chart_data('income')
                print(f"Individual income data: {individual_income}")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == '__main__':
    exit(test_chart_data()) 