# Quick Command Reference

## Setup Commands

### Initial Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Database Setup
```bash
# Create PostgreSQL database
createdb event_management

# Create admin user
python create_admin.py
```

## Development Commands

### Run Application
```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Development mode with custom host/port
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Testing
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest test_main.py -v

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test class
pytest test_main.py::TestAuthentication -v

# Run specific test
pytest test_main.py::TestAuthentication::test_register_user -v
```

## Docker Commands

### Build and Run
```bash
# Build Docker image
docker build -t event-management .

# Run Docker container
docker run -p 8000:8000 --env-file .env event-management

# Run with volume mount for uploads
docker run -p 8000:8000 --env-file .env -v $(pwd)/uploads:/app/uploads event-management
```

### Docker Compose
```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# Remove volumes
docker-compose down -v
```

## Database Commands

### PostgreSQL
```bash
# Connect to database
psql -U username -d event_management

# Backup database
pg_dump -U username event_management > backup.sql

# Restore database
psql -U username event_management < backup.sql

# Drop database
dropdb event_management

# Create database
createdb event_management
```

### Alembic (Database Migrations)
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history

# View current revision
alembic current
```

## Dependency Management

### Install/Update Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install package-name

# Update requirements file
pip freeze > requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio httpx

# Upgrade all packages
pip list --outdated
pip install --upgrade package-name
```

## Git Commands

### Basic Workflow
```bash
# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add remote repository
git remote add origin https://github.com/username/repo.git

# Push to remote
git push -u origin main

# Create new branch
git checkout -b feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature
```

## Useful URLs

### Local Development
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

## Environment Variables

### Required
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/event_management
```

### Optional
```bash
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=*
SESSION_MAX_AGE=3600
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
pip show package-name
```

### Check Port Usage
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### Kill Process on Port
```bash
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Check Database Connection
```bash
# Test PostgreSQL connection
psql -U username -d event_management -c "SELECT 1;"
```

### View Application Logs
```bash
# Docker logs
docker logs event_management_app

# Docker Compose logs
docker-compose logs web

# Follow logs
docker-compose logs -f web
```

## Production Deployment

### Pre-deployment Checklist
```bash
# Set production environment variables
export ENVIRONMENT=production
export DEBUG=False
export SECRET_KEY=<strong-secret-key>
export DATABASE_URL=<production-db-url>

# Run tests
pytest

# Build Docker image
docker build -t event-management:latest .

# Tag for registry
docker tag event-management:latest registry.example.com/event-management:latest

# Push to registry
docker push registry.example.com/event-management:latest
```

### Test Authentication
```bash
# Check with authentication
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'
```

## Performance Monitoring

### Check Resource Usage
```bash
# Docker stats
docker stats

# Docker Compose stats
docker-compose stats

# System resources
top
htop
```

## Cleanup Commands

### Remove Unused Resources
```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove test cache
rm -rf .pytest_cache

# Remove Docker resources
docker system prune -a

# Remove Docker volumes
docker volume prune
```
