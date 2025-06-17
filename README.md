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
