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

### Environment Variables
**IMPORTANT**: Never commit sensitive information to your repository!

1. **Create a `.env` file** (not tracked by git):
   ```env
   # Copy from env.example and fill in your actual values
   SECRET_KEY=your-super-secure-secret-key-here
   DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@[YOUR_HOST]:5432/postgres
   DEBUG=False
   ```

2. **Generate a secure SECRET_KEY**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Get your Supabase DATABASE_URL**:
   - Go to your Supabase project dashboard
   - Navigate to Settings > Database
   - Copy the connection string

### Security Features
- ✅ **Environment variables** for all sensitive data
- ✅ **Secure secret key generation** using `os.urandom()`
- ✅ **SQLAlchemy ORM** for secure database operations
- ✅ **Flask-Login** for session management
- ✅ **Supabase Row Level Security (RLS)** policies
- ✅ **No hardcoded passwords** in source code
- ✅ **Automatic fallback** to SQLite for development

### Production Security Checklist
- [ ] Set `SECRET_KEY` environment variable
- [ ] Set `DATABASE_URL` environment variable
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS in production
- [ ] Regularly rotate secret keys
- [ ] Monitor application logs
- [ ] Keep dependencies updated

### What's Secured
- ✅ **Database passwords** - stored in environment variables
- ✅ **Flask secret keys** - auto-generated if not provided
- ✅ **Connection strings** - no hardcoded values
- ✅ **Debug information** - disabled in production
- ✅ **Session data** - encrypted with secure keys

## 🚀 Live Deployment

**Application URL**: https://budge-it-j4bp.onrender.com

## 🔧 Deployment Status & Troubleshooting

### Current Issues & Solutions

#### 1. Supabase Connection Limits
**Issue**: "Max client connections reached" error
**Status**: Your data is safe in Supabase! This is a connection limit issue, not a data loss issue.

**Solutions**:
- **Wait**: Connection limits reset automatically (usually within 15-30 minutes)
- **Upgrade**: Consider upgrading your Supabase plan for higher connection limits
- **Monitor**: Use the health check endpoints below to monitor status

#### 2. Worker Timeout
**Issue**: Gunicorn worker timeout
**Status**: Fixed with updated configuration in `render.yaml`

### Health Check Endpoints

Use these endpoints to monitor your application status:

- **Basic Health**: `https://budge-it-j4bp.onrender.com/health`
- **Database Test**: `https://budge-it-j4bp.onrender.com/test-db`
- **Supabase Status**: `https://budge-it-j4bp.onrender.com/check-supabase`
- **Detailed Status**: `https://budge-it-j4bp.onrender.com/database-status`

### Quick Fixes

1. **Check if Supabase is back online**:
   ```bash
   curl https://budge-it-j4bp.onrender.com/check-supabase
   ```

2. **Monitor application health**:
   ```bash
   curl https://budge-it-j4bp.onrender.com/health
   ```

3. **If still having issues, redeploy**:
   - Push any changes to your GitHub repository
   - Render will automatically redeploy

## 🛠️ Local Development

### Prerequisites
- Python 3.10+
- pip
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lMarul/Budge-IT.git
   cd Budge-IT
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=your_supabase_connection_string
   SECRET_KEY=your_secret_key
   FLASK_ENV=development
   ```

4. **Run the application**:
   ```bash
   python wsgi.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5001`

## 📊 Features

- **User Authentication**: Secure login and registration system
- **Transaction Management**: Add, edit, and delete income/expense transactions
- **Category Management**: Custom categories for better organization
- **Data Visualization**: Charts and graphs for financial insights
- **Admin Panel**: User management and system administration
- **Responsive Design**: Works on desktop and mobile devices

## 🗄️ Database

The application uses **Supabase** (PostgreSQL) as the primary database with automatic fallback to SQLite for development.

### Database Schema
- **Users**: User accounts and authentication
- **Categories**: Transaction categories (income/expense)
- **Transactions**: Financial transactions with metadata

## 🚀 Deployment

### Render Deployment
The application is configured for deployment on Render with:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app --timeout 120 --workers 2 --worker-class sync --max-requests 1000 --max-requests-jitter 100`
- **Environment**: Python 3.10.13

### Environment Variables
Set these in your Render dashboard:
- `DATABASE_URL`: Your Supabase PostgreSQL connection string
- `SECRET_KEY`: A secure secret key for Flask sessions
- `FLASK_ENV`: Set to `production`

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check your `DATABASE_URL` environment variable
   - Verify Supabase connection string format
   - Ensure Supabase service is running

2. **Application Won't Start**
   - Check Render logs for error messages
   - Verify all dependencies are in `requirements.txt`
   - Ensure `wsgi.py` is properly configured

3. **Supabase Connection Limits**
   - Wait for connection limits to reset (15-30 minutes)
   - Consider upgrading Supabase plan
   - Monitor with health check endpoints

### Getting Help

1. **Check Render Logs**: View deployment logs in Render dashboard
2. **Use Health Endpoints**: Monitor application status via provided endpoints
3. **Review Error Messages**: Check browser console and server logs

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

- **Anthony** - Backend Development
- **Marwin** - Frontend Development  
- **Nika** - Database Design
- **Vince** - System Architecture
- **Vinz** - UI/UX Design

---

**Note**: If you're experiencing Supabase connection issues, your data is safe! The application will automatically reconnect once connection limits are reset.

## 🚀 Current Status

**✅ App Successfully Deployed!**
- **Live URL**: https://budge-it-j4bp.onrender.com
- **Status**: Running and accessible
- **Database**: Supabase (PostgreSQL)

## 📊 Database Connection Status

The app is currently experiencing **Supabase connection limits** which is normal for the free tier. Here's what you need to know:

### ✅ What's Working
- App is deployed and accessible
- All your data is safe in Supabase
- App will work once connection limits reset (15-30 minutes)
- Users can access the app interface

### ⚠️ Current Issue
- Supabase connection timeouts due to connection limits
- Login attempts may fail during high traffic periods
- This is a **temporary connection issue**, not a data loss issue

### 💡 Solutions
1. **Wait 15-30 minutes** for connection limits to reset
2. **Upgrade Supabase plan** for higher connection limits
3. **Use the monitoring tools** below to check status

## 🔍 Monitoring Tools

### 1. Built-in Health Checks
Visit these URLs to check app status:
- **App Status**: https://budge-it-j4bp.onrender.com/status
- **Health Check**: https://budge-it-j4bp.onrender.com/health
- **Database Status**: https://budge-it-j4bp.onrender.com/db-status
- **Supabase Check**: https://budge-it-j4bp.onrender.com/check-supabase

### 2. Local Monitoring Script
Run the monitoring script to get detailed status:

```bash
python monitor_db.py
```

This script will:
- Check app accessibility
- Test database connections
- Show connection pool status
- Provide troubleshooting guidance

## 🛠️ Technical Details

### Database Configuration
- **Primary**: Supabase PostgreSQL
- **Connection Pool**: Ultra-conservative settings to avoid limits
- **Fallback**: SQLite (only if no DATABASE_URL)
- **Data Safety**: All data preserved in Supabase

### Connection Settings
- Pool Size: 1 connection
- Pool Recycle: 5 minutes
- Connection Timeout: 3 seconds
- Statement Timeout: 5 seconds

## 🚀 Deployment

The app is deployed on Render with the following configuration:

### Environment Variables
- `DATABASE_URL`: Supabase PostgreSQL connection string
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: 10000 (Render default)

### Build Process
1. Install Python dependencies
2. Initialize Flask app
3. Create database tables
4. Start Gunicorn server

## 📁 Project Structure

```
Final System - Live/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # Flask routes
│   ├── static/              # Static files
│   ├── templates/           # HTML templates
│   └── utils/               # Database utilities
├── instance/                # Instance-specific files
├── monitor_db.py            # Database monitoring script
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment config
├── supabase_schema.sql      # Database schema
└── wsgi.py                  # WSGI entry point
```

## 🔧 Development

### Local Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run: `python wsgi.py`

### Database Migration
The app automatically handles database initialization. If you need to migrate from JSON:
```python
from app.utils.database import migrate_from_json
migrate_from_json('budget_tracker.json')
```

## 📞 Support

### Common Issues
1. **Connection Timeouts**: Wait 15-30 minutes, then try again
2. **Login Failures**: Database connection issue - data is safe
3. **App Not Loading**: Check Render deployment status

### Data Safety
- **Your data is always safe in Supabase**
- Connection issues don't affect stored data
- App will reconnect automatically when limits reset

## 🎯 Next Steps

1. **Monitor the app** using the provided tools
2. **Wait for connection limits** to reset
3. **Consider upgrading** Supabase plan for better reliability
4. **Test login functionality** once connections are restored

---

**Remember**: Your data is safe in Supabase! Connection issues are temporary and will resolve automatically.
