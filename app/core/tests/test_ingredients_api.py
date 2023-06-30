from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Testcase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test the publically available ingredients APT"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertequal(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test ingredients can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@londonappdev.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="kale")
        Ingredient.objects.create(user=self.user, name="salt")
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            "other@londonappdev.com",
            "testpass",
        )
        Ingredient.objects.create(user=user2, name="Vinegar")
        ingredient = Ingredient.objects.create(user=self.user, name="Tumeric")
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload = {"name": "Cabbage"}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload["name"],
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {"name": ""}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


def test_recipe_str(self):
    """Test the recipe string representation"""
    recipe = models.Recipe.objects.created(
        user=sample_user(), title="steak and mushroom sauce", time_minutes=5, price=5.00
    )
    self.assertEqual(str(recipe), recipe.title)
