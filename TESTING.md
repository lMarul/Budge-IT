# Budget Tracker - Testing Documentation

## Overview

This document provides comprehensive information about testing the Budget Tracker application. The testing suite includes unit tests, integration tests, and automated test runners to ensure the application works correctly before deployment.

## Test Structure

```
├── test_config.py          # Testing configuration
├── test_utils.py           # Testing utilities and helpers
├── tests.py               # Comprehensive test suite
├── run_tests.py           # Test runner script
└── TESTING.md             # This documentation
```

## Quick Start

### 1. Install Testing Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Basic Tests

```bash
python test_utils.py
```

### 3. Run Complete Test Suite

```bash
python run_tests.py
```

### 4. Run Specific Test Categories

```bash
# Authentication tests only
python run_tests.py --auth

# Dashboard tests only
python run_tests.py --dashboard

# Transaction tests only
python run_tests.py --transactions

# Category management tests only
python run_tests.py --categories

# Admin functionality tests only
python run_tests.py --admin

# API endpoint tests only
python run_tests.py --api
```

## Test Categories

### 1. Basic Functionality Tests
- Application creation and configuration
- Database connection and setup
- Health check endpoints
- Basic route accessibility

### 2. Authentication Tests
- User registration
- User login/logout
- Invalid credential handling
- Session management
- Password hashing

### 3. Dashboard Tests
- Dashboard access control
- Financial summary display
- Data visualization
- User-specific data isolation

### 4. Transaction Tests
- Income transaction creation
- Expense transaction creation
- Transaction validation
- Transaction editing and deletion
- Date handling

### 5. Category Tests
- Category creation
- Category editing
- Category deletion
- Category color management
- User-specific categories

### 6. History Tests
- Transaction history display
- Filtering and sorting
- Pagination
- Export functionality

### 7. Admin Tests
- Admin authentication
- Admin dashboard access
- User management
- System statistics

### 8. API Tests
- REST API endpoints
- JSON response validation
- Chart data endpoints
- Error handling

## Test Configuration

The testing environment uses a separate configuration (`test_config.py`) that includes:

- **In-memory SQLite database** for fast testing
- **Test-specific secret keys** for security
- **Disabled CSRF protection** for easier testing
- **Debug mode enabled** for detailed error messages
- **Sample test data** for consistent testing

## Test Data

The testing suite includes predefined test data:

### Test Users
- `testuser1` / `testpass123`
- `testuser2` / `testpass456`
- `admin` / `adminpass123`

### Test Categories
- Income: Salary, Freelance
- Expense: Food, Transport, Entertainment, Bills

### Test Transactions
- Sample income and expense transactions
- Various amounts and dates
- Different categories

## Running Tests with Coverage

To run tests with code coverage analysis:

```bash
python run_tests.py --coverage
```

This will:
1. Run all tests
2. Generate a coverage report in the terminal
3. Create an HTML coverage report in the `htmlcov/` directory

## Test Reports

### Basic Test Report
```bash
python run_tests.py --report
```

Generates a JSON report with:
- Database statistics
- Test configuration status
- Timestamp and environment info

### Coverage Report
The coverage report shows:
- Line coverage percentage
- Branch coverage percentage
- Uncovered lines and branches
- HTML report for detailed analysis

## Continuous Integration

### GitHub Actions (Recommended)
Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python run_tests.py
    
    - name: Generate coverage report
      run: |
        python run_tests.py --coverage
```

### Local CI Setup
For local continuous integration:

```bash
# Create a test script
echo '#!/bin/bash
python run_tests.py
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi' > test_ci.sh

chmod +x test_ci.sh
```

## Debugging Tests

### Common Issues

1. **Database Connection Errors**
   - Ensure SQLite is available
   - Check file permissions
   - Verify database path

2. **Import Errors**
   - Check Python path
   - Verify module structure
   - Install missing dependencies

3. **Test Data Issues**
   - Reset test database
   - Check test data consistency
   - Verify model relationships

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In test_config.py
DEBUG = True
LOG_LEVEL = 'DEBUG'
```

### Manual Testing

For manual testing during development:

```python
from test_utils import create_test_client

# Create test client with data
client, app, users, categories = create_test_client()

# Test specific functionality
response = client.get('/dashboard')
print(response.status_code)
print(response.get_data(as_text=True))
```

## Best Practices

### Writing Tests

1. **Test Isolation**: Each test should be independent
2. **Clear Naming**: Use descriptive test method names
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Test Data**: Use consistent, realistic test data
5. **Error Cases**: Test both success and failure scenarios

### Test Maintenance

1. **Regular Updates**: Keep tests updated with code changes
2. **Coverage Goals**: Aim for >80% code coverage
3. **Performance**: Keep tests fast and efficient
4. **Documentation**: Document complex test scenarios

### Pre-deployment Checklist

- [ ] All tests pass
- [ ] Coverage report generated
- [ ] No critical issues in test results
- [ ] Test data cleaned up
- [ ] Documentation updated

## Troubleshooting

### Test Failures

1. **Check test output** for specific error messages
2. **Verify test data** is properly set up
3. **Check database state** before and after tests
4. **Review recent changes** that might affect tests

### Performance Issues

1. **Use in-memory database** for faster tests
2. **Minimize database operations** in tests
3. **Use test fixtures** for common setup
4. **Parallel test execution** for large test suites

### Environment Issues

1. **Check Python version** compatibility
2. **Verify dependency versions** match requirements
3. **Check file permissions** for database files
4. **Review environment variables** configuration

## Support

For testing-related issues:

1. Check this documentation
2. Review test output and error messages
3. Check the test configuration
4. Verify the application code changes
5. Consult the main application documentation

## Contributing

When adding new features:

1. **Write tests first** (TDD approach)
2. **Update test data** if needed
3. **Add test categories** for new functionality
4. **Update documentation** with new test procedures
5. **Ensure all tests pass** before merging

---

**Last Updated**: January 2024
**Test Suite Version**: 1.0.0 