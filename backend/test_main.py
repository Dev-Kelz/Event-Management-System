# test_main.py
"""
Basic test suite for the Event Management System
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_register_duplicate_user(self):
        """Test registering duplicate user fails"""
        # First registration
        client.post(
            "/register",
            json={
                "username": "duplicate",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        # Second registration with same email
        response = client.post(
            "/register",
            json={
                "username": "duplicate2",
                "email": "duplicate@example.com",
                "password": "password456"
            }
        )
        assert response.status_code == 400
    
    def test_login_success(self):
        """Test successful login"""
        # Register user first
        client.post(
            "/register",
            json={
                "username": "logintest",
                "email": "login@example.com",
                "password": "password123"
            }
        )
        # Login
        response = client.post(
            "/login",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 200
        assert response.json()["success"] is False


class TestEvents:
    """Test event management endpoints"""
    
    def test_get_events(self):
        """Test retrieving all events"""
        response = client.get("/events/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_event(self):
        """Test creating an event"""
        response = client.post(
            "/events/",
            data={
                "title": "Test Event",
                "date": "2024-12-31",
                "time": "18:00",
                "location": "Test Location",
                "description": "Test Description"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Event"
        assert data["location"] == "Test Location"
    
    def test_create_event_with_invalid_image(self):
        """Test creating event with invalid image type"""
        response = client.post(
            "/events/",
            data={
                "title": "Test Event",
                "date": "2024-12-31",
                "time": "18:00",
                "location": "Test Location",
                "description": "Test Description"
            },
            files={"image": ("test.txt", b"not an image", "text/plain")}
        )
        assert response.status_code == 400


class TestAPI:
    """Test general API functionality"""
    
    def test_docs_endpoint(self):
        """Test API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test ReDoc documentation is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
