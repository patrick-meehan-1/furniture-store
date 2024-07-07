from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *

# Create your tests here.

class CustomUserTestCase(TestCase):
    # Create custom user for testing
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@t.com",
            password="tpassword",
            age=23
        )

    def test_create_user(self):
        # Test if a user is created properly
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@t.com")
        self.assertEqual(self.user.age, 23)
        self.assertTrue(self.user.check_password('tpassword'))

    def test_superuser_create_user(self):
        # Test creating a superuser
        self.superuser = get_user_model().objects.create_superuser(
            username="suser",
            email="suser@s.com",
            password='spassword'
        )
        self.assertEqual(self.superuser.username, "suser")
        self.assertEqual(self.superuser.email, "suser@s.com")
        self.assertTrue(self.superuser.check_password, "spassword")
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)