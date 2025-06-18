# Vince - Updated for SQLAlchemy

# Import Flask components for main application routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
# Import datetime for date handling and calculations
from datetime import datetime, timedelta, date
# Import login decorator for protected routes
from app.decorators import login_required
# Import models for database operations
from app.models import User, Category, Transaction
# Import db from main app
from app import db
# Import database utility functions
from app.utils.database import get_transactions_by_user, get_categories_by_user_and_type, create_transaction, create_category, update_transaction, delete_transaction as delete_transaction_util, get_user_by_id, create_common_users, get_all_users, reset_user_password, check_database_connection, get_database_status
import os

# Create main blueprint for organizing application routes
main_bp = Blueprint('main', __name__)

# Simple status route that works even when database is down
@main_bp.route('/status')
def status():
    """
    Simple status endpoint that works even when database is unavailable.
    """
    return jsonify({
        'status': 'running',
        'message': 'Budge-IT app is running! Your Supabase data is safe.',
        'database': 'checking...',
        'timestamp': datetime.now().isoformat()
    }), 200

# Comprehensive database status endpoint
@main_bp.route('/db-status')
def detailed_database_status():
    """
    Comprehensive database status endpoint with detailed connection information.
    """
    try:
        # Get detailed database status
        db_status = get_database_status()
        
        # Add additional app context
        db_status.update({
            'app_status': 'running',
            'timestamp': datetime.now().isoformat(),
            'environment': 'production' if os.environ.get('DATABASE_URL') else 'development',
            'supabase_configured': bool(os.environ.get('DATABASE_URL')),
            'connection_pool_info': {
                'pool_size': db_status.get('pool_size', 'unknown'),
                'checked_in': db_status.get('checked_in', 'unknown'),
                'checked_out': db_status.get('checked_out', 'unknown')
            } if db_status.get('status') == 'connected' else 'connection_failed'
        })
        
        # Determine HTTP status code
        status_code = 200 if db_status.get('status') == 'connected' else 503
        
        return jsonify(db_status), status_code
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Database status check failed',
            'timestamp': datetime.now().isoformat(),
            'note': 'Your Supabase data is still safe - this is just a connection issue'
        }), 500

# Health check endpoint to monitor database status
@main_bp.route('/health')
def health_check():
    """
    Health check endpoint to monitor database and app status.
    """
    try:
        from app.utils.database import check_database_connection
        
        # Check database connection
        db_healthy = check_database_connection()
        
        health_status = {
            'status': 'healthy' if db_healthy else 'degraded',
            'database': 'connected' if db_healthy else 'connection_limited',
            'message': 'Your Supabase data is safe and accessible' if db_healthy else 'Supabase connection limited - your data is safe, try again in 15-30 minutes',
            'timestamp': datetime.now().isoformat()
        }
        
        status_code = 200 if db_healthy else 503
        return jsonify(health_status), status_code
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database': 'unknown',
            'message': f'Health check failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# Test endpoint to verify database connection
@main_bp.route('/test')
def test_endpoint():
    """
    Test endpoint to verify the application is working.
    
    Returns:
        dict: Test response with database status
    """
    try:
        from app.models import User
        user_count = User.query.count()
        return jsonify({
            'status': 'working',
            'database': 'connected',
            'user_count': user_count,
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Application is working correctly!'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Database connection failed'
        }), 500

# Database connection test endpoint
@main_bp.route('/test-db')
def test_database():
    """
    Test database connection and return status.
    
    Returns:
        dict: Database connection status
    """
    try:
        from app.models import User
        user_count = User.query.count()
        
        # Check if we're using Supabase or SQLite
        database_uri = db.engine.url
        
        return jsonify({
            'status': 'connected',
            'database_type': 'postgresql' if 'postgresql' in str(database_uri) else 'sqlite',
            'database_uri': str(database_uri).replace(str(database_uri.password), '***') if database_uri.password else str(database_uri),
            'user_count': user_count,
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Database connection successful'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Database connection failed'
        }), 500

# Route to check Supabase connection specifically
@main_bp.route('/check-supabase')
def check_supabase():
    """
    Check if Supabase connection is available and working.
    
    Returns:
        dict: Supabase connection status
    """
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            return jsonify({
                'status': 'not_configured',
                'message': 'No DATABASE_URL environment variable found'
            }), 200
        
        if not database_url.startswith('postgresql://'):
            return jsonify({
                'status': 'not_supabase',
                'message': 'DATABASE_URL is not a PostgreSQL connection string'
            }), 200
        
        # Try to connect to Supabase
        from app.models import User
        user_count = User.query.count()
        
        return jsonify({
            'status': 'connected',
            'message': f'Supabase connection successful! Found {user_count} users.',
            'user_count': user_count,
            'database_url': database_url[:50] + '...' if len(database_url) > 50 else database_url
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Supabase connection failed',
            'suggestion': 'Your data is still safe in Supabase. The issue is connection limits.',
            'solution': 'Wait for connection limits to reset or upgrade Supabase plan'
        }), 500

# Route to show database status and help with Supabase issues
@main_bp.route('/database-status')
def database_status():
    """
    Show detailed database status and help with Supabase issues.
    
    Returns:
        dict: Detailed database status
    """
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        # Check if we're using Supabase or SQLite
        from app.models import User
        database_uri = db.engine.url
        
        # Try to get user count
        user_count = User.query.count()
        
        return jsonify({
            'status': 'connected',
            'database_type': 'postgresql' if 'postgresql' in str(database_uri) else 'sqlite',
            'database_uri': str(database_uri).replace(str(database_uri.password), '***') if database_uri.password else str(database_uri),
            'user_count': user_count,
            'environment_url': database_url[:50] + '...' if database_url and len(database_url) > 50 else database_url,
            'message': 'Database connection successful',
            'note': 'If this is SQLite, your Supabase data is still safe but not accessible due to connection limits'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Database connection failed',
            'supabase_data_safe': True,
            'issue': 'Connection limits reached',
            'solution': 'Wait for limits to reset or upgrade Supabase plan'
        }), 500

# Route: / - Entry point, redirects based on authentication status
@main_bp.route('/')
def index():
    """
    Handles the root route and redirects users appropriately.
    
    This route serves as the entry point to the application. It checks if
    a user is logged in and redirects them to the appropriate dashboard
    (admin or regular) based on their role. Non-authenticated users are
    shown the login page.
    
    Returns:
        str: Redirect response or rendered login template
    """
    # Check if user is logged in
    if 'user_id' in session:
        # Redirect admin users to admin dashboard, others to regular dashboard
        if session.get('username') == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    # Show login page for non-authenticated users
    return render_template('login.html')

# Route: /dashboard - Shows user's financial overview and summary
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the main user dashboard with financial overview.
    
    This route shows the user's financial summary including total income
    and expenses. It requires user authentication and provides the main
    interface for viewing financial data.
    
    Returns:
        str: Rendered dashboard template with financial summary
    """
    try:
        # Get current user ID from session
        user_id = session['user_id']
        # Get all transactions for current user
        user_transactions = get_transactions_by_user(user_id)

        # Calculate total income and expenses for user
        total_income = sum(t.amount for t in user_transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in user_transactions if t.transaction_type == 'expense')

        # Render dashboard with financial summary
        return render_template('dashboard.html',
                               total_income=total_income,
                               total_expense=total_expense)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in dashboard route: {e}")
        
        # Return fallback values if database connection fails
        return render_template('dashboard.html',
                               total_income=0,
                               total_expense=0)

# Route: /income - Shows income entry form with user's income categories
@main_bp.route('/income')
@login_required
def income():
    """
    Displays the income entry page with user's income categories.
    
    This route shows the income form along with all income categories
    available to the current user for adding new income transactions.
    
    Returns:
        str: Rendered income template with categories
    """
    try:
        # Get current user ID and income categories
        user_id = session['user_id']
        income_categories = get_categories_by_user_and_type(user_id, 'income')
        
        # Convert categories to the format expected by the frontend
        categories_data = []
        for category in income_categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'type': category.category_type,
                'color': category.color
            })
        
        # Render income page with categories
        return render_template('income.html', income_categories=categories_data)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in income route: {e}")
        
        # Return empty categories if database connection fails
        return render_template('income.html', income_categories=[])

# Route: /expense - Shows expense entry form with user's expense categories
@main_bp.route('/expense')
@login_required
def expense():
    """
    Displays the expense entry page with user's expense categories.
    
    This route shows the expense form along with all expense categories
    available to the current user for adding new expense transactions.
    
    Returns:
        str: Rendered expense template with categories
    """
    try:
        # Get current user ID and expense categories
        user_id = session['user_id']
        expense_categories = get_categories_by_user_and_type(user_id, 'expense')
        
        # Convert categories to the format expected by the frontend
        categories_data = []
        for category in expense_categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'type': category.category_type,
                'color': category.color
            })
        
        # Render expense page with categories
        return render_template('expense.html', expense_categories=categories_data)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in expense route: {e}")
        
        # Return empty categories if database connection fails
        return render_template('expense.html', expense_categories=[])

# Route: /add_transaction - Creates new income or expense transaction
@main_bp.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    """
    Handles the creation of new financial transactions.
    """
    # Get current user ID and form data
    user_id = session['user_id']
    amount = float(request.form['amount'])
    category_id = int(request.form['category_id'])
    transaction_type = request.form['type']
    date_str = request.form['date']
    item_name = request.form['Item Name']

    # Validate that category exists and belongs to user
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        return redirect(url_for('main.dashboard'))

    # Create new transaction in database
    from datetime import datetime
    transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    new_transaction = create_transaction(user_id, amount, category_id, transaction_type, transaction_date, item_name)
    
    if new_transaction:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('main.dashboard'))

# Route: /history - Shows transaction history page with filtering options
@main_bp.route('/history')
@login_required
def history():
    """
    Displays the transaction history page for the current user.
    
    This route shows all transactions for the user with filtering capabilities
    by date range, transaction type, and category. It also provides
    transaction management features like editing and deletion.
    
    Returns:
        str: Rendered history template with user's transactions and categories
    """
    # Get current user ID and query parameters
    user_id = session['user_id']
    period = request.args.get('period', 'month')  # Default to month
    start_date = request.args.get('start_date') or request.args.get('start')
    end_date = request.args.get('end_date') or request.args.get('end')
    transaction_type = request.args.get('type')
    category_id = request.args.get('category_id')
    
    # Get all transactions for the user
    transactions = get_transactions_by_user(user_id)
    print(f"DEBUG: Found {len(transactions)} total transactions for user {user_id}")
    print(f"DEBUG: Period: {period}, Start: {start_date}, End: {end_date}")
    
    # Apply filters
    filtered_transactions = []
    for transaction in transactions:
        try:
            # Date filtering - only apply if period is 'custom' or if specific dates are provided
            if period == 'custom' and (start_date or end_date):
                if start_date:
                    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                    if transaction.date < start_dt:
                        continue
                if end_date:
                    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                    if transaction.date > end_dt:
                        continue
            elif period != 'all':  # Apply period-based filtering for non-custom periods
                today = datetime.now().date()
                if period == 'today':
                    if transaction.date != today:
                        continue
                elif period == 'week':
                    week_start = today - timedelta(days=today.weekday())
                    if transaction.date < week_start:
                        continue
                elif period == 'month':
                    month_start = today.replace(day=1)
                    if transaction.date < month_start:
                        continue
                elif period == 'year':
                    year_start = today.replace(month=1, day=1)
                    if transaction.date < year_start:
                        continue
            
            # Transaction type filtering
            if transaction_type and transaction_type != 'both' and transaction.transaction_type != transaction_type:
                continue
            
            # Category filtering
            if category_id and str(transaction.category_id) != category_id:
                continue
                
            filtered_transactions.append(transaction)
        except Exception as e:
            print(f"DEBUG: Error filtering transaction {transaction.id}: {e}")
            filtered_transactions.append(transaction)

    print(f"DEBUG: After filtering: {len(filtered_transactions)} transactions")

    # Enhance transactions with category name and color if not already present
    for transaction in filtered_transactions:
        category_id = getattr(transaction, 'category_id', None)
        if category_id is not None:
            # Get category information for transaction
            category = Category.query.filter_by(id=category_id, user_id=user_id).first()
            if category:
                transaction.category_name = category.name
                transaction.category_color = category.color
            else:
                transaction.category_name = 'Uncategorized'
                transaction.category_color = '#6c757d'
        else:
            transaction.category_name = 'Uncategorized'
            transaction.category_color = '#6c757d'

    # Sort transactions by date, most recent first
    filtered_transactions.sort(key=lambda x: x.date if hasattr(x, 'date') else datetime.fromisoformat(x['date']), reverse=True)
    
    # Get categories for the edit modal
    income_categories = get_categories_by_user_and_type(user_id, 'income')
    expense_categories = get_categories_by_user_and_type(user_id, 'expense')
    
    # Convert categories to the format expected by the frontend
    all_categories = []
    for category in income_categories:
        all_categories.append({
            'id': category.id,
            'name': category.name,
            'type': category.category_type,
            'color': category.color
        })
    for category in expense_categories:
        all_categories.append({
            'id': category.id,
            'name': category.name,
            'type': category.category_type,
            'color': category.color
        })
    
    print(f"DEBUG: Final transactions to render: {len(filtered_transactions)}")
    return render_template('history.html', transactions=filtered_transactions, all_categories=all_categories)

# Route: /edit_transaction/<transaction_id> - Updates existing transaction details
@main_bp.route('/edit_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def edit_transaction(transaction_id):
    """
    Handles the updating of existing transactions.
    
    This route processes form submissions to modify transaction details
    including amount, item name, date, and category. It validates the
    transaction belongs to the user and handles category changes.
    
    Args:
        transaction_id: ID of the transaction to be updated
    
    Returns:
        str: Redirect response to history page with success/error message
    """
    # Get current user ID and form data
    user_id = session['user_id']
    
    try:
        # Get form data for transaction update
        amount = float(request.form['amount'])
        item_name = request.form['item_name']
        date = request.form['date']
        new_category_id = request.form['category_id']
        transaction_type = request.form['type']

        # Update transaction using new utility function
        if update_transaction(transaction_id, user_id, amount, item_name, date, new_category_id, transaction_type):
            return redirect(url_for('main.history'))
        else:
            return redirect(url_for('main.history'))
    except ValueError:
        # Handle invalid amount input
        return redirect(url_for('main.history'))
    except Exception as e:
        # Handle any other errors
        return redirect(url_for('main.history'))

# Route: /delete_transaction/<transaction_id> - Removes transaction from database
@main_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """
    Handles the deletion of transactions.
    
    This route processes requests to delete transactions and provides
    confirmation feedback. It ensures only the transaction owner can
    delete their transactions. Supports both regular form submissions
    and AJAX requests.
    
    Args:
        transaction_id: ID of the transaction to be deleted
    
    Returns:
        str: Redirect response to history page with success/error message
        or JSON response for AJAX requests
    """
    # Get current user ID
    user_id = session['user_id']
    
    # Delete transaction using utility function (with alias to avoid naming conflict)
    deleted_transaction = delete_transaction_util(transaction_id, user_id)
    
    # Check if this is an AJAX request
    if request.headers.get('Content-Type') == 'application/json':
        if deleted_transaction:
            return jsonify({'success': True, 'message': f"{deleted_transaction['type'].capitalize()} transaction deleted successfully!"})
        else:
            return jsonify({'success': False, 'message': 'Transaction not found or unauthorized.'})
    
    # Regular form submission
    return redirect(url_for('main.history'))

# Route: /categories - Shows category management page for user
@main_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    """
    Displays the category management page for the current user.
    
    This route shows all income and expense categories for the user,
    allowing them to view, add, edit, and delete categories.
    
    Returns:
        str: Rendered categories template with user's categories
    """
    user_id = session['user_id']
    income_categories = get_categories_by_user_and_type(user_id, 'income')
    expense_categories = get_categories_by_user_and_type(user_id, 'expense')
    return render_template('categories.html', income_categories=income_categories, expense_categories=expense_categories)

# Route: /add_category - Creates new income or expense transaction
@main_bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    """
    Handles the creation of new categories.

    This route processes form submissions to create new income or expense
    categories. It validates that all required fields are provided and
    checks for duplicate category names within the same type.

    Returns:
        str: Redirect response to categories page with success/error message
    """
    try:
        # Get current user ID and form data
        user_id = session['user_id']
        name = request.form['name']
        category_type = request.form['type']
        color = request.form['color']

        # Basic validation for required fields
        if not name or not category_type or not color:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.categories'))

        # Check if category name already exists for this user and type
        existing_categories = get_categories_by_user_and_type(user_id, category_type)
        if any(c.name.lower() == name.lower() for c in existing_categories):
            flash('Category with this name already exists for this type!', 'danger')
            return redirect(url_for('main.categories'))

        # Create new category in database
        new_category = create_category(user_id, name, category_type, color)
        if new_category:
            flash('Category added successfully!', 'success')
        else:
            flash('Failed to add category due to a database error.', 'danger')

    except Exception as e:
        # Catch any other unexpected errors in this route
        flash(f'An unexpected error occurred: {e}', 'danger')
        print(f"Error in add_category route: {e}") # For server-side debugging

    return redirect(url_for('main.categories'))

# Route: /edit_category/<category_id> - Shows edit form (GET) or updates category (POST)
@main_bp.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """
    Handles the editing of existing categories.
    
    This route displays the category edit form for GET requests and
    processes updates for POST requests. It validates category ownership
    and checks for duplicate names.
    
    Args:
        category_id: ID of the category to be edited
    
    Returns:
        str: Rendered edit template or redirect response
    """
    # Get current user ID and find category to edit
    user_id = session['user_id']
    category_to_edit = Category.query.filter_by(id=category_id, user_id=user_id).first()

    # Check if category exists and belongs to user
    if not category_to_edit:
        return redirect(url_for('main.categories'))

    if request.method == 'POST':
        try:
            # Get form data for category update
            new_name = request.form['name']
            new_type = request.form['type']
            new_color = request.form['color']

            # Check for duplicate name for the same user and type, excluding the current category being edited
            existing_categories = get_categories_by_user_and_type(user_id, new_type)
            if any(c.name.lower() == new_name.lower() and c.id != category_id for c in existing_categories):
                return redirect(url_for('main.categories'))
            else:
                # Update category in database
                category_to_edit.name = new_name
                category_to_edit.category_type = new_type
                category_to_edit.color = new_color
                from app.utils.database import save_database
                save_database()
                return redirect(url_for('main.categories'))
        except Exception as e:
            # Handle any errors during update
            return redirect(url_for('main.categories'))
    
    # Render edit category template for GET requests
    return render_template('edit_category.html', category=category_to_edit)

# Route: /delete_category/<category_id> - Removes category and updates related transactions
@main_bp.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """
    Handles the deletion of categories.
    
    This route processes requests to delete categories and updates all
    related transactions to be marked as 'Uncategorized'. It ensures
    only the category owner can delete their categories.
    
    Args:
        category_id: ID of the category to be deleted
    
    Returns:
        str: Redirect response to categories page with success/error message
    """
    # Get current user ID
    user_id = session['user_id']
    
    # Find and delete category
    category_to_delete = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if category_to_delete:
        from app.utils.database import save_database
        from app.models import db
        db.session.delete(category_to_delete)
        save_database()
    return redirect(url_for('main.categories'))

# Route: /get_chart_data/<chart_type> - Returns JSON data for financial charts
@main_bp.route('/get_chart_data/<string:chart_type>', methods=['GET'])
@login_required
def get_chart_data(chart_type):
    """
    Provides chart data for financial visualization.
    
    This route generates JSON data for charts based on the user's transactions.
    It supports different time periods (today, week, month, year) and modes
    (individual transactions or category aggregation). The data is used for
    creating pie charts and other visualizations.
    
    Args:
        chart_type: Type of chart data ('all', 'income', 'expense')
    
    Returns:
        JSON: Chart data formatted for visualization libraries
    """
    user_id = session['user_id']
    period = request.args.get('period', 'month')
    mode = request.args.get('mode', 'category')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    user_transactions = get_transactions_by_user(user_id)
    now = datetime.now()
    today = now.date()
    end_date_filter = today
    start_date_filter = None

    if period == 'today':
        start_date_filter = today
        end_date_filter = today
    elif period == 'week':
        start_date_filter = today - timedelta(days=today.weekday())
    elif period == 'month':
        start_date_filter = today.replace(day=1)
    elif period == 'year':
        start_date_filter = today.replace(month=1, day=1)
    elif period == 'custom' and start_date and end_date:
        try:
            start_date_filter = datetime.fromisoformat(start_date).date()
            end_date_filter = datetime.fromisoformat(end_date).date()
        except ValueError:
            start_date_filter = None
            end_date_filter = today

    filtered_transactions = []
    for t in user_transactions:
        try:
            t_date = t.date if isinstance(t.date, date) else t.date.date()
            if start_date_filter is None or (start_date_filter <= t_date <= end_date_filter):
                filtered_transactions.append(t)
        except Exception as e:
            print(f"Date filter error: {e}")
            continue

    # Fallback: if no data, return all transactions for debugging
    if not filtered_transactions:
        print("No transactions matched filter, returning all for debugging.")
        filtered_transactions = user_transactions

    chart_data = []
    if mode == 'individual':
        for transaction in filtered_transactions:
            if chart_type == 'all' or transaction.transaction_type == chart_type:
                label = transaction.item_name.strip() if transaction.item_name else ''
                if not label:
                    category = Category.query.filter_by(id=transaction.category_id, user_id=user_id).first()
                    category_name = category.name if category else 'Uncategorized'
                    label = f"{transaction.date.strftime('%Y-%m-%d')} - {category_name}"
                amount_value = float(transaction.amount)
                category = Category.query.filter_by(id=transaction.category_id, user_id=user_id).first()
                chart_data.append({
                    'name': label,
                    'value': amount_value,
                    'color': category.color if category else '#6c757d',
                    'original_type': transaction.transaction_type
                })
        print(f"Chart type: {chart_type}, Mode: {mode}, Data count: {len(chart_data)}")
    else:
        category_summary = {}
        for transaction in filtered_transactions:
            if chart_type == 'all' or transaction.transaction_type == chart_type:
                category_id = transaction.category_id
                if category_id:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    if category:
                        name = category.name
                        color = category.color
                        amount_for_chart = float(transaction.amount) if transaction.transaction_type == 'income' else -float(transaction.amount)
                        if name not in category_summary:
                            category_summary[name] = {'value': 0, 'color': color, 'type': transaction.transaction_type}
                        category_summary[name]['value'] += amount_for_chart
                    else:
                        name = 'Uncategorized'
                        color = '#6c757d'
                        amount_for_chart = float(transaction.amount) if transaction.transaction_type == 'income' else -float(transaction.amount)
                        if name not in category_summary:
                            category_summary[name] = {'value': 0, 'color': color, 'type': transaction.transaction_type}
                        category_summary[name]['value'] += amount_for_chart
                else:
                    name = 'Uncategorized'
                    color = '#6c757d'
                    amount_for_chart = float(transaction.amount) if transaction.transaction_type == 'income' else -float(transaction.amount)
                    if name not in category_summary:
                        category_summary[name] = {'value': 0, 'color': color, 'type': transaction.transaction_type}
                    category_summary[name]['value'] += amount_for_chart
        chart_data = [{'name': name, 'value': summary['value'], 'color': summary['color'], 'type': summary['type']} 
                      for name, summary in category_summary.items()]
        if chart_type != 'all':
            chart_data = [{'name': item['name'], 'value': abs(item['value']), 'color': item['color']} for item in chart_data]
        print(f"Chart type: {chart_type}, Mode: {mode}, Data count: {len(chart_data)}")
    return jsonify(chart_data)

# New endpoint for line graph data
@main_bp.route('/get_line_data/<string:chart_type>', methods=['GET'])
@login_required
def get_line_data(chart_type):
    user_id = session['user_id']
    period = request.args.get('period', 'month')
    user_transactions = get_transactions_by_user(user_id)
    now = datetime.now()
    today = now.date()
    start_date_filter = today.replace(day=1) if period == 'month' else today.replace(month=1, day=1)
    # Group by date
    date_totals = {}
    for t in user_transactions:
        if chart_type == 'all' or t.transaction_type == chart_type:
            t_date = t.date if isinstance(t.date, date) else t.date.date()
            if t_date >= start_date_filter:
                date_str = t_date.strftime('%Y-%m-%d')
                date_totals.setdefault(date_str, 0)
                date_totals[date_str] += float(t.amount)
    # Sort by date
    sorted_dates = sorted(date_totals.keys())
    data = {
        'labels': sorted_dates,
        'values': [date_totals[d] for d in sorted_dates]
    }
    return jsonify(data)

# Route: /account - Shows user account statistics and information
@main_bp.route('/account')
@login_required
def account():
    """
    Displays the user's account information and statistics.
    
    This route shows comprehensive account information including total
    income, expenses, transaction count, and account creation date.
    It provides users with an overview of their financial activity.
    
    Returns:
        str: Rendered account template with user statistics
    """
    try:
        # Get current user ID and transaction data
        user_id = session['user_id']
        user_transactions = get_transactions_by_user(user_id)
        
        # Calculate account statistics
        all_time_income = sum(t.amount for t in user_transactions if t.transaction_type == 'income')
        all_expense = sum(t.amount for t in user_transactions if t.transaction_type == 'expense')
        total_transactions = len(user_transactions)

        # Get user creation date - handle missing created_at field
        user_info = User.query.get(user_id)
        member_since = user_info.created_at.isoformat() if user_info and user_info.created_at else 'N/A'
        
        # Render account page with user statistics
        return render_template('account.html',
                               total_income=all_time_income,
                               total_expense=all_expense,
                               total_transactions=total_transactions,
                               member_since=member_since)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in account route: {e}")
        
        # Return fallback values if database connection fails
        return render_template('account.html',
                               total_income=0,
                               total_expense=0,
                               total_transactions=0,
                               member_since='N/A')

# Route: /about - Shows application information and features
@main_bp.route('/about')
def about():
    """
    Displays the about page with application information.
    
    This route shows general information about the budget tracking
    application and its features.
    
    Returns:
        str: Rendered about template
    """
    # Render about page
    return render_template('about.html')

# Route: /contact - Shows contact information and team details
@main_bp.route('/contact')
def contact():
    """
    Displays the contact page with team information.
    
    This route shows contact details and information about the development
    team. It's accessible to all users without authentication.
    
    Returns:
        str: Rendered contact template
    """
    return render_template('contact.html')

# Route: /member/<member> - Shows individual team member profile
@main_bp.route('/member/<member>')
def member_profile(member):
    """
    Displays individual team member profile pages.
    
    This route shows detailed information about each team member including
    their role, skills, and contributions to the project. It's accessible
    to all users without authentication.
    
    Args:
        member: String identifier for the team member (vince, marwin, vinz, nika, anthony)
    
    Returns:
        str: Rendered member profile template or 404 if member not found
    """
    # Define valid member identifiers
    valid_members = ['vince', 'marwin', 'vinz', 'nika', 'anthony']
    
    # Check if the member parameter is valid
    if member not in valid_members:
        return render_template('404.html'), 404
    
    # Render the appropriate member profile template
    return render_template(f'members/{member}.html')

# Route: /get_categories - Returns user's categories as JSON for AJAX requests
@main_bp.route('/get_categories')
@login_required
def get_categories():
    """
    Provides category data for AJAX requests.
    
    This route returns all categories for the current user in JSON format,
    useful for dynamic form population and AJAX functionality.
    
    Returns:
        JSON: List of user's categories
    """
    user_id = session['user_id']
    income_categories = get_categories_by_user_and_type(user_id, 'income')
    expense_categories = get_categories_by_user_and_type(user_id, 'expense')
    
    # Convert categories to the format expected by the frontend
    categories_data = []
    
    for category in income_categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'type': category.category_type,
            'color': category.color
        })
    
    for category in expense_categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'type': category.category_type,
            'color': category.color
        })
    
    # Return categories as JSON for AJAX requests
    return jsonify(categories_data)

# Route to create common users
@main_bp.route('/create-users')
def create_users():
    """
    Create common users for testing and recovery.
    
    Returns:
        dict: Response with user creation status
    """
    try:
        from app.utils.database import create_common_users, get_all_users
        
        # Create common users
        created_count = create_common_users()
        
        # Get all users
        all_users = get_all_users()
        user_list = []
        for user in all_users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'status': 'success',
            'created_count': created_count,
            'total_users': len(all_users),
            'users': user_list,
            'message': f'Created {created_count} new users. Total users: {len(all_users)}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to create users'
        }), 500

# Route to list all users
@main_bp.route('/list-users')
def list_users():
    """
    List all users in the database.
    
    Returns:
        dict: Response with user list
    """
    try:
        from app.utils.database import get_all_users
        
        all_users = get_all_users()
        user_list = []
        for user in all_users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'status': 'success',
            'total_users': len(all_users),
            'users': user_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to list users'
        }), 500

# Route to reset user password
@main_bp.route('/reset-password/<username>/<new_password>')
def reset_password(username, new_password):
    """
    Reset a user's password.
    
    Args:
        username: Username of the user
        new_password: New password to set
    
    Returns:
        dict: Response with password reset status
    """
    try:
        from app.utils.database import reset_user_password
        
        success = reset_user_password(username, new_password)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Password reset successful for user {username}'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'User {username} not found'
            }), 404
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to reset password'
        }), 500 