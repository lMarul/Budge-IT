# Budget-IT

A comprehensive budget tracking application built with Flask and SQLAlchemy, featuring user authentication, transaction management, and financial analytics.

## Features

- **User Authentication**: Secure login and registration system
- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Category Management**: Custom categories with color coding
- **Financial Analytics**: Interactive charts and summary statistics
- **Admin Panel**: User management and system administration
- **Responsive Design**: Modern UI with dark mode support

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Authentication**: Flask-Login
- **Deployment**: Render

## Local Development

### Prerequisites

- Python 3.8+
- PostgreSQL database (local or Supabase)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lMarul/Budget-IT.git
   cd Budget-IT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open http://localhost:5001 in your browser

## Deployment on Render

### Prerequisites

- Render account
- Supabase database (or any PostgreSQL database)

### Deployment Steps

1. **Fork/Clone this repository** to your GitHub account

2. **Create a new Web Service** on Render:
   - Connect your GitHub repository
   - Choose "Python" as the environment
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`

3. **Configure Environment Variables** in Render:
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `0`

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Environment Variables for Production

```bash
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=0
```

### Supabase Database Setup

1. Create a new project on Supabase
2. Get your database connection string from Settings > Database
3. Update the `DATABASE_URL` environment variable in Render

## Project Structure

```
Budget-IT/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment config
├── Procfile            # Alternative deployment config
├── database/           # Database models and utilities
│   ├── models.py       # SQLAlchemy models
│   └── utils.py        # Database utilities
├── routes/             # Flask route blueprints
│   ├── auth.py         # Authentication routes
│   ├── main.py         # Main application routes
│   └── admin.py        # Admin panel routes
├── templates/          # HTML templates
├── static/            # CSS, JS, and images
└── scripts/           # Utility scripts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on GitHub.

## 🎯 Features

### User Features
- ✅ **Secure Authentication** - Registration, login, and session management
- ✅ **Dashboard** - Financial overview with interactive charts
- ✅ **Transaction Management** - Add, edit, and delete income/expenses
- ✅ **Category Management** - Customizable categories with color coding
- ✅ **Transaction History** - Comprehensive history with filtering
- ✅ **Dark/Light Mode** - User preference for interface theme
- ✅ **Responsive Design** - Works on desktop and mobile devices

### Admin Features
- ✅ **User Management** - View, edit, and delete user accounts
- ✅ **Database Viewer** - Excel-like interface for data browsing
- ✅ **System Statistics** - Overview of all system data
- ✅ **Secure Access** - Admin-only routes with proper authentication

### Technical Features
- ✅ **Real-time Updates** - AJAX-based smooth interactions
- ✅ **Data Validation** - Client-side and server-side validation
- ✅ **Error Handling** - Proper error pages and logging
- ✅ **Security** - Password hashing, session management, CSRF protection

## 🏗️ Architecture

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
    ├── PROJECT_OVERVIEW.md
    ├── API_DOCUMENTATION.md
    └── README_*.md
```

## 🔧 Configuration

The application supports multiple environments through configuration classes:

### Development
```python
# Default configuration with debug mode enabled
DEBUG = True
HOST = '127.0.0.1'
PORT = 5001
```

### Production
```python
# Production configuration with security settings
DEBUG = False
HOST = '0.0.0.0'
PORT = 5001
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### Environment Variables
- `SECRET_KEY` - Flask secret key for session management
- `PORT` - Application port (default: 5001)

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

### Dark Mode Support
- Automatic theme detection
- User preference persistence
- Consistent styling across all components

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and authentication
- [ ] Transaction creation and management
- [ ] Category management
- [ ] Admin functionality
- [ ] Responsive design on different devices
- [ ] Dark/light mode toggle
- [ ] Error handling and validation

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

## 📚 Documentation

- **[Project Overview](docs/PROJECT_OVERVIEW.md)** - Comprehensive project documentation
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Data Flow](data_flow.txt)** - Detailed data flow analysis
- **[Architecture](docs/README_OPTIMIZED.md)** - System architecture details

## 👥 Development Team

- **Project Lead**: Maru
- **Backend Developer**: Vince
- **Frontend Developer**: Marwin
- **UI/UX Designer**: Nika
- **Quality Assurance**: Anthony
- **Documentation**: Vinz

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in config.py or use different port
   python app.py --port 5002
   ```

2. **Database file not found**
   - The application will create the database file automatically
   - Check file permissions in the project directory

3. **Import errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Getting Help

1. Check the application logs for detailed error messages
2. Review the data flow documentation in `data_flow.txt`
3. Contact the development team through the contact page

## 📄 License

This project is developed for educational purposes as part of a Data Structures course project.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

*Last updated: December 2024*
