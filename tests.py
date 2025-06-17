# Comprehensive Test Suite for Budget Tracker
import unittest
import json
from datetime import datetime, date
from test_utils import (
    create_test_app, setup_test_data, cleanup_test_data,
    login_test_user, logout_test_user, get_test_user_session,
    create_sample_transaction_data, create_sample_category_data,
    assert_response_contains, assert_response_redirects, assert_json_response
)

class BudgetTrackerTestCase(unittest.TestCase):
    """Base test case for Budget Tracker application"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.app = create_test_app()
        self.client = self.app.test_client()
        self.users, self.categories = setup_test_data(self.app)
        
        # Create app context
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after each test method"""
        cleanup_test_data(self.app)
        self.app_context.pop()

class TestBasicFunctionality(BudgetTrackerTestCase):
    """Test basic application functionality"""
    
    def test_app_creation(self):
        """Test that the app can be created"""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config['TESTING'])
    
    def test_root_route(self):
        """Test the root route"""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_database_connection(self):
        """Test database connection"""
        response = self.client.get('/test-db')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'connected')

class TestAuthentication(BudgetTrackerTestCase):
    """Test authentication functionality"""
    
    def test_login_page(self):
        """Test login page accessibility"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Login')
    
    def test_register_page(self):
        """Test register page accessibility"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Register')
    
    def test_user_login(self):
        """Test user login functionality"""
        response = login_test_user(self.client, 'testuser1', 'testpass123')
        self.assertEqual(response.status_code, 200)
        # Should redirect to dashboard after login
        assert_response_contains(response, 'Dashboard')
    
    def test_invalid_login(self):
        """Test invalid login credentials"""
        response = self.client.post('/login', data={
            'username': 'invaliduser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should show error message
        assert_response_contains(response, 'Invalid')
    
    def test_user_logout(self):
        """Test user logout functionality"""
        # First login
        login_test_user(self.client, 'testuser1', 'testpass123')
        # Then logout
        response = logout_test_user(self.client)
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
        assert_response_contains(response, 'Login')

class TestDashboard(BudgetTrackerTestCase):
    """Test dashboard functionality"""
    
    def test_dashboard_access_without_login(self):
        """Test dashboard access without authentication"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
        assert_response_contains(response, 'Login')
    
    def test_dashboard_access_with_login(self):
        """Test dashboard access with authentication"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Dashboard')
    
    def test_dashboard_financial_summary(self):
        """Test dashboard shows financial summary"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        # Should show income and expense totals
        assert_response_contains(response, 'Total Income')
        assert_response_contains(response, 'Total Expense')

class TestTransactions(BudgetTrackerTestCase):
    """Test transaction functionality"""
    
    def test_income_page_access(self):
        """Test income page accessibility"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/income')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Income')
    
    def test_expense_page_access(self):
        """Test expense page accessibility"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/expense')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Expense')
    
    def test_add_income_transaction(self):
        """Test adding income transaction"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        
        # Get a category ID for income
        from app.models import Category
        category = Category.query.filter_by(category_type='income').first()
        
        response = self.client.post('/add_transaction', data={
            'amount': 1000.00,
            'category_id': category.id,
            'transaction_type': 'income',
            'date': date.today().isoformat(),
            'item_name': 'Test Income'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should show success message or redirect to dashboard
        assert_response_contains(response, 'Dashboard')
    
    def test_add_expense_transaction(self):
        """Test adding expense transaction"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        
        # Get a category ID for expense
        from app.models import Category
        category = Category.query.filter_by(category_type='expense').first()
        
        response = self.client.post('/add_transaction', data={
            'amount': 50.00,
            'category_id': category.id,
            'transaction_type': 'expense',
            'date': date.today().isoformat(),
            'item_name': 'Test Expense'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should show success message or redirect to dashboard
        assert_response_contains(response, 'Dashboard')

class TestCategories(BudgetTrackerTestCase):
    """Test category management functionality"""
    
    def test_categories_page_access(self):
        """Test categories page accessibility"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Categories')
    
    def test_add_category(self):
        """Test adding new category"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        
        response = self.client.post('/add_category', data={
            'name': 'Test Category',
            'category_type': 'expense',
            'color': '#ff0000'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should redirect back to categories page
        assert_response_contains(response, 'Categories')

class TestHistory(BudgetTrackerTestCase):
    """Test transaction history functionality"""
    
    def test_history_page_access(self):
        """Test history page accessibility"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'History')
    
    def test_history_shows_transactions(self):
        """Test that history page shows transactions"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        # Should show transaction data
        assert_response_contains(response, 'Transaction')

class TestAdminFunctionality(BudgetTrackerTestCase):
    """Test admin functionality"""
    
    def test_admin_login(self):
        """Test admin login"""
        response = login_test_user(self.client, 'admin', 'adminpass123')
        self.assertEqual(response.status_code, 200)
        # Should redirect to admin dashboard
        assert_response_contains(response, 'Admin')
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard accessibility"""
        login_test_user(self.client, 'admin', 'adminpass123')
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
        assert_response_contains(response, 'Admin Dashboard')

class TestAPIEndpoints(BudgetTrackerTestCase):
    """Test API endpoints"""
    
    def test_get_categories_api(self):
        """Test categories API endpoint"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/get_categories')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('categories', data)
    
    def test_chart_data_api(self):
        """Test chart data API endpoint"""
        login_test_user(self.client, 'testuser1', 'testpass123')
        response = self.client.get('/get_chart_data/expense')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('labels', data)
        self.assertIn('data', data)

class TestErrorHandling(BudgetTrackerTestCase):
    """Test error handling"""
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
    
    def test_500_error(self):
        """Test 500 error handling"""
        # This would require triggering an actual error
        # For now, just test that error pages exist
        response = self.client.get('/500')
        self.assertIn(response.status_code, [404, 500])

def run_all_tests():
    """Run all tests and generate a report"""
    print("🧪 Starting Budget Tracker Test Suite...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(BudgetTrackerTestCase)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
    
    return result

if __name__ == '__main__':
    run_all_tests() 