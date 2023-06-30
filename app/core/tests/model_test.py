from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful!"""
        email = "test@londonappdev.com"
        password = "Password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@LONDONAPPDEV.com"
        user = get_user_model().objects.create_user(
            email,
            "test123",
        )


def sample_user(
    email="test@londonappdev.com",
    password="testpass",
):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email,
        password,
    )


def test_tag_str(self):
    """Test the tag string created"""
    tag = models.Tag.objects.created(
        user=sample_user(),
        name="Vegan",
    )
    self.assertEqual(str(tag), tag.name)


def test_ingredient_str(self):
    """Test the ingredient string representation"""
    ingredient = models.Ingredient.objects.create(
        user=sample_user(),
        name="Cucumber",
    )
    self.assertequal(str(ingredient), ingredient.name)
