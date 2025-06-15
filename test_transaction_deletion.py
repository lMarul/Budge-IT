#!/usr/bin/env python3
"""
Test script to verify transaction deletion functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database.utils import get_transactions_by_user, delete_transaction as delete_transaction_util
from database.models import User

def test_transaction_deletion():
    """Test transaction deletion functionality."""
    with app.app_context():
        print("Testing transaction deletion functionality...")
        
        # Get a test user (assuming admin user exists)
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user not found. Please create an admin user first.")
            return False
        
        user_id = user.id
        print(f"✅ Found user: {user.username} (ID: {user_id})")
        
        # Get user's transactions
        transactions = get_transactions_by_user(user_id)
        print(f"📊 Found {len(transactions)} transactions for user")
        
        if not transactions:
            print("❌ No transactions found. Please add some transactions first.")
            return False
        
        # Test deletion of the first transaction
        test_transaction = transactions[0]
        print(f"🧪 Testing deletion of transaction: {test_transaction.item_name} (ID: {test_transaction.id})")
        
        # Delete the transaction
        result = delete_transaction_util(test_transaction.id, user_id)
        
        if result:
            print(f"✅ Transaction deleted successfully!")
            print(f"   Deleted: {result['item_name']} - ₱{result['amount']} ({result['type']})")
            
            # Verify transaction is no longer in database
            remaining_transactions = get_transactions_by_user(user_id)
            if len(remaining_transactions) == len(transactions) - 1:
                print("✅ Transaction count decreased by 1 - deletion verified!")
                return True
            else:
                print("❌ Transaction count mismatch - deletion may have failed!")
                return False
        else:
            print("❌ Transaction deletion failed!")
            return False

if __name__ == "__main__":
    success = test_transaction_deletion()
    if success:
        print("\n🎉 All tests passed! Transaction deletion is working correctly.")
    else:
        print("\n💥 Tests failed! Please check the issues above.") 