-- Supabase Database Schema for Budget Tracker
-- This schema will be created automatically by SQLAlchemy, but you can also run this manually

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE IF NOT EXISTS "category" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('income', 'expense')),
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS "transaction" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES "category"(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('income', 'expense')),
    item_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_category_user_id ON "category"(user_id);
CREATE INDEX IF NOT EXISTS idx_category_type ON "category"(category_type);
CREATE INDEX IF NOT EXISTS idx_transaction_user_id ON "transaction"(user_id);
CREATE INDEX IF NOT EXISTS idx_transaction_category_id ON "transaction"(category_id);
CREATE INDEX IF NOT EXISTS idx_transaction_date ON "transaction"(date);
CREATE INDEX IF NOT EXISTS idx_transaction_type ON "transaction"(transaction_type);

-- Row Level Security (RLS) policies for Supabase
-- Enable RLS on all tables
ALTER TABLE "user" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "category" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "transaction" ENABLE ROW LEVEL SECURITY;

-- User policies (users can only see their own data)
CREATE POLICY "Users can view own profile" ON "user" FOR SELECT USING (auth.uid()::text = id::text);
CREATE POLICY "Users can update own profile" ON "user" FOR UPDATE USING (auth.uid()::text = id::text);

-- Category policies
CREATE POLICY "Users can view own categories" ON "category" FOR SELECT USING (user_id = auth.uid()::integer);
CREATE POLICY "Users can insert own categories" ON "category" FOR INSERT WITH CHECK (user_id = auth.uid()::integer);
CREATE POLICY "Users can update own categories" ON "category" FOR UPDATE USING (user_id = auth.uid()::integer);
CREATE POLICY "Users can delete own categories" ON "category" FOR DELETE USING (user_id = auth.uid()::integer);

-- Transaction policies
CREATE POLICY "Users can view own transactions" ON "transaction" FOR SELECT USING (user_id = auth.uid()::integer);
CREATE POLICY "Users can insert own transactions" ON "transaction" FOR INSERT WITH CHECK (user_id = auth.uid()::integer);
CREATE POLICY "Users can update own transactions" ON "transaction" FOR UPDATE USING (user_id = auth.uid()::integer);
CREATE POLICY "Users can delete own transactions" ON "transaction" FOR DELETE USING (user_id = auth.uid()::integer);

-- Insert sample data (optional)
-- You can uncomment these lines to add sample data for testing

/*
-- Sample categories for user 1
INSERT INTO "category" (user_id, name, category_type, color) VALUES
(1, 'Salary', 'income', '#28a745'),
(1, 'Freelance', 'income', '#17a2b8'),
(1, 'Food & Dining', 'expense', '#dc3545'),
(1, 'Transportation', 'expense', '#fd7e14'),
(1, 'Shopping', 'expense', '#6f42c1');

-- Sample transactions for user 1
INSERT INTO "transaction" (user_id, category_id, amount, transaction_type, item_name, date) VALUES
(1, 1, 5000.00, 'income', 'Monthly Salary', '2024-01-15'),
(1, 2, 500.00, 'income', 'Freelance Project', '2024-01-20'),
(1, 3, 50.00, 'expense', 'Grocery Shopping', '2024-01-18'),
(1, 4, 30.00, 'expense', 'Gas', '2024-01-19'),
(1, 5, 100.00, 'expense', 'New Shoes', '2024-01-21');
*/ 