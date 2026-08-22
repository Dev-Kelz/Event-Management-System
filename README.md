# Event Management System

A full-stack Event Management System built with **BeeWare/Toga** for the frontend and **FastAPI** for the backend. The application allows users to create, manage, and participate in events through an intuitive user interface and a robust RESTful API.

## Features

* User Authentication (Sign Up/Login)
* Event Creation and Management
* Event Registration
* Event Details Viewing
* User Profile Management
* Responsive Cross-Platform Interface
* RESTful API Integration
* PostgreSQL Database Support

## Technology Stack

### Frontend

* Python
* BeeWare
* Toga

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication

## Project Structure

```text
Event-Management-System/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── event.py
│   │   │   ├── stage.py
│   │   │   ├── task.py
│   │   │   └── notification.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── event.py
│   │   │   ├── stage.py
│   │   │   ├── task.py
│   │   │   └── notification.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── events.py
│   │   │   ├── tasks.py
│   │   │   └── notifications.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── event_service.py
│   │   │   ├── task_service.py
│   │   │   └── notification_service.py
│   │   └── dependencies/
│   │       └── auth.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    └── beeware_app/
        ├── app.py
        ├── screens/
        │   ├── login.py
        │   ├── register.py
        │   ├── dashboard.py
        │   ├── events.py
        │   ├── event_details.py
        │   ├── tasks.py
        │   ├── notifications.py
        │   └── profile.py
        │
        ├── services/
        │   └── api.py
        │
        └── models/
```

## Prerequisites

Before running the project, ensure you have the following installed:

* Python 3.10+
* PostgreSQL
* Git
* Virtual Environment (Recommended)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Event-Management-System
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

## Running the Application

### Start the Backend Server

```bash
cd backend

uvicorn app.main:app --reload
```

The backend API will run at:

```text
http://127.0.0.1:8000
```

### Start the BeeWare Frontend

```bash
cd frontend

python app.py
```

## Environment Variables

Create a `.env` file inside the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/event_management
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Future Improvements

* Event Notifications
* Payment Integration
* QR Code Event Check-In
* Event Analytics Dashboard
* Dark Mode Support
* Real-Time Chat

## Contributing

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

**Ogbegbe Destiny Kelachi**

Email: [kelz.codes@gmail.com](mailto:kelz.codes@gmail.com)

GitHub: https://github.com/dev-kelz

## Project Repository

https://github.com/dev-kelz/Event-Management-System
