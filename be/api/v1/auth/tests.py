from django.test import TestCase
from master.models import User, RegToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class AuthViewsTests(APITestCase):
    def setUp(self):
        # Create test registration token
        self.reg_token = RegToken.objects.create(
            name="Test Token",
            token_code="TEST2025",
            is_active=True,
            max_usage=10,
            created_by="Test System"
        )
        
        # Membuat user untuk testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            reg_token=self.reg_token
        )
        # Membuat token untuk user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_register_view_with_valid_token(self):
        """Test registration dengan valid token"""
        url = reverse('auth_register')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'token_registrasi': 'TEST2025'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)

    def test_register_view_without_token(self):
        """Test registration tanpa token (should fail)"""
        url = reverse('auth_register')
        data = {
            'username': 'notoken',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'notoken@example.com',
            'first_name': 'No',
            'last_name': 'Token'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_invalid_token(self):
        """Test registration dengan invalid token"""
        url = reverse('auth_register')
        data = {
            'username': 'invalidtoken',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'invalid@example.com',
            'first_name': 'Invalid',
            'last_name': 'Token',
            'token_registrasi': 'INVALID2025'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_registration_token_valid(self):
        """Test token validation endpoint dengan valid token"""
        url = reverse('validate_registration_token')
        data = {'token_code': 'TEST2025'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token_name', response.data)
        self.assertIn('is_valid', response.data)
        self.assertTrue(response.data['is_valid'])

    def test_validate_registration_token_invalid(self):
        """Test token validation endpoint dengan invalid token"""
        url = reverse('validate_registration_token')
        data = {'token_code': 'INVALID2025'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        url = reverse('auth_login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('refresh', response.data['tokens'])
        self.assertIn('access', response.data['tokens'])
        self.assertIn('message', response.data)

    def test_login_view_invalid_credentials(self):
        url = reverse('auth_login')
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_view(self):
        url = reverse('auth_logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'refresh': str(self.refresh)}
        response = self.client.post(url, data, format='json')
        # Updated: Now returns 200 with message instead of 205
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_view_without_refresh_token(self):
        """Test logout tanpa refresh token"""
        url = reverse('auth_logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_view_success(self):
        url = reverse('password_change')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newtestpass123',
            'new_password2': 'newtestpass123'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_password_change_view_wrong_old_password(self):
        url = reverse('password_change')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newtestpass123',
            'new_password2': 'newtestpass123'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_view(self):
        url = reverse('password_reset')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_view_get(self):
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertIn('reg_token_info', response.data)

    def test_profile_view_update(self):
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'email': 'updated@example.com', 'first_name': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Updated: Response now contains 'user' object with updated data
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'updated@example.com')
        self.assertIn('message', response.data)

    def test_registration_info_endpoint(self):
        """Test registration info endpoint"""
        url = reverse('registration_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('requires_token', response.data)
        self.assertTrue(response.data['requires_token'])


class RegTokenModelTests(TestCase):
    """Test RegToken model functionality"""
    
    def setUp(self):
        self.token = RegToken.objects.create(
            name="Test Token",
            token_code="TEST2025",
            is_active=True,
            max_usage=5,
            created_by="Test System"
        )
    
    def test_token_creation(self):
        """Test token creation"""
        self.assertEqual(self.token.name, "Test Token")
        self.assertEqual(self.token.token_code, "TEST2025")
        self.assertTrue(self.token.is_active)
        self.assertEqual(self.token.current_usage, 0)
    
    def test_token_validation_active(self):
        """Test token validation when active"""
        is_valid, message = self.token.is_valid()
        self.assertTrue(is_valid)
        self.assertEqual(message, "Token valid")
    
    def test_token_validation_inactive(self):
        """Test token validation when inactive"""
        self.token.is_active = False
        self.token.save()
        is_valid, message = self.token.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(message, "Token tidak aktif")
    
    def test_token_validation_expired(self):
        """Test token validation when expired"""
        self.token.expires_at = timezone.now() - timedelta(days=1)
        self.token.save()
        is_valid, message = self.token.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(message, "Token sudah kadaluarsa")
    
    def test_token_validation_max_usage_reached(self):
        """Test token validation when max usage reached"""
        self.token.current_usage = 5  # Same as max_usage
        self.token.save()
        is_valid, message = self.token.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(message, "Token sudah mencapai batas maksimal penggunaan")
    
    def test_token_use(self):
        """Test token usage increment"""
        initial_usage = self.token.current_usage
        self.token.use_token()
        self.assertEqual(self.token.current_usage, initial_usage + 1)
    
    def test_remaining_usage(self):
        """Test remaining usage calculation"""
        self.assertEqual(self.token.remaining_usage, 5)
        self.token.use_token()
        self.assertEqual(self.token.remaining_usage, 4)
    
    def test_unlimited_token(self):
        """Test unlimited token (max_usage = 0)"""
        unlimited_token = RegToken.objects.create(
            name="Unlimited Token",
            token_code="UNLIMITED2025",
            max_usage=0
        )
        self.assertEqual(unlimited_token.remaining_usage, "Unlimited")
        
        # Use token multiple times
        for i in range(100):
            unlimited_token.use_token()
        
        is_valid, message = unlimited_token.is_valid()
        self.assertTrue(is_valid)
