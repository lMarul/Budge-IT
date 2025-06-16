# Debugging Vercel Internal Server Errors

## 🚨 **Common Causes & Solutions**

### **Issue 1: Missing Environment Variables**

**Symptoms**: Internal Server Error when accessing database-dependent routes
**Solution**: Set up environment variables in Vercel

#### **Quick Fix via Vercel Dashboard:**
1. Go to your Vercel project dashboard
2. Click **Settings → Environment Variables**
3. Add these variables:

```
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

#### **Quick Fix via CLI:**
```bash
# Login to Vercel first
vercel login

# Set environment variables
vercel env add DATABASE_URL production "your-supabase-connection-string"
vercel env add SECRET_KEY production "your-secret-key"
vercel env add FLASK_ENV production "production"

# Redeploy
vercel --prod
```

### **Issue 2: Database Connection Problems**

**Symptoms**: Errors when accessing Account or Admin Database pages
**Solution**: Verify Supabase connection

#### **Check Supabase Connection:**
1. Go to Supabase Dashboard
2. Check if your database is running
3. Verify connection string format
4. Check if your IP is whitelisted

#### **Test Database Connection Locally:**
```bash
python test_database_connection.py
```

### **Issue 3: Import Path Issues**

**Symptoms**: ModuleNotFoundError in logs
**Solution**: Check import paths

#### **Common Fixes:**
1. Ensure all imports use absolute paths:
```python
# ✅ Correct
from app.models import User
from app.routes.auth import auth_bp

# ❌ Incorrect
from models import User
from routes.auth import auth_bp
```

2. Check `vercel.json` has correct PYTHONPATH:
```json
{
  "env": {
    "PYTHONPATH": ".",
    "FLASK_APP": "wsgi.py"
  }
}
```

### **Issue 4: Flask-Login Configuration**

**Symptoms**: Authentication errors
**Solution**: Verify user_loader setup

#### **Check app/__init__.py:**
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

## 🔧 **Immediate Fixes to Try**

### **Fix 1: Set Environment Variables**
Run this script to set up environment variables:
```bash
python setup_vercel_env.py
```

### **Fix 2: Update vercel.json**
Make sure your `vercel.json` has proper error handling:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/app/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ],
  "functions": {
    "wsgi.py": {
      "maxDuration": 30
    }
  },
  "env": {
    "FLASK_ENV": "production",
    "PYTHONPATH": ".",
    "FLASK_APP": "wsgi.py"
  }
}
```

### **Fix 3: Add Error Handling to wsgi.py**
```python
# Production WSGI entry point for Vercel deployment
import os
import sys
from app import create_app

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Create the application instance with production configuration
    app = create_app()
    
    # Ensure we're in production mode
    if not app.debug:
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Budget Tracker startup')
        
except Exception as e:
    print(f"Error creating app: {e}")
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    app.run()
```

## 📊 **How to Check Logs**

### **Method 1: Vercel Dashboard**
1. Go to your Vercel project
2. Click on the latest deployment
3. Click "Functions" tab
4. Check the logs for errors

### **Method 2: Vercel CLI**
```bash
# Login first
vercel login

# Check logs
vercel logs

# Check specific function logs
vercel logs wsgi.py
```

### **Method 3: Local Testing**
```bash
# Test locally with production settings
export DATABASE_URL="your-supabase-connection-string"
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
python wsgi.py
```

## 🎯 **Step-by-Step Debugging Process**

### **Step 1: Check Environment Variables**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Verify all required variables are set
3. Check for typos in variable names

### **Step 2: Test Database Connection**
1. Run `python test_database_connection.py`
2. Verify Supabase is accessible
3. Check connection string format

### **Step 3: Check Import Paths**
1. Look for ModuleNotFoundError in logs
2. Verify all imports use absolute paths
3. Check `vercel.json` PYTHONPATH setting

### **Step 4: Verify Flask Configuration**
1. Check `app/__init__.py` for proper setup
2. Verify user_loader function
3. Check database initialization

### **Step 5: Redeploy with Fixes**
```bash
# Commit any fixes
git add .
git commit -m "Fix: Resolve Internal Server Error"
git push

# Redeploy
vercel --prod
```

## 🚨 **Emergency Fixes**

### **If Still Getting Errors:**
1. **Check Supabase**: Ensure database is running and accessible
2. **Regenerate Secret Key**: Use `import secrets; print(secrets.token_hex(32))`
3. **Verify Routes**: Check if all route imports are correct
4. **Test Locally**: Use `.env` file to test locally first

### **Quick Environment Variable Test:**
Add this to your main route to test:
```python
@app.route('/test-env')
def test_env():
    return {
        'database_url': bool(os.environ.get('DATABASE_URL')),
        'secret_key': bool(os.environ.get('SECRET_KEY')),
        'flask_env': os.environ.get('FLASK_ENV')
    }
```

## 📞 **Need More Help?**

1. **Check Vercel Status**: [status.vercel.com](https://status.vercel.com)
2. **Supabase Status**: [status.supabase.com](https://status.supabase.com)
3. **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)

## 🔄 **Redeployment Checklist**

- [ ] Environment variables set in Vercel
- [ ] Database connection tested
- [ ] Import paths verified
- [ ] Flask configuration checked
- [ ] Local testing passed
- [ ] Changes committed and pushed
- [ ] Redeployed to Vercel 