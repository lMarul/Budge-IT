#!/usr/bin/env python3
"""
Script to create sample transactions for testing charts.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from config import config
from database.models import db, User, Category, Transaction
from database.utils import create_transaction

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def create_sample_data():
    """Create sample transactions for testing."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a non-admin user
            user = User.query.filter(User.username != 'admin').first()
            if not user:
                print("No non-admin users found")
                return
            
            print(f"Creating sample data for user: {user.username} (ID: {user.id})")
            
            # Get user's categories
            income_categories = Category.query.filter_by(user_id=user.id, category_type='income').all()
            expense_categories = Category.query.filter_by(user_id=user.id, category_type='expense').all()
            
            print(f"Found {len(income_categories)} income categories and {len(expense_categories)} expense categories")
            
            if not income_categories or not expense_categories:
                print("User doesn't have categories. Please run the fix_categories script first.")
                return
            
            # Create sample income transactions
            sample_income = [
                {'amount': 50000, 'item_name': 'Monthly Salary', 'days_ago': 5},
                {'amount': 5000, 'item_name': 'Freelance Project', 'days_ago': 10},
                {'amount': 2000, 'item_name': 'Investment Dividend', 'days_ago': 15},
            ]
            
            # Create sample expense transactions
            sample_expenses = [
                {'amount': 5000, 'item_name': 'Grocery Shopping', 'days_ago': 1},
                {'amount': 2000, 'item_name': 'Gas Station', 'days_ago': 2},
                {'amount': 3000, 'item_name': 'Restaurant Dinner', 'days_ago': 3},
                {'amount': 1500, 'item_name': 'Movie Tickets', 'days_ago': 4},
                {'amount': 8000, 'item_name': 'Electric Bill', 'days_ago': 7},
            ]
            
            # Create income transactions
            for i, income_data in enumerate(sample_income):
                category = income_categories[i % len(income_categories)]
                date = datetime.now().date() - timedelta(days=income_data['days_ago'])
                
                transaction = create_transaction(
                    user_id=user.id,
                    amount=income_data['amount'],
                    category_id=category.id,
                    transaction_type='income',
                    date=date,
                    item_name=income_data['item_name']
                )
                
                if transaction:
                    print(f"✓ Created income transaction: {income_data['item_name']} - ₱{income_data['amount']}")
                else:
                    print(f"✗ Failed to create income transaction: {income_data['item_name']}")
            
            # Create expense transactions
            for i, expense_data in enumerate(sample_expenses):
                category = expense_categories[i % len(expense_categories)]
                date = datetime.now().date() - timedelta(days=expense_data['days_ago'])
                
                transaction = create_transaction(
                    user_id=user.id,
                    amount=expense_data['amount'],
                    category_id=category.id,
                    transaction_type='expense',
                    date=date,
                    item_name=expense_data['item_name']
                )
                
                if transaction:
                    print(f"✓ Created expense transaction: {expense_data['item_name']} - ₱{expense_data['amount']}")
                else:
                    print(f"✗ Failed to create expense transaction: {expense_data['item_name']}")
            
            print("\nSample data creation completed!")
            
            # Show summary
            total_transactions = Transaction.query.filter_by(user_id=user.id).count()
            total_income = sum(t.amount for t in Transaction.query.filter_by(user_id=user.id, transaction_type='income').all())
            total_expenses = sum(t.amount for t in Transaction.query.filter_by(user_id=user.id, transaction_type='expense').all())
            
            print(f"\nSummary:")
            print(f"Total transactions: {total_transactions}")
            print(f"Total income: ₱{total_income:,.2f}")
            print(f"Total expenses: ₱{total_expenses:,.2f}")
            print(f"Net balance: ₱{total_income - total_expenses:,.2f}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == '__main__':
    exit(create_sample_data()) 