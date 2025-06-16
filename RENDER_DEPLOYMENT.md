# Render Deployment Guide for Budget Tracker

Simple step-by-step guide to deploy your Flask Budget Tracker to Render.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
3. **Git Repository**: Your code should be in a Git repository

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the project to be created

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

## Step 3: Test Your Application

1. Visit your deployed URL
2. Try to register a new user
3. Test login functionality
4. Add some transactions

## Troubleshooting

### Common Issues:

1. **"Module not found" Errors**
   - Make sure all imports use absolute paths: `from app.models import User`

2. **Database Connection Errors**
   - Verify `DATABASE_URL` is set correctly in Render
   - Check Supabase connection string format

3. **Build Failures**
   - Check if all dependencies are in `requirements.txt`
   - Verify `gunicorn` is included in requirements

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Supabase PostgreSQL connection string | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Flask environment | No |

## File Structure

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

## Quick Deployment Checklist

- [ ] Supabase project created and schema applied
- [ ] Environment variables configured in Render
- [ ] All imports use absolute paths
- [ ] `requirements.txt` includes all dependencies
- [ ] `wsgi.py` is properly configured
- [ ] Git repository is up to date
- [ ] Deployment successful and app accessible 