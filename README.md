# Budge-IT: Personal Budget Tracker

A comprehensive personal budget tracking application built with Flask and SQLAlchemy, featuring user authentication, transaction management, and financial analytics. Deployed on Vercel with Supabase database.

## 🚀 Features

- **User Authentication**: Secure login/registration system
- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Category Management**: Customizable categories with color coding
- **Financial Analytics**: Charts and reports for spending analysis
- **Admin Dashboard**: User management and system overview
- **Responsive Design**: Mobile-friendly interface
- **Cloud Database**: Real-time sync with Supabase PostgreSQL

## 🏗️ Project Structure

```
├── app/                        # Main application package
│   ├── __init__.py            # App factory with database config
│   ├── decorators.py          # Authentication decorators
│   ├── models/                # Database models
│   │   └── __init__.py        # SQLAlchemy models
│   ├── routes/                # Application routes
│   │   ├── __init__.py        # Routes package
│   │   ├── auth.py            # Authentication routes
│   │   ├── main.py            # Main application routes
│   │   └── admin.py           # Admin dashboard routes
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py        # Utils package
│   │   └── database.py        # Database utility functions
│   ├── templates/             # HTML templates
│   └── static/                # CSS, JS, and static assets
├── scripts/                   # Utility scripts
├── tests/                     # Test files
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── vercel.json                # Vercel deployment config
├── wsgi.py                    # Production WSGI entry point
├── supabase_schema.sql        # Database schema for Supabase
├── env_template.txt           # Environment variables template
└── README.md                  # Project documentation
```

## 👥 Team Members

- **Anthony**: Application factory, configuration, and deployment setup
- **Marwin**: SQLAlchemy models and database schema
- **Vince**: Database utilities, main routes, and core functionality

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Flask-Login 0.6.3
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Deployment**: Vercel, Supabase

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
   # Copy the template
   cp env_template.txt .env
   # Edit .env with your Supabase database URL
   ```

4. **Run the application**
   ```bash
   python wsgi.py
   ```

## 🌐 Deployment

### Vercel + Supabase Deployment (Recommended)

This project is optimized for deployment on Vercel with Supabase database.

1. **Follow the complete deployment guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
2. **Quick start**:
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel
   ```

### Database Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Get your database connection string from Supabase dashboard
3. Set the `DATABASE_URL` environment variable in Vercel
4. The app will automatically create tables on first run

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Vercel + Supabase Deployment Guide](VERCEL_DEPLOYMENT.md)

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Creating Sample Data
```bash
python scripts/create_sample_data.py
```

### Database Connection Test
```bash
python test_database_connection.py
```

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

3. **Set up Supabase**:
   - Create a Supabase project
   - Get your database URL
   - Add `DATABASE_URL` to Vercel environment variables

4. **Access your app** at the provided URL!

For detailed instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

## 🔗 Live Demo

Once deployed, your app will be available at:
- **Vercel URL**: `https://your-project-name.vercel.app`
- **Database**: Supabase dashboard for data management

## 🛡️ Security

- Environment variables for all sensitive data
- SQLAlchemy ORM for secure database operations
- Flask-Login for session management
- Supabase Row Level Security (RLS) policies
