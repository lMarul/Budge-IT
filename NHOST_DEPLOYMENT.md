# Nhost Deployment Guide for Budget Tracker

This guide will help you deploy your Flask Budget Tracker app to Nhost with PostgreSQL integration.

## Prerequisites

1. **Nhost Account**: Sign up at [nhost.io](https://nhost.io)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
3. **Nhost CLI**: Install for local development (optional)

## Step 1: Set Up Nhost Project

### 1.1 Create Nhost Project
1. Go to [nhost.io](https://nhost.io) and create a new project
2. Wait for the project to be created (this may take a few minutes)
3. Note down your project subdomain (e.g., `your-project.nhost.run`)

### 1.2 Set Up Database Schema
1. Go to the Nhost Dashboard → Database
2. Use the SQL Editor to run the schema from `supabase_schema.sql`
3. Or use the Nhost CLI to apply migrations

### 1.3 Get Environment Variables
1. Go to Settings → Environment Variables in your Nhost dashboard
2. Copy the following variables:
   - `NHOST_BACKEND_URL`
   - `NHOST_GRAPHQL_URL`
   - `NHOST_STORAGE_URL`
   - `NHOST_AUTH_URL`
   - `DATABASE_URL` (PostgreSQL connection string)

## Step 2: Deploy to Nhost

### 2.1 Connect Your Repository
1. Go to your Nhost project dashboard
2. Navigate to Functions → Deploy
3. Connect your Git repository
4. Select the repository containing your Flask app

### 2.2 Configure the Function
Set these configuration options:

- **Name**: `budget-tracker` (or your preferred name)
- **Runtime**: `Python 3.11`
- **Entry Point**: `wsgi.py`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python wsgi.py`

### 2.3 Set Environment Variables
Add these environment variables in Nhost:

| Variable | Value | Description |
|----------|-------|-------------|
| `NHOST_BACKEND_URL` | `https://your-project.nhost.run/v1` | Nhost backend URL |
| `NHOST_GRAPHQL_URL` | `https://your-project.nhost.run/v1/graphql` | Nhost GraphQL URL |
| `NHOST_STORAGE_URL` | `https://your-project.nhost.run/v1/storage` | Nhost storage URL |
| `NHOST_AUTH_URL` | `https://your-project.nhost.run/v1/auth` | Nhost auth URL |
| `DATABASE_URL` | `postgresql://postgres:[password]@[host]:5432/postgres` | PostgreSQL connection string |
| `SECRET_KEY` | `your-super-secret-key-here` | Flask secret key for sessions |
| `FLASK_ENV` | `production` | Flask environment setting |

### 2.4 Deploy
1. Click "Deploy Function"
2. Wait for the build to complete
3. Your app will be available at the provided URL

## Step 3: Verify Deployment

### 3.1 Check Build Logs
If deployment fails, check the build logs in Nhost for errors. Common issues:

- **Import Errors**: Make sure all imports use the correct paths
- **Database Connection**: Verify `DATABASE_URL` is correct
- **Missing Dependencies**: Ensure `requirements.txt` is complete

### 3.2 Test the Application
1. Visit your deployed URL
2. Try to register a new user
3. Test login functionality
4. Add some transactions

## Troubleshooting Common Issues

### Issue 1: "Module not found" Errors
**Solution**: Ensure all imports use the correct paths:
```python
# Correct
from app.models import User
from app.utils.database import create_user

# Incorrect
from models import User
from utils.database import create_user
```

### Issue 2: Database Connection Errors
**Solution**: 
1. Verify `DATABASE_URL` is set correctly in Nhost
2. Check PostgreSQL connection string format
3. Ensure Nhost database is accessible

### Issue 3: Flask-Login Issues
**Solution**: Make sure `user_loader` is properly configured in `app/__init__.py`:
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### Issue 4: Nhost Integration Issues
**Solution**: 
1. Verify all Nhost environment variables are set
2. Check Nhost backend URLs are correct
3. Ensure Nhost project is running

### Issue 5: Build Timeout
**Solution**: 
1. Check if all dependencies are properly listed in `requirements.txt`
2. Optimize imports and reduce build complexity
3. Consider using a build cache

## Local Testing Before Deployment

### Test Locally with Nhost
```bash
# Install Nhost CLI
npm install -g nhost

# Link to your Nhost project
nhost link

# Set environment variables
export NHOST_BACKEND_URL="https://your-project.nhost.run/v1"
export NHOST_GRAPHQL_URL="https://your-project.nhost.run/v1/graphql"
export NHOST_STORAGE_URL="https://your-project.nhost.run/v1/storage"
export NHOST_AUTH_URL="https://your-project.nhost.run/v1/auth"
export DATABASE_URL="your-postgresql-connection-string"
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"

# Run the app
python wsgi.py
```

### Run the Test Script
```bash
python test_app.py
```

## Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `NHOST_BACKEND_URL` | Nhost backend URL | Yes | `https://your-project.nhost.run/v1` |
| `NHOST_GRAPHQL_URL` | Nhost GraphQL URL | Yes | `https://your-project.nhost.run/v1/graphql` |
| `NHOST_STORAGE_URL` | Nhost storage URL | Yes | `https://your-project.nhost.run/v1/storage` |
| `NHOST_AUTH_URL` | Nhost auth URL | Yes | `https://your-project.nhost.run/v1/auth` |
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://postgres:password@host:5432/postgres` |
| `SECRET_KEY` | Flask secret key for sessions | Yes | `your-super-secret-key-here` |
| `FLASK_ENV` | Flask environment | No | `production` |

## File Structure for Nhost

Your project should have this structure:
```
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── templates/
│   └── static/
├── wsgi.py
├── requirements.txt
├── runtime.txt
└── README.md
```

## Monitoring and Maintenance

### Check Deployment Status
- Monitor Nhost dashboard for deployment status
- Check function logs for errors
- Monitor Nhost database performance

### Update Deployment
1. Push changes to your Git repository
2. Nhost will automatically redeploy
3. Check build logs for any issues

## Support

If you encounter issues:

1. **Check Nhost Function Logs**: Look for specific error messages
2. **Test Locally**: Use `python test_app.py` to verify local functionality
3. **Verify Environment Variables**: Ensure all required variables are set
4. **Check Nhost**: Verify database connection and project status

## Quick Deployment Checklist

- [ ] Nhost project created and running
- [ ] Database schema applied
- [ ] Environment variables configured in Nhost
- [ ] All imports use absolute paths
- [ ] `requirements.txt` includes all dependencies
- [ ] `wsgi.py` is properly configured
- [ ] Local testing passes (`python test_app.py`)
- [ ] Git repository is up to date
- [ ] Deployment successful and app accessible

## Common Error Messages and Solutions

### "No module named 'app'"
**Solution**: Ensure `wsgi.py` imports correctly and all paths are absolute

### "Database connection failed"
**Solution**: Verify `DATABASE_URL` format and Nhost credentials

### "Missing user_loader"
**Solution**: Ensure `user_loader` function is defined in `app/__init__.py`

### "Nhost backend not accessible"
**Solution**: Check Nhost project status and environment variables

### "Import error in routes"
**Solution**: Verify all imports use absolute paths from the app root

## Nhost CLI Commands

```bash
# Install Nhost CLI
npm install -g nhost

# Login to Nhost
nhost login

# Link to project
nhost link

# Deploy function
nhost functions deploy

# Check status
nhost status
``` 