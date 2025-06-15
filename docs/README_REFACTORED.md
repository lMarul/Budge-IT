# Budget Tracker - Refactored Structure

This is a Flask-based budget tracking application with admin functionality, organized using a modular structure for better maintainability and scalability.

## Project Structure

```
budget-tracker/
├── app_new.py              # Main application entry point
├── config.py               # Configuration settings
├── utils.py                # Database utilities and helper functions
├── auth.py                 # Authentication decorators and helpers
├── models.py               # Data models (User, Category, Transaction)
├── requirements.txt        # Python dependencies
├── budget_tracker.json     # JSON database file
├── routes/                 # Route blueprints
│   ├── __init__.py
│   ├── auth.py            # Authentication routes (login, register, logout)
│   ├── main.py            # Main application routes (dashboard, transactions, etc.)
│   └── admin.py           # Admin routes (user management, database view)
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
│   └── ... (other templates)
└── static/                # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

## Key Improvements

### 1. **Modular Architecture**
- **Separation of Concerns**: Each module has a specific responsibility
- **Blueprints**: Routes are organized into logical blueprints
- **Models**: Data operations are centralized in model classes

### 2. **Better Code Organization**
- **`utils.py`**: Database operations, Jinja2 filters, and utility functions
- **`auth.py`**: Authentication decorators and helper functions
- **`models.py`**: User, Category, and Transaction models with CRUD operations
- **`routes/`**: Organized route blueprints by functionality

### 3. **Configuration Management**
- **`config.py`**: Centralized configuration for different environments
- **Environment-based settings**: Development, Production, and Testing configs

### 4. **Improved Maintainability**
- **Single Responsibility**: Each function/class has one clear purpose
- **Reusability**: Common operations are abstracted into reusable functions
- **Testability**: Modular structure makes unit testing easier

## Features

### User Features
- User registration and authentication
- Dashboard with financial overview
- Income and expense tracking
- Transaction history with editing capabilities
- Category management
- Account statistics
- Responsive design with dark mode support

### Admin Features
- Admin dashboard with system statistics
- User management (view, edit, delete users)
- Database viewing in JSON format
- Secure admin-only access

## Installation and Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app_new.py
   ```

3. **Access the application**:
   - Main application: http://127.0.0.1:5001
   - Admin access: Login with username `admin` and password `admin123`

## Database

The application uses a JSON-based database (`budget_tracker.json`) for simplicity. The database structure includes:

- **Users**: User accounts with authentication
- **Categories**: Income and expense categories
- **Transactions**: Financial transactions with category associations

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Admin-only access control
- CSRF protection (can be enhanced)

## Future Enhancements

This modular structure makes it easy to add:

1. **Database Migration**: Switch to SQLAlchemy with PostgreSQL/MySQL
2. **API Endpoints**: Add RESTful API for mobile apps
3. **Advanced Features**: Budget goals, recurring transactions, reports
4. **Testing**: Comprehensive unit and integration tests
5. **Deployment**: Docker containerization and cloud deployment

## Migration from Old Structure

To migrate from the old `app.py`:

1. Backup your `budget_tracker.json` file
2. Replace `app.py` with `app_new.py`
3. Ensure all new modules are in place
4. Test the application thoroughly

The new structure maintains all existing functionality while providing a solid foundation for future development. 