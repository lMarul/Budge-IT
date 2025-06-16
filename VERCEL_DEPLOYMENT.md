# Vercel Deployment Guide

## Overview
This guide will help you deploy your Flask application to Vercel, a modern cloud platform for static sites and serverless functions.

## Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```

## Project Structure
Your project is already configured for Vercel with:
- `vercel.json` - Vercel configuration
- `wsgi.py` - WSGI entry point
- `requirements.txt` - Python dependencies

## Deployment Steps

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project? → No (for first deployment)
   - Project name → Enter your preferred name
   - Directory → ./ (current directory)
   - Override settings? → No

5. **Your app will be deployed** and you'll get a URL like:
   ```
   https://your-project-name.vercel.app
   ```

### Method 2: Using Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your Git repository** (GitHub, GitLab, Bitbucket)
4. **Configure the project**:
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`
5. **Add Environment Variables** (if needed):
   - `SECRET_KEY`: Your Flask secret key
   - `DATABASE_URL`: Your database connection string
6. **Click "Deploy"**

## Environment Variables

Set these in your Vercel project settings:

### Required
- `SECRET_KEY`: Your Flask secret key (generate a secure one)
- `FLASK_ENV`: Set to `production`

### Optional (for database)
- `DATABASE_URL`: Your database connection string
  - For Supabase: `postgresql://user:password@host:port/database`
  - For local development: `sqlite:///app.db`

## Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### wsgi.py
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

## Database Setup

### For Supabase (Recommended)
1. Create a Supabase project
2. Get your database connection string
3. Set `DATABASE_URL` environment variable in Vercel
4. Run database migrations (if needed)

### For SQLite (Development only)
- SQLite works locally but not recommended for production
- Use Supabase or another PostgreSQL service for production

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Make sure all imports use relative paths (e.g., `from .models import User`)
   - Check that all required packages are in `requirements.txt`

2. **Database Connection**:
   - Verify `DATABASE_URL` is set correctly
   - Test database connection locally first

3. **Static Files**:
   - Static files should be in the `static/` directory
   - They'll be served automatically by Flask

4. **Environment Variables**:
   - Make sure all required environment variables are set in Vercel dashboard
   - Check that variable names match exactly

### Debugging

1. **Check Vercel Logs**:
   - Go to your project in Vercel dashboard
   - Click on "Functions" tab
   - Check the logs for errors

2. **Local Testing**:
   ```bash
   # Test locally with production settings
   export FLASK_ENV=production
   python wsgi.py
   ```

## Post-Deployment

1. **Test your application**:
   - Visit your Vercel URL
   - Test all major functionality
   - Check for any errors in the console

2. **Set up custom domain** (optional):
   - Go to your project settings in Vercel
   - Add your custom domain
   - Configure DNS settings

3. **Monitor performance**:
   - Use Vercel Analytics
   - Monitor function execution times
   - Check for any performance issues

## Security Considerations

1. **Environment Variables**:
   - Never commit secrets to your repository
   - Use Vercel's environment variable system
   - Rotate secrets regularly

2. **Database Security**:
   - Use connection pooling
   - Enable SSL for database connections
   - Use strong passwords

3. **Application Security**:
   - Keep dependencies updated
   - Use HTTPS (automatic with Vercel)
   - Implement proper authentication

## Support

If you encounter issues:
1. Check the [Vercel documentation](https://vercel.com/docs)
2. Review your application logs
3. Test locally with production settings
4. Contact Vercel support if needed

## Next Steps

After successful deployment:
1. Set up continuous deployment from your Git repository
2. Configure monitoring and analytics
3. Set up staging environments
4. Implement CI/CD pipelines 