# Render Deployment Guide for Budget Tracker

This guide will help you deploy your Flask Budget Tracker app to Render with Supabase integration.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the project to be created (this may take a few minutes)

### 1.2 Set Up Database Schema
1. Go to the SQL Editor in your Supabase dashboard
2. Copy and paste the contents of `supabase_schema.sql` into the editor
3. Run the SQL script to create all necessary tables

### 1.3 Get Database Connection String
1. Go to Settings → Database in your Supabase dashboard
2. Copy the "Connection string" (URI format)
3. It should look like: `postgresql://postgres:[password]@[host]:5432/postgres`

## Step 2: Deploy to Render

### 2.1 Connect Your Repository
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Select the repository containing your Flask app

### 2.2 Configure the Web Service
Set these configuration options:

- **Name**: `budget-tracker` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app`
- **Plan**: Free (or paid if needed)

### 2.3 Set Environment Variables
Add these environment variables in Render:

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://postgres:[password]@[host]:5432/postgres` | Your Supabase connection string |
| `SECRET_KEY` | `your-super-secret-key-here` | Flask secret key for sessions |
| `FLASK_ENV` | `production` | Flask environment setting |

### 2.4 Deploy
1. Click "Create Web Service"
2. Wait for the build to complete
3. Your app will be available at the provided URL

## Step 3: Verify Deployment

### 3.1 Check Build Logs
If deployment fails, check the build logs in Render for errors. Common issues:

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
1. Verify `DATABASE_URL` is set correctly in Render
2. Check Supabase connection string format
3. Ensure Supabase database is accessible

### Issue 3: Flask-Login Issues
**Solution**: Make sure `user_loader` is properly configured in `app/__init__.py`:
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### Issue 4: Static Files Not Loading
**Solution**: Ensure static files are in the correct location:
```
app/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
```

### Issue 5: Build Timeout
**Solution**: 
1. Check if all dependencies are properly listed in `requirements.txt`
2. Optimize imports and reduce build complexity
3. Consider using a build cache

## Local Testing Before Deployment

### Test Locally with Production Settings
```bash
# Set production environment variables
export DATABASE_URL="your-supabase-connection-string"
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
| `DATABASE_URL` | Supabase PostgreSQL connection string | Yes | `postgresql://postgres:password@host:5432/postgres` |
| `SECRET_KEY` | Flask secret key for sessions | Yes | `your-super-secret-key-here` |
| `FLASK_ENV` | Flask environment | No | `production` |

## File Structure for Render

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
- Monitor Render dashboard for deployment status
- Check build logs for errors
- Monitor Supabase dashboard for database performance

### Update Deployment
1. Push changes to your Git repository
2. Render will automatically redeploy
3. Check build logs for any issues

## Support

If you encounter issues:

1. **Check Render Build Logs**: Look for specific error messages
2. **Test Locally**: Use `python test_app.py` to verify local functionality
3. **Verify Environment Variables**: Ensure all required variables are set
4. **Check Supabase**: Verify database connection and schema

## Quick Deployment Checklist

- [ ] Supabase project created and schema applied
- [ ] Environment variables configured in Render
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
**Solution**: Verify `DATABASE_URL` format and Supabase credentials

### "Missing user_loader"
**Solution**: Ensure `user_loader` function is defined in `app/__init__.py`

### "Build timeout"
**Solution**: Check `requirements.txt` and optimize build process

### "Import error in routes"
**Solution**: Verify all imports use absolute paths from the app root 