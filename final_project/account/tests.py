from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_superuser(self):

        db = get_user_model()
        super_user = db.objects.create_superuser(
            email='testuser@admin.com', user_name='username', password='test')

        self.assertEqual(super_user.email, 'testuser@admin.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'testuser@admin.com')
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@admin.com', user_name='username', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@admin.com', user_name='username', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='username', password='password', is_staff=False)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@normal.com', 'username', 'password')

        self.assertEqual(user.email, 'testuser@normal.com')
        self.assertEqual(user.user_name, 'username')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
