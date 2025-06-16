# Setting Up Environment Variables in Vercel

## 🚀 **Quick Setup Methods**

### **Method 1: Vercel Dashboard (Easiest)**

1. **Go to your Vercel project dashboard**
2. **Click on your project**
3. **Go to Settings → Environment Variables**
4. **Add each variable**:

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://postgres:[password]@[host]:5432/postgres` | Your Supabase connection string |
| `SECRET_KEY` | `your-super-secret-key-here` | Flask secret key for sessions |
| `FLASK_ENV` | `production` | Flask environment setting |

### **Method 2: Vercel CLI (Command Line)**

```bash
# Set environment variables
vercel env add DATABASE_URL production "postgresql://postgres:[password]@[host]:5432/postgres"
vercel env add SECRET_KEY production "your-super-secret-key-here"
vercel env add FLASK_ENV production "production"

# Deploy
vercel --prod
```

### **Method 3: Automated Script**

Run the setup script I created:

```bash
python setup_vercel_env.py
```

## 🔧 **Getting Your Supabase Connection String**

1. **Go to Supabase Dashboard**
2. **Select your project**
3. **Go to Settings → Database**
4. **Copy the "Connection string"**
5. **Replace `[password]` with your actual password**

Example:
```
postgresql://postgres:your-actual-password@db.abcdefghijklmnop.supabase.co:5432/postgres
```

## 📁 **Local Development vs Production**

### **Local Development (.env file)**
Create a `.env` file in your project root:
```env
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
DEBUG=True
```

### **Production (Vercel Environment Variables)**
Set these in Vercel dashboard:
```env
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

## 🔒 **Security Best Practices**

### **Secret Key Generation**
Generate a strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### **Environment Variable Security**
- ✅ **Do**: Use Vercel's environment variable system
- ✅ **Do**: Generate strong, unique secret keys
- ✅ **Do**: Use different keys for development and production
- ❌ **Don't**: Commit `.env` files to Git
- ❌ **Don't**: Use weak or default secret keys

## 🚨 **Common Issues & Solutions**

### **Issue 1: "DATABASE_URL not found"**
**Solution**: Make sure you've set the environment variable in Vercel dashboard

### **Issue 2: "Secret key not set"**
**Solution**: Generate a new secret key and set it in Vercel

### **Issue 3: "Database connection failed"**
**Solution**: 
1. Check your Supabase connection string
2. Verify your Supabase database is running
3. Check if your IP is whitelisted in Supabase

### **Issue 4: "Environment variables not loading"**
**Solution**:
1. Make sure you're in the correct environment (Production/Preview/Development)
2. Redeploy after setting environment variables
3. Check Vercel build logs for errors

## 📋 **Deployment Checklist**

- [ ] Supabase project created and running
- [ ] Database schema applied
- [ ] Environment variables set in Vercel
- [ ] Secret key generated and set
- [ ] Local testing completed
- [ ] Git repository up to date
- [ ] Vercel project connected to repository

## 🔄 **Updating Environment Variables**

### **Via Dashboard**
1. Go to Vercel project settings
2. Edit environment variables
3. Redeploy automatically

### **Via CLI**
```bash
# Update existing variable
vercel env rm DATABASE_URL production
vercel env add DATABASE_URL production "new-connection-string"

# Deploy changes
vercel --prod
```

## 📊 **Monitoring Environment Variables**

### **Check Current Variables**
```bash
vercel env ls
```

### **View Variable Values**
```bash
vercel env pull .env.local
```

## 🎯 **Pro Tips**

1. **Use different environments**: Set up separate variables for Production, Preview, and Development
2. **Test locally**: Use `.env` file for local testing before deploying
3. **Monitor logs**: Check Vercel function logs for environment variable issues
4. **Backup variables**: Keep a secure backup of your environment variables
5. **Rotate secrets**: Regularly update your secret keys

## 🆘 **Need Help?**

If you encounter issues:

1. **Check Vercel Build Logs**: Look for specific error messages
2. **Test Locally**: Use `python test_app.py` to verify functionality
3. **Verify Supabase**: Ensure database connection works
4. **Check Environment**: Make sure variables are set for the correct environment

## 📞 **Support Resources**

- [Vercel Environment Variables Documentation](https://vercel.com/docs/concepts/projects/environment-variables)
- [Supabase Connection Guide](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [Flask Configuration Guide](https://flask.palletsprojects.com/en/2.3.x/config/) 