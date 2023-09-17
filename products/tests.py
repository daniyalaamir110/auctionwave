from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Product
from categories.models import Category
from datetime import datetime, timedelta, timezone


class ProductModelTests(TestCase):
    def test_create_product(self):
        category = Category(title="test")
        creator = User(
            username="test", email="test@test.com", first_name="test", last_name="test"
        )
        valid_till = datetime.now(tz=timezone.utc) + timedelta(days=1)
        product = Product(
            title="test",
            description="test",
            base_price=1200,
            valid_till=valid_till,
            category=category,
            creator=creator,
        )
        self.assertIsNotNone(product)

    def test_create_product_with_past_valid_till(self):
        category = Category(title="test")
        category.save()

        creator = User(
            username="test", email="test@test.com", first_name="test", last_name="test"
        )
        creator.save()

        valid_till = datetime.now(tz=timezone.utc) - timedelta(days=10)

        with self.assertRaises(ValidationError):
            product = Product(
                title="test",
                description="test",
                base_price=1200,
                valid_till=valid_till,
                category=category,
                creator=creator,
            )

            product.save()

    def test_create_product_with_invalid_base_price(self):
        category = Category(title="test")
        category.save()

        valid_till = datetime.now(tz=timezone.utc) + timedelta(days=10)

        with self.assertRaises(IntegrityError):
            product = Product(
                title="test",
                description="test",
                base_price=1200,
                valid_till=valid_till,
                category=category,
            )

            product.save()
