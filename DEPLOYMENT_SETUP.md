# Deployment Setup Guide

## Environment Variables Required

Create a `.env` file in your project root with the following variables:

```env
# Flask Secret Key (generate a secure random key for production)
SECRET_KEY=your-secret-key-change-in-production

# Database URL (Supabase PostgreSQL connection string)
# Format: postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
DATABASE_URL=postgresql://postgres:password@localhost:5432/budget_tracker

# Flask Environment
FLASK_ENV=production
FLASK_APP=wsgi.py

# Debug Mode (set to False for production)
DEBUG=False
```

## Render Deployment Configuration

The application is configured for Render deployment with:

- **Python Version**: 3.7.18
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
- **Environment**: Production

## Database Setup

1. Create a Supabase project
2. Run the SQL schema from `supabase_schema.sql`
3. Get your database connection string
4. Set the `DATABASE_URL` environment variable in Render

## Security Notes

- Generate a secure random secret key for production
- Never commit the `.env` file to version control
- Use environment variables for all sensitive configuration 