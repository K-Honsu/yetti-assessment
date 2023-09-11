import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestUserFlow:

    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    def test_register_user(self):
        register_data = {
            'email': 'money@gmail.com',
            'password': 'emmanuella1234'
        }
        response = self.client.post('/auth/users/', register_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'email' in response.data

    def test_login_user(self):
        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        login_data = {
            'password': 'emmanuella1234',
            'email': 'money@gmail.com'
        }
        response = self.client.post('/users/login/', login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'auth_token' in response.data

    def test_incorrect_email_login(self):
        data = {
            'password': 'emmanuella1234',
            'email': 'money1@gmail.com'
        }
        response = self.client.post('/users/login/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_incorrect_password_login(self):
        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        data = {
            'password': 'emmanuella12345',
            'email': 'money@gmail.com'
        }
        response = self.client.post('/users/login/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_non_existent_user_login(self):
        data = {
            'password': 'john',
            'email': 'jamie@gmail.com'
        }
        response = self.client.post('/users/login/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_access_user_detail_unauthenticated(self):
        response = self.client.get('/auth/users/me', follow=True)
        assert response.data['detail'] == 'Authentication credentials were not provided.'
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_hello_world_unauthenticated(self):
        response = self.client.get('/users/page/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_hello_world_authenticated(self):
        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        login_data = {
            'password': 'emmanuella1234',
            'email': 'money@gmail.com'
        }
        response = self.client.post('/users/login/', login_data)
        assert 'auth_token' in response.data
        token = response.data['auth_token']
        res = self.client.get('/users/page/',HTTP_AUTHORIZATION=f"Token {token}")
        assert res.status_code == status.HTTP_200_OK

    def test_logout_user(self):
        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        login_data = {
                'password': 'emmanuella1234',
                'email': 'money@gmail.com'
            }
        response = self.client.post('/users/login/', login_data)
        assert 'auth_token' in response.data
        token = response.data['auth_token']
        res = self.client.post('/users/logout/',HTTP_AUTHORIZATION=f"Token {token}")
        assert res.status_code == status.HTTP_204_NO_CONTENT
        
    def test_session_fixation_prevention(self):
    # Test to prevent session fixation vulnerability
    
    # Create a new session
        session = self.client.session
        session.save()
        session_key = session.session_key

        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        # Log in with the current session
        login_data = {
            'password': 'emmanuella1234',
            'email': 'money@gmail.com'
        }
        response = self.client.post('/users/login/', login_data)

        # Ensure that the session key has changed after login
        assert response.status_code == status.HTTP_200_OK
        assert self.client.session != session_key

    def test_csrf_token_protection(self):
        # Test to ensure CSRF token protection
        
        response = self.client.get('/users/page/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        User.objects.create_user(email='money@gmail.com', password='emmanuella1234')
        login_data = {
            'password': 'emmanuella1234',
            'email': 'money@gmail.com'
        }
        response = self.client.post('/users/login/', login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'auth_token' in response.data
        token = response.data['auth_token']

        # Attempt to access the protected resource with CSRF token
        headers = {'HTTP_AUTHORIZATION': f"Token {token}", 'HTTP_X-CSRFToken': 'invalid_csrf_token'}
        response = self.client.get('/users/page/', headers)

        # Ensure CSRF token protection is effective
        assert response.status_code == status.HTTP_401_UNAUTHORIZED