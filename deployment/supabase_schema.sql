-- Budget Tracker Database Schema for Supabase
-- Copy and paste this entire script into Supabase SQL Editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('income', 'expense')),
    color VARCHAR(7) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('income', 'expense')),
    date DATE NOT NULL,
    item_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);
CREATE INDEX IF NOT EXISTS idx_categories_type ON categories(category_type);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_category_id ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users table (simplified for Flask app)
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own data" ON users
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own data" ON users
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete their own data" ON users
    FOR DELETE USING (true);

-- Create RLS policies for categories table (simplified for Flask app)
CREATE POLICY "Users can view their own categories" ON categories
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own categories" ON categories
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own categories" ON categories
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete their own categories" ON categories
    FOR DELETE USING (true);

-- Create RLS policies for transactions table (simplified for Flask app)
CREATE POLICY "Users can view their own transactions" ON transactions
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own transactions" ON transactions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own transactions" ON transactions
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete their own transactions" ON transactions
    FOR DELETE USING (true);

-- Create functions for better data management

-- Function to get user statistics
CREATE OR REPLACE FUNCTION get_user_stats(user_id_param INTEGER)
RETURNS TABLE (
    total_income DECIMAL(10,2),
    total_expenses DECIMAL(10,2),
    net_balance DECIMAL(10,2),
    transaction_count INTEGER,
    category_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expenses,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE -t.amount END), 0) as net_balance,
        COUNT(t.id) as transaction_count,
        COUNT(DISTINCT c.id) as category_count
    FROM users u
    LEFT JOIN categories c ON u.id = c.user_id
    LEFT JOIN transactions t ON u.id = t.user_id
    WHERE u.id = user_id_param
    GROUP BY u.id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get monthly summary
CREATE OR REPLACE FUNCTION get_monthly_summary(user_id_param INTEGER, year_param INTEGER, month_param INTEGER)
RETURNS TABLE (
    month_year TEXT,
    total_income DECIMAL(10,2),
    total_expenses DECIMAL(10,2),
    net_balance DECIMAL(10,2),
    transaction_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        TO_CHAR(DATE(year_param || '-' || month_param || '-01'), 'Month YYYY') as month_year,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expenses,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE -t.amount END), 0) as net_balance,
        COUNT(t.id) as transaction_count
    FROM transactions t
    WHERE t.user_id = user_id_param
    AND EXTRACT(YEAR FROM t.date) = year_param
    AND EXTRACT(MONTH FROM t.date) = month_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get category summary
CREATE OR REPLACE FUNCTION get_category_summary(user_id_param INTEGER, start_date DATE, end_date DATE)
RETURNS TABLE (
    category_name VARCHAR(100),
    category_type VARCHAR(20),
    category_color VARCHAR(7),
    total_amount DECIMAL(10,2),
    transaction_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name as category_name,
        c.category_type,
        c.color as category_color,
        COALESCE(SUM(t.amount), 0) as total_amount,
        COUNT(t.id) as transaction_count
    FROM categories c
    LEFT JOIN transactions t ON c.id = t.category_id 
        AND t.date BETWEEN start_date AND end_date
    WHERE c.user_id = user_id_param
    GROUP BY c.id, c.name, c.category_type, c.color
    ORDER BY total_amount DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.created_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers to all tables
CREATE TRIGGER update_users_created_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_created_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_created_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data (optional - remove if you don't want sample data)
-- INSERT INTO users (username, email, password_hash) VALUES 
-- ('demo_user', 'demo@example.com', 'hashed_password_here');

-- INSERT INTO categories (user_id, name, category_type, color) VALUES 
-- (1, 'Salary', 'income', '#28a745'),
-- (1, 'Freelance', 'income', '#17a2b8'),
-- (1, 'Food', 'expense', '#dc3545'),
-- (1, 'Transportation', 'expense', '#ffc107'),
-- (1, 'Entertainment', 'expense', '#6f42c1');

-- INSERT INTO transactions (user_id, category_id, amount, transaction_type, date, item_name) VALUES 
-- (1, 1, 5000.00, 'income', CURRENT_DATE - INTERVAL '30 days', 'Monthly Salary'),
-- (1, 3, 150.00, 'expense', CURRENT_DATE - INTERVAL '5 days', 'Grocery Shopping'),
-- (1, 4, 50.00, 'expense', CURRENT_DATE - INTERVAL '3 days', 'Gas Station');

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;

-- Display success message
SELECT 'Budget Tracker database schema created successfully!' as status; 