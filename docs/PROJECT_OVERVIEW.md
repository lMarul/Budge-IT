# Budget Tracker System - Project Overview

## 🎯 Project Description

The Budget Tracker System is a comprehensive Flask-based web application designed to help users manage their personal finances. It provides an intuitive interface for tracking income and expenses, managing categories, and visualizing financial data through interactive charts.

## 🏗️ System Architecture

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Database**: JSON-based file storage
- **Charts**: Chart.js for data visualization
- **Authentication**: Session-based with password hashing

### Architecture Pattern
- **MVC Pattern**: Model-View-Controller separation
- **Blueprint Architecture**: Modular route organization
- **Template Inheritance**: Consistent UI with base templates
- **RESTful Design**: Clean URL structure and HTTP methods

## 📁 Project Structure

```
budget-tracker/
├── app.py                 # Main application entry point
├── config.py             # Configuration management
├── models.py             # Data models and business logic
├── utils.py              # Utility functions and helpers
├── decorators.py         # Authentication decorators
├── requirements.txt      # Python dependencies
├── budget_tracker.json   # JSON database file
├── data_flow.txt         # Data flow documentation
├── routes/               # Flask blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── main.py          # Main application routes
│   └── admin.py         # Admin functionality routes
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── admin_functions/ # Admin-specific templates
│   └── members/         # Team member profiles
├── static/              # Static assets (images, CSS, JS)
└── docs/               # Documentation
```

## 🚀 Key Features

### User Features
- **User Authentication**: Secure registration and login
- **Dashboard**: Financial overview with charts and statistics
- **Transaction Management**: Add, edit, and delete income/expenses
- **Category Management**: Customizable categories with color coding
- **Transaction History**: Comprehensive history with filtering
- **Account Settings**: User profile management
- **Dark/Light Mode**: User preference for interface theme

### Admin Features
- **User Management**: View, edit, and delete user accounts
- **Database Viewer**: Excel-like interface for data browsing
- **System Statistics**: Overview of all system data
- **Secure Access**: Admin-only routes with proper authentication

### Technical Features
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: AJAX-based smooth interactions
- **Data Validation**: Client-side and server-side validation
- **Error Handling**: Proper error pages and logging
- **Security**: Password hashing, session management, CSRF protection

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget-tracker
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Main app: http://127.0.0.1:5001
   - Admin access: Login with username `admin`

## 🔐 Security Features

- **Password Hashing**: Using Werkzeug's security functions
- **Session Management**: Secure session handling
- **Route Protection**: Authentication and authorization decorators
- **Input Validation**: Protection against malicious input
- **CSRF Protection**: Form submission security
- **Data Isolation**: Users can only access their own data

## 📊 Data Flow

The application follows a clear data flow pattern:

1. **User Input** → HTML forms and AJAX requests
2. **Route Processing** → Flask routes handle requests
3. **Business Logic** → Models process data and apply rules
4. **Data Storage** → JSON file persistence
5. **Response** → HTML templates or JSON responses

For detailed data flow documentation, see `data_flow.txt`.

## 🎨 UI/UX Design

### Design Principles
- **Clean & Modern**: Minimalist design with clear hierarchy
- **Responsive**: Mobile-first approach with responsive breakpoints
- **Accessible**: Proper contrast ratios and keyboard navigation
- **Consistent**: Unified design language across all pages

### Color Scheme
- **Primary**: Blue (#3B82F6)
- **Success**: Green (#10B981)
- **Warning**: Yellow (#F59E0B)
- **Error**: Red (#EF4444)
- **Neutral**: Gray scale (#6B7280)

### Dark Mode Support
- Automatic theme detection
- User preference persistence
- Consistent styling across all components

## 🔄 Development Workflow

### Code Organization
- **Blueprints**: Routes organized by functionality
- **Models**: Business logic separated from routes
- **Templates**: Reusable components with inheritance
- **Static Assets**: Organized by type and purpose

### Best Practices
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful error handling with user feedback
- **Validation**: Both client-side and server-side validation
- **Security**: Input sanitization and output encoding

## 🧪 Testing Strategy

### Manual Testing
- User registration and authentication
- Transaction creation and management
- Category management
- Admin functionality
- Responsive design on different devices

### Automated Testing (Future)
- Unit tests for models and utilities
- Integration tests for routes
- Frontend testing with JavaScript
- Performance testing

## 🚀 Deployment

### Development Environment
- Local Flask development server
- Debug mode enabled
- Detailed error messages

### Production Environment
- WSGI server (Gunicorn recommended)
- Debug mode disabled
- Environment variables for configuration
- Proper logging and monitoring

## 📈 Future Enhancements

### Planned Features
- **Export Functionality**: PDF and Excel export
- **Budget Goals**: Set and track financial goals
- **Recurring Transactions**: Automatic transaction creation
- **Multi-currency Support**: International currency handling
- **Mobile App**: Native mobile application
- **API Integration**: Third-party bank integration

### Technical Improvements
- **Database Migration**: SQLite or PostgreSQL
- **Caching**: Redis for performance optimization
- **Background Tasks**: Celery for async processing
- **Monitoring**: Application performance monitoring
- **CI/CD**: Automated testing and deployment

## 👥 Team Information

### Development Team
- **Project Lead**: Maru
- **Backend Developer**: Vince
- **Frontend Developer**: Marwin
- **UI/UX Designer**: Nika
- **Quality Assurance**: Anthony
- **Documentation**: Vinz

### Contact Information
For support or questions, please visit the contact page or reach out to the development team.

## 📄 License

This project is developed for educational purposes as part of a Data Structures course project.

---

*Last updated: December 2024* 