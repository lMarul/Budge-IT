# Marwin - SQLAlchemy Models for Budget Tracker

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import event

# Import db from the main app module to avoid conflicts
from app import db

class User(db.Model):
    """
    User model for SQLAlchemy database.
    
    This model represents user accounts in the database with proper relationships
    to categories and transactions.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    categories = relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """
    Category model for SQLAlchemy database.
    
    This model represents expense and income categories with proper relationships
    to users and transactions.
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    color = db.Column(db.String(7), nullable=False)  # Hex color code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = relationship('Transaction', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert category object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category_type': self.category_type,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name} ({self.category_type})>'

class Transaction(db.Model):
    """
    Transaction model for SQLAlchemy database.
    
    This model represents financial transactions with proper relationships
    to users and categories.
    """
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.Date, nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert transaction object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'amount': float(self.amount) if self.amount else 0.0,
            'transaction_type': self.transaction_type,
            'date': self.date.isoformat() if self.date else None,
            'item_name': self.item_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.item_name} ({self.amount})>'

# Database initialization function
def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

# Migration helper function
def migrate_from_json(json_file_path):
    """
    Migrate data from JSON file to SQLAlchemy database.
    
    This function reads the existing JSON database and creates corresponding
    records in the SQLAlchemy database.
    """
    import json
    import os
    
    if not os.path.exists(json_file_path):
        print(f"JSON file {json_file_path} not found. Skipping migration.")
        return
    
    try:
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)
        
        # Migrate users
        for user_data in json_data.get('users', []):
            user = User.query.filter_by(username=user_data['username']).first()
            if not user:
                user = User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash']
                )
                if 'created_at' in user_data:
                    user.created_at = datetime.fromisoformat(user_data['created_at'])
                db.session.add(user)
        
        # Migrate categories
        for category_data in json_data.get('categories', []):
            category = Category.query.filter_by(id=category_data['id']).first()
            if not category:
                category = Category(
                    id=category_data['id'],
                    user_id=category_data['user_id'],
                    name=category_data['name'],
                    category_type=category_data['category_type'],
                    color=category_data['color']
                )
                if 'created_at' in category_data:
                    category.created_at = datetime.fromisoformat(category_data['created_at'])
                db.session.add(category)
        
        # Migrate transactions
        for transaction_data in json_data.get('transactions', []):
            transaction = Transaction.query.filter_by(id=transaction_data['id']).first()
            if not transaction:
                transaction = Transaction(
                    id=transaction_data['id'],
                    user_id=transaction_data['user_id'],
                    category_id=transaction_data['category_id'],
                    amount=transaction_data['amount'],
                    transaction_type=transaction_data['transaction_type'],
                    date=datetime.fromisoformat(transaction_data['date']).date(),
                    item_name=transaction_data['item_name']
                )
                if 'created_at' in transaction_data:
                    transaction.created_at = datetime.fromisoformat(transaction_data['created_at'])
                db.session.add(transaction)
        
        db.session.commit()
        print(f"Successfully migrated data from {json_file_path}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during migration: {e}")
        raise 