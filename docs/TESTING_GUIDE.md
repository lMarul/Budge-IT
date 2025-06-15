# Budget Tracker System - Testing Guide

## Overview

This guide provides comprehensive testing strategies for the Budget Tracker System, covering manual testing, automated testing, and quality assurance procedures.

## 🧪 Testing Strategy

### Testing Pyramid
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Manual Testing**: User acceptance testing

## 📋 Manual Testing Checklist

### Authentication Testing

#### User Registration
- [ ] **Valid Registration**
  - [ ] Register with valid username, email, and password
  - [ ] Verify user is created in database
  - [ ] Verify default categories are created
  - [ ] Verify redirect to login page

- [ ] **Invalid Registration**
  - [ ] Try registering with existing username
  - [ ] Try registering with invalid email format
  - [ ] Try registering with short password (< 6 characters)
  - [ ] Try registering with mismatched passwords
  - [ ] Verify appropriate error messages

#### User Login
- [ ] **Valid Login**
  - [ ] Login with correct username and password
  - [ ] Verify session is created
  - [ ] Verify redirect to dashboard
  - [ ] Verify user data is accessible

- [ ] **Invalid Login**
  - [ ] Try logging in with incorrect password
  - [ ] Try logging in with non-existent username
  - [ ] Try logging in with empty fields
  - [ ] Verify appropriate error messages

#### User Logout
- [ ] **Logout Functionality**
  - [ ] Click logout button
  - [ ] Verify session is destroyed
  - [ ] Verify redirect to login page
  - [ ] Verify dark mode preference is cleared

### Dashboard Testing

#### Dashboard Display
- [ ] **Dashboard Load**
  - [ ] Verify dashboard loads after login
  - [ ] Verify user-specific data is displayed
  - [ ] Verify charts render correctly
  - [ ] Verify navigation menu is present

#### Chart Functionality
- [ ] **Income Chart**
  - [ ] Verify income data is displayed correctly
  - [ ] Verify chart updates when new income is added
  - [ ] Verify chart colors match category colors

- [ ] **Expense Chart**
  - [ ] Verify expense data is displayed correctly
  - [ ] Verify chart updates when new expense is added
  - [ ] Verify chart colors match category colors

#### Quick Actions
- [ ] **Add Income Button**
  - [ ] Click "Add Income" button
  - [ ] Verify redirect to income page
  - [ ] Verify form is pre-filled correctly

- [ ] **Add Expense Button**
  - [ ] Click "Add Expense" button
  - [ ] Verify redirect to expense page
  - [ ] Verify form is pre-filled correctly

### Transaction Management Testing

#### Adding Transactions
- [ ] **Add Income**
  - [ ] Fill out income form with valid data
  - [ ] Submit form
  - [ ] Verify transaction is created
  - [ ] Verify redirect to income page
  - [ ] Verify success message

- [ ] **Add Expense**
  - [ ] Fill out expense form with valid data
  - [ ] Submit form
  - [ ] Verify transaction is created
  - [ ] Verify redirect to expense page
  - [ ] Verify success message

#### Transaction Validation
- [ ] **Amount Validation**
  - [ ] Try submitting with negative amount
  - [ ] Try submitting with zero amount
  - [ ] Try submitting with non-numeric amount
  - [ ] Verify appropriate error messages

- [ ] **Date Validation**
  - [ ] Try submitting with future date
  - [ ] Try submitting with invalid date format
  - [ ] Verify appropriate error messages

- [ ] **Category Validation**
  - [ ] Try submitting without selecting category
  - [ ] Try submitting with invalid category
  - [ ] Verify appropriate error messages

#### Editing Transactions
- [ ] **Edit Transaction**
  - [ ] Navigate to transaction history
  - [ ] Click edit button on a transaction
  - [ ] Modify transaction details
  - [ ] Submit changes
  - [ ] Verify transaction is updated
  - [ ] Verify success message

#### Deleting Transactions
- [ ] **Delete Transaction**
  - [ ] Navigate to transaction history
  - [ ] Click delete button on a transaction
  - [ ] Confirm deletion
  - [ ] Verify transaction is removed
  - [ ] Verify success message

### Category Management Testing

#### Adding Categories
- [ ] **Add Income Category**
  - [ ] Navigate to categories page
  - [ ] Fill out category form for income
  - [ ] Select color
  - [ ] Submit form
  - [ ] Verify category is created
  - [ ] Verify category appears in income form

- [ ] **Add Expense Category**
  - [ ] Navigate to categories page
  - [ ] Fill out category form for expense
  - [ ] Select color
  - [ ] Submit form
  - [ ] Verify category is created
  - [ ] Verify category appears in expense form

#### Category Validation
- [ ] **Name Validation**
  - [ ] Try adding category with empty name
  - [ ] Try adding category with duplicate name
  - [ ] Try adding category with very long name
  - [ ] Verify appropriate error messages

- [ ] **Color Validation**
  - [ ] Try adding category without color
  - [ ] Try adding category with invalid color format
  - [ ] Verify appropriate error messages

#### Editing Categories
- [ ] **Edit Category**
  - [ ] Click edit button on a category
  - [ ] Modify category name and color
  - [ ] Submit changes
  - [ ] Verify category is updated
  - [ ] Verify related transactions show updated category

#### Deleting Categories
- [ ] **Delete Category**
  - [ ] Click delete button on a category
  - [ ] Confirm deletion
  - [ ] Verify category is removed
  - [ ] Verify related transactions are updated

### Admin Functionality Testing

#### Admin Access
- [ ] **Admin Login**
  - [ ] Login with admin credentials
  - [ ] Verify admin dashboard is accessible
  - [ ] Verify admin menu is present

- [ ] **Non-Admin Access**
  - [ ] Try accessing admin routes as regular user
  - [ ] Verify access is denied
  - [ ] Verify appropriate error message

#### User Management
- [ ] **View Users**
  - [ ] Navigate to user management
  - [ ] Verify all users are listed
  - [ ] Verify user details are correct

- [ ] **Edit User**
  - [ ] Click edit button on a user
  - [ ] Modify user details
  - [ ] Submit changes
  - [ ] Verify user is updated

- [ ] **Delete User**
  - [ ] Click delete button on a user
  - [ ] Confirm deletion
  - [ ] Verify user and related data are removed

#### Database Viewer
- [ ] **View Database**
  - [ ] Navigate to database viewer
  - [ ] Verify all tables are accessible
  - [ ] Verify data is displayed correctly
  - [ ] Verify search functionality works

### UI/UX Testing

#### Responsive Design
- [ ] **Desktop Testing**
  - [ ] Test on desktop browsers (Chrome, Firefox, Safari, Edge)
  - [ ] Verify layout is correct
  - [ ] Verify all functionality works

- [ ] **Mobile Testing**
  - [ ] Test on mobile devices
  - [ ] Test on tablets
  - [ ] Verify responsive layout
  - [ ] Verify touch interactions work

- [ ] **Browser Compatibility**
  - [ ] Test on different browsers
  - [ ] Test on different browser versions
  - [ ] Verify consistent behavior

#### Dark Mode Testing
- [ ] **Dark Mode Toggle**
  - [ ] Toggle dark mode on/off
  - [ ] Verify theme changes immediately
  - [ ] Verify theme persists across page reloads
  - [ ] Verify theme is cleared on logout

- [ ] **Dark Mode Styling**
  - [ ] Verify all elements have dark mode styles
  - [ ] Verify text is readable in dark mode
  - [ ] Verify colors are appropriate for dark mode

#### Accessibility Testing
- [ ] **Keyboard Navigation**
  - [ ] Navigate using only keyboard
  - [ ] Verify all interactive elements are accessible
  - [ ] Verify focus indicators are visible

- [ ] **Screen Reader Compatibility**
  - [ ] Test with screen reader software
  - [ ] Verify all content is announced correctly
  - [ ] Verify form labels are associated correctly

### Performance Testing

#### Load Testing
- [ ] **Page Load Times**
  - [ ] Measure dashboard load time
  - [ ] Measure transaction history load time
  - [ ] Measure chart rendering time
  - [ ] Verify times are acceptable (< 3 seconds)

- [ ] **Database Performance**
  - [ ] Test with large number of transactions
  - [ ] Test with large number of categories
  - [ ] Verify queries are optimized

#### Memory Usage
- [ ] **Memory Leaks**
  - [ ] Monitor memory usage during extended use
  - [ ] Verify no memory leaks occur
  - [ ] Verify garbage collection works properly

### Security Testing

#### Input Validation
- [ ] **SQL Injection**
  - [ ] Try SQL injection in form fields
  - [ ] Verify inputs are properly sanitized
  - [ ] Verify no database errors occur

- [ ] **XSS Prevention**
  - [ ] Try XSS attacks in form fields
  - [ ] Verify scripts are not executed
  - [ ] Verify output is properly escaped

#### Authentication Security
- [ ] **Session Management**
  - [ ] Test session timeout
  - [ ] Test session hijacking prevention
  - [ ] Verify secure session handling

- [ ] **Password Security**
  - [ ] Verify passwords are hashed
  - [ ] Test password strength requirements
  - [ ] Verify password reset functionality

## 🤖 Automated Testing

### Unit Testing Setup

#### Install Testing Dependencies
```bash
pip install pytest pytest-flask pytest-cov
```

#### Test Structure
```
tests/
├── __init__.py
├── conftest.py
├── test_models.py
├── test_routes.py
├── test_utils.py
└── test_integration.py
```

#### Example Unit Test
```python
import pytest
from models import User, Category, Transaction

def test_user_creation():
    user = User.create("testuser", "test@example.com", "password123")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.verify_password("password123")

def test_category_creation():
    user = User.create("testuser", "test@example.com", "password123")
    category = Category.create(user.id, "Salary", "income", "#28a745")
    assert category.name == "Salary"
    assert category.type == "income"
    assert category.color == "#28a745"
```

### Integration Testing

#### Flask Test Client
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_route(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin'
    })
    assert response.status_code == 302  # Redirect after login
```

### End-to-End Testing

#### Selenium Testing
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_user_registration():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:5001/register")
        
        # Fill registration form
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirm_password").send_keys("password123")
        
        # Submit form
        driver.find_element(By.TAG_NAME, "form").submit()
        
        # Verify redirect to login
        assert "login" in driver.current_url
    finally:
        driver.quit()
```

## 📊 Test Reporting

### Coverage Reporting
```bash
# Run tests with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Results
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run tests with verbose output
pytest -v

# Run tests and show print statements
pytest -s
```

## 🔄 Continuous Integration

### GitHub Actions Workflow
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
        pip install pytest pytest-flask pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 🐛 Bug Reporting

### Bug Report Template
```
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- Browser: [e.g. Chrome, Firefox]
- Version: [e.g. 22]
- OS: [e.g. Windows, macOS, Linux]

**Screenshots**
If applicable, add screenshots

**Additional Context**
Any other context about the problem
```

## 📈 Quality Metrics

### Code Quality
- **Test Coverage**: Aim for >80% coverage
- **Code Complexity**: Keep functions simple
- **Documentation**: All functions documented
- **Code Style**: Follow PEP 8 guidelines

### Performance Metrics
- **Page Load Time**: < 3 seconds
- **Database Query Time**: < 100ms
- **Memory Usage**: Stable over time
- **Error Rate**: < 1%

## 🎯 Testing Best Practices

### Test Design
- Write tests before or alongside code (TDD)
- Keep tests independent and isolated
- Use descriptive test names
- Test both positive and negative cases
- Mock external dependencies

### Test Maintenance
- Update tests when code changes
- Remove obsolete tests
- Keep test data clean and minimal
- Use fixtures for common setup

### Test Execution
- Run tests frequently during development
- Run full test suite before deployment
- Monitor test execution time
- Investigate failing tests immediately

---

*Last updated: December 2024* 