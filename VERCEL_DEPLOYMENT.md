# Vercel + Supabase Deployment Guide

## 🚀 Quick Start

This guide will help you deploy your Flask app to Vercel with Supabase database integration.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
3. **Vercel CLI** (optional): `npm install -g vercel`

## Step 1: Set Up Supabase Database

1. **Create a Supabase project**:
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization and region
   - Wait for the project to be created

2. **Get your database connection string**:
   - Go to Settings → Database
   - Copy the "Connection string" (URI format)
   - It should look like: `postgresql://postgres:[password]@[project-ref].supabase.co:5432/postgres`

3. **Set up your database schema**:
   - Go to SQL Editor in Supabase
   - Run the SQL schema from `supabase_schema.sql` (if you have one)
   - Or let the app create tables automatically on first run

## Step 2: Deploy to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project? → No (for first deployment)
   - Project name → Enter your preferred name
   - Directory → ./ (current directory)
   - Override settings? → No

### Method 2: Using Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your Git repository** (GitHub, GitLab, Bitbucket)
4. **Configure the project**:
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

## Step 3: Configure Environment Variables

**This is the most important step for database sync!**

1. **Go to your Vercel project dashboard**
2. **Click "Settings" → "Environment Variables"**
3. **Add these variables**:

### Required Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://postgres:[password]@[project-ref].supabase.co:5432/postgres` | Your Supabase database connection string |
| `SECRET_KEY` | `your-super-secret-key-here` | A secure random string for Flask sessions |

### Example DATABASE_URL
```
postgresql://postgres:yourpassword@abcdefghijklmnop.supabase.co:5432/postgres
```

### How to Generate SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

## Step 4: Redeploy

After setting environment variables:

1. **Go to "Deployments" tab**
2. **Click "Redeploy" on your latest deployment**
3. **Or push a new commit to trigger automatic deployment**

## Step 5: Verify Database Sync

1. **Visit your Vercel URL** (e.g., `https://your-project.vercel.app`)
2. **Register a new account**
3. **Add some transactions**
4. **Check your Supabase dashboard** to see the data

## Troubleshooting

### Database Connection Issues

1. **Check your DATABASE_URL**:
   - Make sure it's the correct Supabase connection string
   - Verify the password is correct
   - Ensure the project reference is correct

2. **Check Vercel logs**:
   - Go to your deployment → "Functions" tab
   - Look for any database connection errors

3. **Test locally with Supabase**:
   ```bash
   set DATABASE_URL=postgresql://postgres:[password]@[project-ref].supabase.co:5432/postgres
   python wsgi.py
   ```

### Common Issues

1. **"Database not syncing"**:
   - Ensure `DATABASE_URL` is set in Vercel
   - Check that the environment variable is applied to production
   - Redeploy after setting environment variables

2. **"Missing user_loader"**:
   - This should be fixed in the current code
   - If you see this error, check that you're using the latest code

3. **"Connection timeout"**:
   - Check your Supabase project is active
   - Verify your IP is not blocked (for local testing)

## Database Schema

Your app will automatically create these tables in Supabase:

- `user` - User accounts
- `category` - Transaction categories
- `transaction` - Financial transactions

## Monitoring

1. **Vercel Analytics**: Monitor your app performance
2. **Supabase Dashboard**: Monitor database usage and performance
3. **Vercel Logs**: Check for any errors in real-time

## Security Best Practices

1. **Never commit secrets** to your repository
2. **Use environment variables** for all sensitive data
3. **Rotate your SECRET_KEY** regularly
4. **Use Supabase Row Level Security** (RLS) if needed

## Support

If you encounter issues:

1. Check the [Vercel documentation](https://vercel.com/docs)
2. Check the [Supabase documentation](https://supabase.com/docs)
3. Review your deployment logs in Vercel
4. Test locally with the same environment variables

## Next Steps

After successful deployment:

1. Set up a custom domain (optional)
2. Configure monitoring and analytics
3. Set up automatic deployments from your Git repository
4. Consider setting up staging environments 