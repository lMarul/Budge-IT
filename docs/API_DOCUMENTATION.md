# Budget Tracker System - API Documentation

## Overview

The Budget Tracker System provides a RESTful API for managing personal finances. This documentation covers all available endpoints, request/response formats, and authentication requirements.

## Base URL

- **Development**: `http://127.0.0.1:5001`
- **Production**: `https://your-domain.com`

## Authentication

The API uses session-based authentication. Users must be logged in to access protected endpoints.

### Authentication Flow

1. **Register**: `POST /register`
2. **Login**: `POST /login`
3. **Session**: Maintained via Flask session
4. **Logout**: `GET /logout`

## Error Responses

All endpoints may return the following error responses:

```json
{
  "error": "Error message",
  "status": "error"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## Authentication Endpoints

### Register User

**POST** `/register`

Creates a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "confirm_password": "string"
}
```

**Response:**
- Success: Redirect to login page
- Error: Flash message with error details

**Validation Rules:**
- Username: 3-20 characters, unique
- Email: Valid email format
- Password: Minimum 6 characters
- Confirm password: Must match password

### Login User

**POST** `/login`

Authenticates user and creates session.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
- Success: Redirect to dashboard
- Error: Flash message with error details

### Logout User

**GET** `/logout`

Ends user session and clears preferences.

**Response:**
- Success: Redirect to login page
- Clears dark mode preference from localStorage

## Main Application Endpoints

### Dashboard

**GET** `/dashboard`

Returns the main dashboard with financial overview.

**Response:**
- HTML template with financial summary
- Requires authentication

### Add Transaction

**POST** `/add_transaction`

Creates a new income or expense transaction.

**Request Body:**
```json
{
  "amount": "number",
  "category_id": "number",
  "type": "income|expense",
  "date": "YYYY-MM-DD",
  "Item Name": "string"
}
```

**Response:**
- Success: Redirect to income/expense page
- Error: Flash message with error details

**Validation Rules:**
- Amount: Positive number
- Category ID: Must belong to user
- Type: Must be "income" or "expense"
- Date: Valid date format

### Get Categories

**GET** `/get_categories`

Returns all categories for the current user.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Salary",
    "type": "income",
    "color": "#28a745"
  }
]
```

### Get Chart Data

**GET** `/get_chart_data/{chart_type}?period={period}&mode={mode}`

Returns chart data for visualization.

**Parameters:**
- `chart_type`: "income", "expense", or "all"
- `period`: "today", "week", "month", "year", or "all"
- `mode`: "category" or "individual"

**Response:**
```json
[
  {
    "name": "Category Name",
    "value": 1000.00,
    "color": "#28a745",
    "type": "income"
  }
]
```

### Transaction History

**GET** `/history`

Returns all transactions for the current user.

**Response:**
- HTML template with transaction table
- Sorted by date (newest first)

### Edit Transaction

**POST** `/edit_transaction/{transaction_id}`

Updates an existing transaction.

**Request Body:**
```json
{
  "amount": "number",
  "item_name": "string",
  "date": "YYYY-MM-DD",
  "category_id": "number",
  "type": "income|expense"
}
```

**Response:**
- Success: Redirect to history page
- Error: Flash message with error details

### Delete Transaction

**POST** `/delete_transaction/{transaction_id}`

Deletes a transaction.

**Headers (for AJAX):**
```
Content-Type: application/json
```

**Response:**
- **AJAX**: JSON response with success/error status
- **Form**: Redirect to history page with flash message

### Categories Management

**GET** `/categories`

Returns category management page.

**POST** `/add_category`

Creates a new category.

**Request Body:**
```json
{
  "name": "string",
  "type": "income|expense",
  "color": "#hexcolor"
}
```

**POST** `/edit_category/{category_id}`

Updates an existing category.

**Request Body:**
```json
{
  "name": "string",
  "type": "income|expense",
  "color": "#hexcolor"
}
```

**POST** `/delete_category/{category_id}`

Deletes a category and updates related transactions.

## Admin Endpoints

### Admin Dashboard

**GET** `/admin`

Returns admin dashboard with system statistics.

**Response:**
- HTML template with system overview
- Requires admin authentication

### User Management

**GET** `/admin/users`

Returns user management page.

**POST** `/admin/edit_user/{user_id}`

Updates user information.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**POST** `/admin/delete_user/{user_id}`

Deletes user and all associated data.

### Database Viewer

**GET** `/admin/database`

Returns database viewer with all system data.

**Response:**
- HTML template with tabbed data view
- Users, categories, and transactions tables

## Static Pages

### About Page

**GET** `/about`

Returns about page with application information.

### Contact Page

**GET** `/contact`

Returns contact page with team information.

### Team Member Profiles

**GET** `/member/{member}`

Returns individual team member profile.

**Parameters:**
- `member`: "vince", "marwin", "vinz", "nika", or "anthony"

## Data Models

### User Model

```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "password_hash": "hashed_string",
  "created_at": "ISO_datetime"
}
```

### Category Model

```json
{
  "id": 1,
  "user_id": 1,
  "name": "string",
  "type": "income|expense",
  "color": "#hexcolor"
}
```

### Transaction Model

```json
{
  "id": 1,
  "user_id": 1,
  "amount": 1000.00,
  "category_id": 1,
  "category_name": "string",
  "category_color": "#hexcolor",
  "type": "income|expense",
  "date": "YYYY-MM-DD",
  "item_name": "string",
  "created_at": "ISO_datetime"
}
```

## Security Considerations

### Input Validation
- All user inputs are validated on both client and server side
- SQL injection protection through parameterized queries
- XSS protection through output encoding

### Authentication
- Session-based authentication with secure session management
- Password hashing using Werkzeug security functions
- Route protection with decorators

### Authorization
- Users can only access their own data
- Admin routes require admin privileges
- Proper error handling for unauthorized access

## Rate Limiting

Currently, the API does not implement rate limiting. For production deployment, consider implementing:

- Request rate limiting per user
- API key authentication for external access
- Request logging and monitoring

## CORS Policy

The API does not implement CORS headers as it's designed for same-origin requests. For cross-origin access, add appropriate CORS headers.

## Versioning

The current API version is v1.0. Future versions will be indicated in the URL path (e.g., `/api/v2/`).

## Support

For API support or questions:
1. Check the application logs for detailed error messages
2. Review the data flow documentation in `data_flow.txt`
3. Contact the development team through the contact page

---

*Last updated: December 2024* 