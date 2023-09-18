from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Category


class CategoryModelTests(TestCase):
    def test_create_category_with_unique_title(self):
        category = Category(title="Car")
        self.assertIsNotNone(category)
        self.assertEqual(category.title, "Car")

    def test_create_two_categories_with_different_titles(self):
        category1 = Category(title="Car")
        category2 = Category(title="Mobile")
        self.assertIsNotNone(category1)
        self.assertIsNotNone(category2)

    def test_create_two_categories_with_same_titles(self):
        category1 = Category(title="Car")
        category1.save()

        with self.assertRaises(IntegrityError):
            category2 = Category(title="Car")
            category2.save()
