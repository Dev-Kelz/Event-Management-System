# FastAPI Admin Panel

A production-ready admin panel built with FastAPI and SQLAdmin, featuring secure authentication, user management, and PostgreSQL database integration.

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red?style=flat-square)

## ✨ Features

- 🔐 **Secure Authentication** - Bcrypt password hashing with session-based auth
- 👥 **User Management** - Full CRUD operations for users with admin panel
- 🗄️ **PostgreSQL Database** - Production-ready database with connection pooling
- 📊 **SQLAdmin Panel** - Beautiful, intuitive admin interface
- 🔒 **Security First** - Environment variable validation, secure sessions, audit logging
- 📝 **Comprehensive Logging** - Track all authentication attempts and errors
- 🏥 **Health Checks** - Built-in endpoint for monitoring and load balancers
- ⚙️ **Production Ready** - CORS, connection pooling, error handling, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- pip and virtualenv

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd FastAPI-Admin
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and set:
   ```env
   SECRET_KEY=your-secure-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```
   
   Generate a secure secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Create PostgreSQL database**
   ```bash
   createdb your_database_name
   ```

6. **Create admin user**
   ```bash
   python create_admin.py
   ```
   
   Follow the interactive prompts to set up your admin account with a strong password.

7. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

8. **Access the admin panel**
   
   Open your browser and navigate to:
   ```
   http://localhost:8000/admin
   ```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Production Deployment Guide](README_PRODUCTION.md)** - Deploy to production safely
- **[Changelog](CHANGELOG.md)** - See all improvements and changes

## 🏗️ Project Structure

```
FastAPI-Admin/
├── main.py              # Main application with admin panel
├── config.py            # Configuration management
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy models
├── auth.py              # Authentication utilities
├── create_admin.py      # Admin user creation script
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Session encryption key (required) | - |
| `DATABASE_URL` | PostgreSQL connection string (required) | - |
| `ENVIRONMENT` | Deployment environment | `development` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |
| `SESSION_MAX_AGE` | Session timeout in seconds | `3600` |
| `DB_POOL_SIZE` | Database connection pool size | `10` |
| `DB_MAX_OVERFLOW` | Max connection pool overflow | `20` |

See `env.example` for complete configuration options.

## 🔒 Security Features

- ✅ Bcrypt password hashing
- ✅ Session-based authentication with secure cookies
- ✅ Environment variable validation
- ✅ Database connection pooling
- ✅ SQL injection protection (via SQLAlchemy)
- ✅ CORS configuration
- ✅ Inactive user checking
- ✅ Comprehensive audit logging
- ✅ Strong password enforcement
- ✅ HTTPS-only cookies in production

## 🛠️ API Endpoints

### Health Check
```bash
GET /health
```

Returns the application and database health status:
```json
{
  "status": "healthy",
  "database": "healthy",
  "environment": "development"
}
```

### Admin Panel
```bash
GET /admin
```

Access the admin interface for user management.

### API Documentation
```bash
GET /docs        # Swagger UI
GET /redoc       # ReDoc
```

Interactive API documentation.

## 👥 User Model

The application includes a User model with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `username` | String(50) | Unique username |
| `email` | String(120) | Unique email address |
| `hashed_password` | String(255) | Bcrypt hashed password |
| `is_active` | Boolean | User active status |
| `is_admin` | Boolean | Admin privileges |

## 🧪 Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Creating Additional Admin Users

```bash
python create_admin.py
```

### Database Backup

```bash
# Backup
pg_dump -U username database_name > backup.sql

# Restore
psql -U username database_name < backup.sql
```

## 🚀 Production Deployment

For production deployment instructions, see [README_PRODUCTION.md](README_PRODUCTION.md).

### Quick Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Configure HTTPS/SSL
- [ ] Restrict `ALLOWED_ORIGINS`
- [ ] Set up database backups
- [ ] Configure proper logging
- [ ] Set up monitoring
- [ ] Use Gunicorn with multiple workers
- [ ] Set up reverse proxy (Nginx)

### Production Run Command

```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## 🐳 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t fastapi-admin .
docker run -p 8000:8000 --env-file .env fastapi-admin
```

## 🔍 Troubleshooting

### "SECRET_KEY environment variable must be set"
Make sure your `.env` file exists and contains a `SECRET_KEY`.

### "DATABASE_URL environment variable must be set"
Add your PostgreSQL connection string to the `.env` file.

### Database Connection Failed
- Verify PostgreSQL is running
- Check credentials in `DATABASE_URL`
- Ensure the database exists

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

For more troubleshooting, see [QUICKSTART.md](QUICKSTART.md).

## 📦 Dependencies

Core dependencies:
- **FastAPI** - Modern web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLAdmin** - Admin panel interface
- **Passlib** - Password hashing
- **Uvicorn** - ASGI server
- **PostgreSQL** - Database
- **python-dotenv** - Environment management

See [requirements.txt](requirements.txt) for complete list with versions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The amazing web framework
- [SQLAdmin](https://github.com/aminalaee/sqladmin) - Beautiful admin interface
- [SQLAlchemy](https://www.sqlalchemy.org/) - Powerful ORM

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Quick Start Guide](QUICKSTART.md)
2. Review the [Production Guide](README_PRODUCTION.md)
3. Look at the [Changelog](CHANGELOG.md)
4. Check application logs for detailed error messages
5. Visit the `/health` endpoint to verify system status

## 🗺️ Roadmap

- [ ] Rate limiting implementation
- [ ] Redis session storage
- [ ] Alembic database migrations
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Two-factor authentication
- [ ] Role-based access control (RBAC)
- [ ] API key authentication
- [ ] Automated testing suite
- [ ] CI/CD pipeline

## 📊 Status

**Version:** 1.0.0  
**Status:** Production Ready ✅  
**Last Updated:** October 28, 2025

---

Made with ❤️ using FastAPI and SQLAdmin

