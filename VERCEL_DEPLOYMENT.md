# Vercel Deployment Guide for Budget Tracker

This guide will help you deploy your Flask Budget Tracker app to Vercel with Supabase integration.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
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

## Step 2: Deploy to Vercel

### 2.1 Connect Your Repository
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository
4. Select the repository containing your Flask app

### 2.2 Configure Environment Variables
In the Vercel project settings, add these environment variables:

```
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

**Important**: Replace `[password]` and `[host]` with your actual Supabase credentials.

### 2.3 Deploy
1. Click "Deploy" in Vercel
2. Wait for the build to complete
3. Your app will be available at the provided URL

## Step 3: Verify Deployment

### 3.1 Check Build Logs
If deployment fails, check the build logs in Vercel for errors. Common issues:

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
**Solution**: Ensure all imports use absolute paths from the app root:
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
1. Verify `DATABASE_URL` is set correctly in Vercel
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
1. Check `vercel.json` maxDuration setting
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

## File Structure for Vercel

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
├── vercel.json
└── README.md
```

## Monitoring and Maintenance

### Check Deployment Status
- Monitor Vercel dashboard for deployment status
- Check function logs for errors
- Monitor Supabase dashboard for database performance

### Update Deployment
1. Push changes to your Git repository
2. Vercel will automatically redeploy
3. Check build logs for any issues

## Support

If you encounter issues:

1. **Check Vercel Build Logs**: Look for specific error messages
2. **Test Locally**: Use `python test_app.py` to verify local functionality
3. **Verify Environment Variables**: Ensure all required variables are set
4. **Check Supabase**: Verify database connection and schema

## Quick Deployment Checklist

- [ ] Supabase project created and schema applied
- [ ] Environment variables configured in Vercel
- [ ] All imports use absolute paths
- [ ] `requirements.txt` includes all dependencies
- [ ] `vercel.json` is properly configured
- [ ] Local testing passes (`python test_app.py`)
- [ ] Git repository is up to date
- [ ] Deployment successful and app accessible

## Common Error Messages and Solutions

### "No module named 'app'"
**Solution**: Add `"PYTHONPATH": "."` to `vercel.json` env section

### "Database connection failed"
**Solution**: Verify `DATABASE_URL` format and Supabase credentials

### "Missing user_loader"
**Solution**: Ensure `user_loader` function is defined in `app/__init__.py`

### "Build timeout"
**Solution**: Increase `maxDuration` in `vercel.json` functions section

### "Import error in routes"
**Solution**: Check all import statements use absolute paths from app root 