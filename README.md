# Budge-IT: Personal Budget Tracker

A comprehensive personal budget tracking application built with Flask and SQLAlchemy, featuring user authentication, transaction management, and financial analytics.

## 🚀 Features

- **User Authentication**: Secure login/registration system
- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Category Management**: Customizable categories with color coding
- **Financial Analytics**: Charts and reports for spending analysis
- **Admin Dashboard**: User management and system overview
- **Responsive Design**: Mobile-friendly interface

## 🏗️ Project Structure

```
├── app.py                 # Main Flask application factory
├── wsgi.py               # Production WSGI entry point
├── config.py             # Configuration settings
├── decorators.py         # Authentication decorators
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version specification
├── render.yaml           # Render deployment configuration
├── Procfile             # Heroku deployment configuration
├── setup.py             # Package configuration
├── build.sh             # Build script
├── database/            # Database models and utilities
│   ├── models.py        # SQLAlchemy models
│   └── utils.py         # Database utility functions
├── routes/              # Application routes
│   ├── auth.py          # Authentication routes
│   ├── main.py          # Main application routes
│   └── admin.py         # Admin dashboard routes
├── templates/           # HTML templates
├── static/              # CSS, JS, and static assets
├── scripts/             # Utility scripts
│   ├── create_sample_data.py
│   └── test_database.py
├── docs/                # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── PROJECT_OVERVIEW.md
│   └── TESTING_GUIDE.md
└── config/              # Configuration files
```

## 👥 Team Members

- **Anthony**: Application factory, configuration, and deployment setup
- **Marwin**: SQLAlchemy models and database schema
- **Vince**: Database utilities, main routes, and core functionality

## 🛠️ Technology Stack

- **Backend**: Flask 2.0.3, SQLAlchemy 1.4.53
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Flask-Login 0.5.0
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Deployment**: Render, Gunicorn 20.1.0

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lMarul/Budge-IT.git
   cd Budge-IT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import create_app; from database.utils import initialize_database; app = create_app(); initialize_database(app)"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 🌐 Deployment

### Render Deployment

1. **Connect your GitHub repository to Render**
2. **Set environment variables**:
   - `SECRET_KEY`: Your Flask secret key
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `FLASK_ENV`: production
   - `FLASK_APP`: wsgi.py

3. **Deploy**: Render will automatically deploy using the configuration in `render.yaml`

### Database Setup

1. Create a Supabase project
2. Run the SQL schema from `supabase_schema.sql`
3. Configure Row Level Security (RLS) policies
4. Set the `DATABASE_URL` environment variable

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Deployment Setup](DEPLOYMENT_SETUP.md)

## 🔧 Development

### Running Tests
```bash
python scripts/test_database.py
```

### Creating Sample Data
```bash
python scripts/create_sample_data.py
```

### Database Migration
The application automatically migrates from JSON to SQLAlchemy on first run.

## 📄 License

This project is part of a Data Structures course assignment.

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the development team.
