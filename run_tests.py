#!/usr/bin/env python3
"""
Test Runner for Budget Tracker Application
==========================================

This script provides an easy way to run tests and generate comprehensive reports
for the Budget Tracker application.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --basic            # Run basic tests only
    python run_tests.py --auth             # Run authentication tests only
    python run_tests.py --dashboard        # Run dashboard tests only
    python run_tests.py --transactions     # Run transaction tests only
    python run_tests.py --categories       # Run category tests only
    python run_tests.py --admin            # Run admin tests only
    python run_tests.py --api              # Run API tests only
    python run_tests.py --report           # Generate test report only
    python run_tests.py --coverage         # Run tests with coverage report
"""

import sys
import os
import argparse
import json
from datetime import datetime
from test_utils import run_basic_tests, generate_test_report
from tests import run_all_tests

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🧪 BUDGET TRACKER - TESTING SUITE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def run_basic_functionality_tests():
    """Run basic functionality tests"""
    print("\n🔧 Running Basic Functionality Tests...")
    try:
        run_basic_tests()
        print("✅ Basic tests completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Basic tests failed: {e}")
        return False

def run_specific_test_category(category):
    """Run tests for a specific category"""
    import unittest
    
    print(f"\n🎯 Running {category.title()} Tests...")
    
    # Import test modules
    from tests import (
        TestBasicFunctionality, TestAuthentication, TestDashboard,
        TestTransactions, TestCategories, TestHistory,
        TestAdminFunctionality, TestAPIEndpoints, TestErrorHandling
    )
    
    # Map category names to test classes
    test_map = {
        'basic': TestBasicFunctionality,
        'auth': TestAuthentication,
        'dashboard': TestDashboard,
        'transactions': TestTransactions,
        'categories': TestCategories,
        'history': TestHistory,
        'admin': TestAdminFunctionality,
        'api': TestAPIEndpoints,
        'error': TestErrorHandling
    }
    
    if category not in test_map:
        print(f"❌ Unknown test category: {category}")
        return False
    
    # Create test suite for specific category
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_map[category])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print results
    print(f"\n📊 {category.title()} Test Results:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

def generate_comprehensive_report():
    """Generate a comprehensive test report"""
    print("\n📋 Generating Comprehensive Test Report...")
    
    try:
        # Generate test report
        report = generate_test_report()
        
        # Add timestamp
        report['generated_at'] = datetime.now().isoformat()
        report['test_environment'] = {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': os.getcwd()
        }
        
        # Save report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Test report saved to: {report_file}")
        
        # Print summary
        print("\n📊 Test Report Summary:")
        print(f"  Database Users: {report['database_stats']['users']}")
        print(f"  Database Categories: {report['database_stats']['categories']}")
        print(f"  Database Transactions: {report['database_stats']['transactions']}")
        print(f"  Testing Mode: {report['test_config']['testing']}")
        print(f"  Debug Mode: {report['test_config']['debug']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate report: {e}")
        return False

def run_coverage_tests():
    """Run tests with coverage reporting"""
    try:
        import coverage
        
        print("\n📊 Running Tests with Coverage...")
        
        # Start coverage measurement
        cov = coverage.Coverage()
        cov.start()
        
        # Run all tests
        result = run_all_tests()
        
        # Stop coverage measurement
        cov.stop()
        cov.save()
        
        # Generate coverage report
        print("\n📈 Coverage Report:")
        cov.report()
        
        # Generate HTML coverage report
        cov.html_report(directory='htmlcov')
        print("📁 HTML coverage report generated in 'htmlcov' directory")
        
        return len(result.failures) == 0 and len(result.errors) == 0
        
    except ImportError:
        print("❌ Coverage module not installed. Install with: pip install coverage")
        return False
    except Exception as e:
        print(f"❌ Coverage test failed: {e}")
        return False

def main():
    """Main function to handle command line arguments and run tests"""
    parser = argparse.ArgumentParser(
        description='Budget Tracker Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--basic', action='store_true',
                       help='Run basic functionality tests only')
    parser.add_argument('--auth', action='store_true',
                       help='Run authentication tests only')
    parser.add_argument('--dashboard', action='store_true',
                       help='Run dashboard tests only')
    parser.add_argument('--transactions', action='store_true',
                       help='Run transaction tests only')
    parser.add_argument('--categories', action='store_true',
                       help='Run category tests only')
    parser.add_argument('--admin', action='store_true',
                       help='Run admin tests only')
    parser.add_argument('--api', action='store_true',
                       help='Run API tests only')
    parser.add_argument('--report', action='store_true',
                       help='Generate test report only')
    parser.add_argument('--coverage', action='store_true',
                       help='Run tests with coverage report')
    parser.add_argument('--all', action='store_true',
                       help='Run all tests (default)')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Determine what to run
    if args.basic:
        success = run_basic_functionality_tests()
    elif args.auth:
        success = run_specific_test_category('auth')
    elif args.dashboard:
        success = run_specific_test_category('dashboard')
    elif args.transactions:
        success = run_specific_test_category('transactions')
    elif args.categories:
        success = run_specific_test_category('categories')
    elif args.admin:
        success = run_specific_test_category('admin')
    elif args.api:
        success = run_specific_test_category('api')
    elif args.report:
        success = generate_comprehensive_report()
    elif args.coverage:
        success = run_coverage_tests()
    else:
        # Default: run all tests
        print("\n🚀 Running Complete Test Suite...")
        result = run_all_tests()
        success = len(result.failures) == 0 and len(result.errors) == 0
    
    # Print final summary
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED! The application is ready for deployment.")
    else:
        print("❌ SOME TESTS FAILED! Please review the issues above.")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main()) 