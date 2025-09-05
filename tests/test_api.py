import pytest
import requests
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

class TestAPI:
    """API endpoint tests"""
    
    @pytest.fixture(autouse=True)
    def wait_for_api(self):
        """Wait for API to be ready before running tests"""
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{API_URL}/health", timeout=5)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                if i == max_retries - 1:
                    pytest.fail("API is not responding after 30 attempts")
                time.sleep(1)

    @pytest.mark.api
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    @pytest.mark.api
    def test_create_user(self):
        """Test user creation endpoint"""
        user_data = {
            "email": "testuser@example.com",
            "name": "Test User"
        }
        response = requests.post(f"{API_URL}/users", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data

    @pytest.mark.api
    def test_get_users(self):
        """Test user retrieval endpoint"""
        response = requests.get(f"{API_URL}/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.api
    def test_counter_endpoint(self):
        """Test Redis counter endpoint"""
        response = requests.post(f"{API_URL}/counter")
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data
        assert isinstance(data["hits"], int)
        assert data["hits"] > 0

    @pytest.mark.api
    def test_invalid_user_creation(self):
        """Test validation on user creation"""
        invalid_user_data = {
            "email": "invalid-email",
            "name": ""
        }
        response = requests.post(f"{API_URL}/users", json=invalid_user_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    def test_duplicate_email(self):
        """Test duplicate email handling"""
        user_data = {
            "email": "duplicate@example.com",
            "name": "First User"
        }
        # Create first user
        response1 = requests.post(f"{API_URL}/users", json=user_data)
        assert response1.status_code == 201

        # Try to create user with same email
        response2 = requests.post(f"{API_URL}/users", json=user_data)
        assert response2.status_code == 400  # Should fail due to unique constraint
