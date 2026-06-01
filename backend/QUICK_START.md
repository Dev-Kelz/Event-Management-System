# Admin Login Quick Start Guide

## Step 1: Start the Server

Make sure your FastAPI server is running:

```bash
cd backend
python -m uvicorn main:app --reload
```

The server should be running at: `http://localhost:8000`

## Step 2: Admin Login

### Using the API

**Endpoint:** `POST /admin/login`

**Request:**
```json
{
  "email": "admin@ems.local",
  "password": "Admin123"
}
```

**Response (Success):**
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

### Using PowerShell (Windows)

```powershell
$body = @{
    email = "admin@ems.local"
    password = "Admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/admin/login" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$response
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/admin/login",
    json={
        "email": "admin@ems.local",
        "password": "Admin123"
    }
)

print(response.json())
```

### Using JavaScript (Frontend)

```javascript
async function login() {
  const response = await fetch('http://localhost:8000/admin/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'admin@ems.local',
      password: 'Admin123'
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Store the admin key for future requests
    localStorage.setItem('adminKey', data.admin_key);
    localStorage.setItem('adminUser', JSON.stringify(data.user));
    console.log('Login successful!', data);
  }
}
```

## Step 3: Use Admin Endpoints

After logging in, use the `admin_key` from the response in the `x-admin-key` header:

### List All Users

**PowerShell:**
```powershell
$headers = @{
    "x-admin-key" = "dev-admin-key"
}

$users = Invoke-RestMethod -Uri "http://localhost:8000/admin/users" `
    -Method Get `
    -Headers $headers

$users
```

**JavaScript:**
```javascript
async function getUsers() {
  const adminKey = localStorage.getItem('adminKey');
  
  const response = await fetch('http://localhost:8000/admin/users', {
    headers: {
      'x-admin-key': adminKey
    }
  });
  
  const users = await response.json();
  console.log(users);
}
```

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid email or password"
}
```
**Solution:** Check your email and password are correct.

### 403 Forbidden
```json
{
  "detail": "Admin privileges required"
}
```
**Solution:** The user exists but is not an admin. Use an admin account.

```json
{
  "detail": "Account is inactive"
}
```
**Solution:** The admin account is disabled. Contact system administrator.

## Testing the Endpoint

Run the test script:

```bash
python test_admin_login.py
```

This will test:
- Valid admin login
- Invalid credentials
- Non-admin user login

## API Documentation

View the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

1. **Change default password** - Update the admin password after first login
2. **Set secure admin key** - Change `ADMIN_API_KEY` in `.env` file
3. **Build admin panel** - Create a frontend interface for user management
4. **Add more admins** - Use the create user endpoint to add more admin users

## Full Documentation

See `ADMIN_GUIDE.md` for complete API documentation and examples.
