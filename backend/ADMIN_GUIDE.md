# Admin User Management Guide

## Overview
This guide explains how to manage users as an administrator in the Event Management System.

## Initial Setup

### 1. Create Admin User
Run the admin creation script:
```bash
python create_admin.py
```

**Default Credentials:**
- Username: `admin`
- Email: `admin@ems.local`
- Password: `Admin123`

**Custom Credentials:**
```bash
python create_admin.py <username> <email> <password>
```

Example:
```bash
python create_admin.py superadmin admin@example.com MySecure123
```

### 2. Database Migration
If you encounter database errors, run the migration script:
```bash
python migrate_db.py
```

## Admin API Endpoints

All admin endpoints require the `x-admin-key` header for authentication.

**Default Admin Key:** `dev-admin-key`

To change the admin key, set the `ADMIN_API_KEY` environment variable in your `.env` file:
```
ADMIN_API_KEY=your-secure-admin-key
```

### Admin Login
**Endpoint:** `POST /admin/login`

This endpoint verifies admin credentials and returns the admin key for subsequent requests.

**Request Body:**
```json
{
  "email": "admin@ems.local",
  "password": "Admin123"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ems.local",
    "password": "Admin123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Admin login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ems.local",
    "is_admin": true
  },
  "admin_key": "dev-admin-key"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid email or password
- `403 Forbidden` - User is not an admin or account is inactive

### Authentication Header
After logging in, include the admin key in all subsequent admin requests:
```
x-admin-key: dev-admin-key
```

## User Management Endpoints

### 1. List All Users
**Endpoint:** `GET /admin/users`

**Example:**
```bash
curl -X GET http://localhost:8000/admin/users \
  -H "x-admin-key: dev-admin-key"
```

**Response:**
```json
[
  {
    "username": "admin",
    "email": "admin@ems.local",
    "is_admin": true
  },
  {
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  }
]
```

### 2. Get User by Email
**Endpoint:** `GET /admin/users/{email}`

**Example:**
```bash
curl -X GET http://localhost:8000/admin/users/john@example.com \
  -H "x-admin-key: dev-admin-key"
```

**Response:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "is_admin": false
}
```

### 3. Create New User
**Endpoint:** `POST /admin/users`

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "is_admin": false
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/users \
  -H "x-admin-key: dev-admin-key" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "SecurePass123",
    "is_admin": false
  }'
```

**Response:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "is_admin": false
}
```

### 4. Update User
**Endpoint:** `PUT /admin/users/{email}`

**Request Body (all fields optional):**
```json
{
  "username": "updatedname",
  "email": "newemail@example.com",
  "is_admin": true
}
```

**Example - Promote user to admin:**
```bash
curl -X PUT http://localhost:8000/admin/users/john@example.com \
  -H "x-admin-key: dev-admin-key" \
  -H "Content-Type: application/json" \
  -d '{
    "is_admin": true
  }'
```

**Example - Change password:**
```bash
curl -X PUT http://localhost:8000/admin/users/john@example.com \
  -H "x-admin-key: dev-admin-key" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "NewSecurePass123"
  }'
```

**Response:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "is_admin": true
}
```

### 5. Delete User
**Endpoint:** `DELETE /admin/users/{email}`

**Example:**
```bash
curl -X DELETE http://localhost:8000/admin/users/john@example.com \
  -H "x-admin-key: dev-admin-key"
```

**Response:**
```json
{
  "success": true,
  "deleted": {
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  }
}
```

## Event Management Endpoints

### Delete Event (Admin)
**Endpoint:** `DELETE /admin/events/{event_id}`

**Example:**
```bash
curl -X DELETE http://localhost:8000/admin/events/1 \
  -H "x-admin-key: dev-admin-key"
```

**Response:**
```json
{
  "success": true,
  "deleted": {
    "id": 1,
    "title": "Event Name",
    "date": "2024-12-01",
    "time": "18:00",
    "location": "Conference Hall"
  }
}
```

## Feedback Management Endpoints

### Delete Feedback (Admin)
**Endpoint:** `DELETE /admin/feedback/{feedback_id}`

**Example:**
```bash
curl -X DELETE http://localhost:8000/admin/feedback/1 \
  -H "x-admin-key: dev-admin-key"
```

## Using with Frontend

### JavaScript/Fetch Example
```javascript
// Admin login
async function adminLogin(email, password) {
  try {
    const response = await fetch('http://localhost:8000/admin/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    
    const data = await response.json();
    // Store admin key for subsequent requests
    localStorage.setItem('adminKey', data.admin_key);
    localStorage.setItem('adminUser', JSON.stringify(data.user));
    
    console.log('Login successful:', data);
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

// List all users (requires login first)
async function listUsers() {
  const adminKey = localStorage.getItem('adminKey');
  
  const response = await fetch('http://localhost:8000/admin/users', {
    method: 'GET',
    headers: {
      'x-admin-key': adminKey
    }
  });
  const users = await response.json();
  console.log(users);
  return users;
}

// Create new user
async function createUser(username, email, password, isAdmin = false) {
  const response = await fetch('http://localhost:8000/admin/users', {
    method: 'POST',
    headers: {
      'x-admin-key': 'dev-admin-key',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username,
      email,
      password,
      is_admin: isAdmin
    })
  });
  const newUser = await response.json();
  console.log(newUser);
}

// Update user
async function updateUser(email, updates) {
  const response = await fetch(`http://localhost:8000/admin/users/${email}`, {
    method: 'PUT',
    headers: {
      'x-admin-key': 'dev-admin-key',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  const updatedUser = await response.json();
  console.log(updatedUser);
}

// Delete user
async function deleteUser(email) {
  const response = await fetch(`http://localhost:8000/admin/users/${email}`, {
    method: 'DELETE',
    headers: {
      'x-admin-key': 'dev-admin-key'
    }
  });
  const result = await response.json();
  console.log(result);
}
```

## Security Best Practices

1. **Change Default Admin Key**
   - Set a strong `ADMIN_API_KEY` in your `.env` file
   - Never commit the `.env` file to version control

2. **Change Default Admin Password**
   - After first login, update the admin password using the update endpoint

3. **Use HTTPS in Production**
   - Always use HTTPS to protect the admin key in transit

4. **Limit Admin Access**
   - Only grant admin privileges to trusted users
   - Regularly audit admin users

5. **Monitor Admin Actions**
   - Keep logs of all admin operations
   - Review admin activity regularly

## Troubleshooting

### Error: "Admin privileges required"
- Ensure you're including the correct `x-admin-key` header
- Verify the admin key matches the one in your `.env` file

### Error: "User already exists"
- The email or username is already registered
- Use the update endpoint to modify existing users

### Error: "User not found"
- Verify the email address is correct
- Use the list endpoint to see all users

### Database Errors
- Run the migration script: `python migrate_db.py`
- Check database connection in `.env` file

## Additional Resources

- **API Documentation:** http://localhost:8000/docs (when server is running)
- **Database Models:** See `models.py`
- **Authentication:** See `auth.py`
