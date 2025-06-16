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
├── app/                        # Main application package
│   ├── __init__.py            # App factory
│   ├── config.py              # Configuration settings
│   ├── decorators.py          # Authentication decorators
│   ├── models/                # Database models
│   │   └── __init__.py        # SQLAlchemy models
│   ├── routes/                # Application routes
│   │   ├── __init__.py        # Routes package
│   │   ├── auth.py            # Authentication routes
│   │   ├── main.py            # Main application routes
│   │   └── admin.py           # Admin dashboard routes
│   └── utils/                 # Utility functions
│       ├── __init__.py        # Utils package
│       └── database.py        # Database utility functions
├── deployment/                # Deployment configuration
│   ├── nhost.yaml             # Nhost deployment config
│   ├── nhost.env.example      # Nhost environment template
│   ├── NHOST_DEPLOYMENT.md    # Nhost deployment guide
│   └── supabase_schema.sql    # Database schema
├── migrations/                # Database migrations
├── templates/                 # HTML templates
├── static/                    # CSS, JS, and static assets
├── scripts/                   # Utility scripts
├── tests/                     # Test files
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version specification
├── Dockerfile                 # Docker configuration
├── .dockerignore              # Docker ignore file
├── vercel.json                # Vercel deployment config
├── wsgi.py                    # Production WSGI entry point
└── README.md                  # Project documentation
```

## 👥 Team Members

- **Anthony**: Application factory, configuration, and deployment setup
- **Marwin**: SQLAlchemy models and database schema
- **Vince**: Database utilities, main routes, and core functionality

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Database**: PostgreSQL (Supabase/Nhost)
- **Authentication**: Flask-Login 0.6.3
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Deployment**: Vercel, Nhost, Gunicorn 21.2.0

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
   cp deployment/nhost.env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import create_app; from app.utils.database import initialize_database; app = create_app(); initialize_database(app)"
   ```

5. **Run the application**
   ```bash
   python wsgi.py
   ```

## 🌐 Deployment

### Vercel Deployment (Recommended)

Vercel provides fast, reliable deployment with automatic scaling and global CDN.

1. **Follow the Vercel deployment guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
2. **Quick start**:
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel
   ```

### Nhost Deployment

Nhost provides a complete backend-as-a-service platform with PostgreSQL, authentication, and file storage.

1. **Follow the Nhost deployment guide**: [deployment/NHOST_DEPLOYMENT.md](deployment/NHOST_DEPLOYMENT.md)
2. **Quick start**:
   ```bash
   npm install -g nhost
   nhost login
   nhost init budge-it
   nhost up
   ```

### Database Setup

1. Create a PostgreSQL database (Supabase recommended)
2. Run the SQL schema from `deployment/supabase_schema.sql`
3. Configure Row Level Security (RLS) policies if needed
4. Set the `DATABASE_URL` environment variable

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Vercel Deployment Guide](VERCEL_DEPLOYMENT.md)
- [Nhost Deployment Guide](deployment/NHOST_DEPLOYMENT.md)

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Creating Sample Data
```bash
python scripts/create_sample_data.py
```

### Database Migration
The application automatically migrates from JSON to SQLAlchemy on first run.

### Health Check
Your application includes a health check endpoint at `/health` for deployment monitoring.

## 📄 License

This project is part of a Data Structures course assignment.

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the development team.

## 🚀 Quick Deploy

### Deploy to Vercel in 3 minutes:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Access your app** at the provided URL!

### Deploy to Nhost in 5 minutes:

1. **Install Nhost CLI**:
   ```bash
   npm install -g nhost
   ```

2. **Deploy**:
   ```bash
   nhost login
   nhost init budge-it
   nhost up
   ```

3. **Access your app** at the provided URL!

For detailed instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) or [deployment/NHOST_DEPLOYMENT.md](deployment/NHOST_DEPLOYMENT.md).
