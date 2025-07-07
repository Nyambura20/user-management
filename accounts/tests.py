from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class CustomUserModelTests(TestCase):
    def test_create_user_with_valid_data(self):
        user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='pass1234'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_verified)
        self.assertTrue(user.check_password('pass1234'))

    def test_create_user_with_invalid_data(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(username='', email='bad', password='')

class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_registration_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'bademail',
            'password1': '123',
            'password2': '456',
        })
        # Check for form errors in the response instead of a specific message
        self.assertContains(response, 'This field is required', status_code=200)

class VerificationViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='verifyme', email='verify@example.com', password='pass1234',
            verification_token='abc123', is_verified=False
        )
        self.client = Client()

    def test_correct_token_verifies(self):
        response = self.client.get(reverse('verify_account', args=['abc123']))
        self.assertRedirects(response, reverse('login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_incorrect_token(self):
        response = self.client.get(reverse('verify_account', args=['wrongtoken']))
        self.assertEqual(response.status_code, 400)

class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='profileuser', email='profile@example.com', password='pass1234'
        )
        self.other = CustomUser.objects.create_user(
            username='otheruser', email='other@example.com', password='pass1234'
        )
        self.client = Client()

    def test_access_own_profile(self):
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'profileuser')

    def test_access_profile_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='changepass', email='changepass@example.com', password='oldpass123'
        )
        self.client = Client()
        self.client.login(username='changepass', password='oldpass123')

    def test_successful_password_change(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'oldpass123',
            'new_password1': 'Newpass456!',
            'new_password2': 'Newpass456!',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Newpass456!'))

    def test_incorrect_old_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'wrongpass',
            'new_password1': 'Newpass456!',
            'new_password2': 'Newpass456!',
        })
        self.assertContains(response, "old password", status_code=200)

class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='loginuser', email='login@example.com', password='pass1234'
        )
        self.client = Client()

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_logout(self):
        self.client.login(username='loginuser', password='pass1234')
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [200, 302])