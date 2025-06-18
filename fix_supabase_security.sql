-- Fix Supabase Security Issues
-- This file addresses the "role mutable search_path" warnings

-- Drop existing functions with security issues
DROP FUNCTION IF EXISTS public.get_category_summary();
DROP FUNCTION IF EXISTS public.get_user_stats();
DROP FUNCTION IF EXISTS public.get_monthly_summary();
DROP FUNCTION IF EXISTS public.update_updated_at_column();

-- Recreate functions with proper security settings
-- Function to get category summary with secure search_path
CREATE OR REPLACE FUNCTION public.get_category_summary(
    p_user_id INTEGER DEFAULT NULL
)
RETURNS TABLE (
    category_name VARCHAR(100),
    total_amount DECIMAL(10,2),
    transaction_count INTEGER
) 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name as category_name,
        COALESCE(SUM(t.amount), 0) as total_amount,
        COUNT(t.id) as transaction_count
    FROM category c
    LEFT JOIN "transaction" t ON c.id = t.category_id
    WHERE (p_user_id IS NULL OR c.user_id = p_user_id)
    GROUP BY c.id, c.name
    ORDER BY total_amount DESC;
END;
$$;

-- Function to get user statistics with secure search_path
CREATE OR REPLACE FUNCTION public.get_user_stats(
    p_user_id INTEGER
)
RETURNS TABLE (
    total_income DECIMAL(10,2),
    total_expenses DECIMAL(10,2),
    net_balance DECIMAL(10,2),
    transaction_count INTEGER
) 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expenses,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE -t.amount END), 0) as net_balance,
        COUNT(t.id) as transaction_count
    FROM "transaction" t
    WHERE t.user_id = p_user_id;
END;
$$;

-- Function to get monthly summary with secure search_path
CREATE OR REPLACE FUNCTION public.get_monthly_summary(
    p_user_id INTEGER,
    p_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE),
    p_month INTEGER DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)
)
RETURNS TABLE (
    month_name VARCHAR(20),
    total_income DECIMAL(10,2),
    total_expenses DECIMAL(10,2),
    net_balance DECIMAL(10,2)
) 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        TO_CHAR(t.date, 'Month YYYY') as month_name,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expenses,
        COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE -t.amount END), 0) as net_balance
    FROM "transaction" t
    WHERE t.user_id = p_user_id 
    AND EXTRACT(YEAR FROM t.date) = p_year 
    AND EXTRACT(MONTH FROM t.date) = p_month
    GROUP BY TO_CHAR(t.date, 'Month YYYY');
END;
$$;

-- Function to update updated_at column with secure search_path
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- Grant appropriate permissions
GRANT EXECUTE ON FUNCTION public.get_category_summary() TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_user_stats(INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_monthly_summary(INTEGER, INTEGER, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.update_updated_at_column() TO authenticated;

-- Add updated_at columns if they don't exist
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "category" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "transaction" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create triggers for updated_at columns
DROP TRIGGER IF EXISTS update_user_updated_at ON "user";
CREATE TRIGGER update_user_updated_at
    BEFORE UPDATE ON "user"
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_category_updated_at ON "category";
CREATE TRIGGER update_category_updated_at
    BEFORE UPDATE ON "category"
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_transaction_updated_at ON "transaction";
CREATE TRIGGER update_transaction_updated_at
    BEFORE UPDATE ON "transaction"
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column(); 