# BeeWare Frontend

This frontend uses BeeWare's Toga toolkit to provide a native-feeling desktop app for the Event Management System.

## Setup

```bash
cd frontend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The app talks to the FastAPI backend at `http://127.0.0.1:8000/api`.

## Features

- View published events
- Log in with existing API credentials
- Refresh event data from the backend
