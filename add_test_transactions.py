#!/usr/bin/env python3
"""
Script to add test transactions for testing deletion functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database.utils import create_transaction, get_categories_by_user_and_type
from database.models import User
from datetime import date

def add_test_transactions():
    """Add test transactions for the admin user."""
    with app.app_context():
        print("Adding test transactions for admin user...")
        
        # Get admin user
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user not found. Please create an admin user first.")
            return False
        
        user_id = user.id
        print(f"✅ Found user: {user.username} (ID: {user_id})")
        
        # Get user's categories
        income_categories = get_categories_by_user_and_type(user_id, 'income')
        expense_categories = get_categories_by_user_and_type(user_id, 'expense')
        
        print(f"📊 Found {len(income_categories)} income categories and {len(expense_categories)} expense categories")
        
        # Add test transactions
        test_transactions = [
            # Income transactions
            {
                'amount': 5000.00,
                'category_id': income_categories[0].id if income_categories else None,
                'transaction_type': 'income',
                'date': date.today(),
                'item_name': 'Salary Payment'
            },
            {
                'amount': 1000.00,
                'category_id': income_categories[0].id if income_categories else None,
                'transaction_type': 'income',
                'date': date.today(),
                'item_name': 'Freelance Work'
            },
            # Expense transactions
            {
                'amount': 500.00,
                'category_id': expense_categories[0].id if expense_categories else None,
                'transaction_type': 'expense',
                'date': date.today(),
                'item_name': 'Grocery Shopping'
            },
            {
                'amount': 200.00,
                'category_id': expense_categories[0].id if expense_categories else None,
                'transaction_type': 'expense',
                'date': date.today(),
                'item_name': 'Transportation'
            }
        ]
        
        created_count = 0
        for transaction_data in test_transactions:
            if transaction_data['category_id'] is None:
                print(f"⚠️  Skipping transaction '{transaction_data['item_name']}' - no category available")
                continue
                
            transaction = create_transaction(
                user_id=user_id,
                amount=transaction_data['amount'],
                category_id=transaction_data['category_id'],
                transaction_type=transaction_data['transaction_type'],
                date=transaction_data['date'],
                item_name=transaction_data['item_name']
            )
            
            if transaction:
                print(f"✅ Created transaction: {transaction.item_name} - ₱{transaction.amount} ({transaction.transaction_type})")
                created_count += 1
            else:
                print(f"❌ Failed to create transaction: {transaction_data['item_name']}")
        
        print(f"\n📊 Successfully created {created_count} test transactions!")
        return created_count > 0

if __name__ == "__main__":
    success = add_test_transactions()
    if success:
        print("\n🎉 Test transactions added successfully!")
        print("You can now test the deletion functionality.")
    else:
        print("\n💥 Failed to add test transactions!") 