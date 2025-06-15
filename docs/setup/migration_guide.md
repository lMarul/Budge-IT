# Budget Tracker - SQLAlchemy Migration Guide

This guide will help you migrate your Budget Tracker application from a JSON-based database to SQLAlchemy with Supabase integration.

## 🎯 What's Changed

Your application has been updated to use:
- **SQLAlchemy ORM** instead of JSON file storage
- **PostgreSQL** database (Supabase) instead of local JSON files
- **Proper database relationships** and constraints
- **Better data integrity** and performance

## 📋 Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Python Dependencies**: Install the new requirements
3. **Environment Setup**: Configure your database connection

## 🚀 Step-by-Step Migration

### Step 1: Install New Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Supabase

1. **Create a new project** in Supabase
2. **Get your database connection string**:
   - Go to Settings → Database
   - Copy the connection string
   - It should look like: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`

### Step 3: Configure Environment Variables

1. **Copy the environment template**:
   ```bash
   cp env_template.txt .env
   ```

2. **Edit `.env` file** with your actual values:
   ```env
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
   FLASK_ENV=development
   DEBUG=True
   ```

### Step 4: Run the Migration Script

```bash
python migrate_to_sqlalchemy.py
```

This script will:
- ✅ Create the database tables
- ✅ Migrate your existing data from JSON to SQLAlchemy
- ✅ Backup your original JSON file
- ✅ Show you the migration results

### Step 5: Update Your Application

1. **Replace the old app.py**:
   ```bash
   cp app_sqlalchemy.py app.py
   ```

2. **Update your route files** to use the new models:
   - Replace `from models import User, Category, Transaction` with `from models_sqlalchemy import User, Category, Transaction`
   - Replace `from utils import ...` with `from utils_sqlalchemy import ...`

### Step 6: Test Your Application

```bash
python app.py
```

## 🔧 File Structure

```
budget_tracker/
├── app.py                    # Updated main application (SQLAlchemy)
├── app_sqlalchemy.py         # New SQLAlchemy version
├── models_sqlalchemy.py      # New SQLAlchemy models
├── utils_sqlalchemy.py       # New SQLAlchemy utilities
├── config.py                 # Updated configuration
├── requirements.txt          # Updated dependencies
├── migrate_to_sqlalchemy.py  # Migration script
├── env_template.txt          # Environment template
├── .env                      # Your environment variables (create this)
├── budget_tracker.json       # Your old JSON database
└── budget_tracker.json.backup # Backup of your old database
```

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`

### Categories Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `name`
- `category_type` ('income' or 'expense')
- `color` (Hex color code)
- `created_at`

### Transactions Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `category_id` (Foreign Key to Categories)
- `amount` (Decimal)
- `transaction_type` ('income' or 'expense')
- `date`
- `item_name`
- `created_at`

## 🔄 Migration Functions

The new system includes these helper functions:

### User Management
- `create_user(username, email, password)`
- `authenticate_user(username, password)`
- `get_user_by_id(user_id)`
- `get_user_by_username(username)`

### Category Management
- `create_category(user_id, name, category_type, color)`
- `get_categories_by_user_and_type(user_id, category_type)`

### Transaction Management
- `create_transaction(user_id, amount, category_id, transaction_type, date, item_name)`
- `get_transactions_by_user(user_id)`

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check your `DATABASE_URL` in `.env`
   - Verify your Supabase credentials
   - Ensure your IP is whitelisted in Supabase

2. **Migration Fails**:
   - Check if your JSON file is valid
   - Ensure you have write permissions
   - Check the console for specific error messages

3. **Import Errors**:
   - Make sure all dependencies are installed
   - Check that you're importing from the correct modules

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your Supabase connection
3. Ensure all environment variables are set correctly

## 🎉 Benefits of the New System

- **Scalability**: Can handle thousands of users and transactions
- **Data Integrity**: Foreign key constraints prevent orphaned records
- **Performance**: Indexed database queries are much faster
- **Backup**: Automatic Supabase backups
- **Security**: Better password hashing and data protection
- **Development**: Better debugging and development tools

## 🔒 Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable SSL in production
- Regularly backup your database

## 📝 Next Steps

After successful migration:
1. Test all functionality thoroughly
2. Update your deployment scripts
3. Set up monitoring and logging
4. Consider adding database migrations for future changes
5. Remove the old JSON files once you're confident

---

**Need help?** Check the console output for specific error messages or refer to the SQLAlchemy and Supabase documentation. 