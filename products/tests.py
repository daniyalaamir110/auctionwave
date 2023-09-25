from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Product
from categories.models import Category
from datetime import datetime, timedelta, timezone
import time


class ProductModelTests(TestCase):
    def setUp(self) -> None:
        Category.objects.create(title="Car")
        Category.objects.create(title="Mobile")
        Category.objects.create(title="PC")

        User.objects.create(
            first_name="Test",
            last_name="User1",
            email="testuser1@test.com",
            username="testuser1",
        ).set_password("test12345")

        User.objects.create(
            first_name="Test",
            last_name="User2",
            email="testuser2@test.com",
            username="testuser2",
        ).set_password("test12345")

    def test_create_product(self):
        car_category = Category.objects.get(title="Car")
        user1 = User.objects.get(username="testuser1")
        valid_till = datetime.now(tz=timezone.utc) + timedelta(days=1)
        product = Product(
            title="test",
            description="test",
            base_price=1200,
            valid_till=valid_till,
            category=car_category,
            creator=user1,
        )
        self.assertIsNotNone(product)

    def test_create_product_with_past_valid_till(self):
        car_category = Category.objects.get(title="Car")
        user1 = User.objects.get(username="testuser1")
        valid_till = datetime.now(tz=timezone.utc) - timedelta(days=1)

        with self.assertRaises(ValidationError):
            product = Product.objects.create(
                title="test",
                description="test",
                base_price=1200,
                valid_till=valid_till,
                category=car_category,
                creator=user1,
            )
            product.save()

    def test_create_product_with_invalid_base_price(self):
        car_category = Category.objects.get(title="Car")
        user1 = User.objects.get(username="testuser1")
        valid_till = datetime.now(tz=timezone.utc) - timedelta(days=1)

        with self.assertRaises(ValidationError):
            product = Product.objects.create(
                title="test",
                description="test",
                base_price=-1200,
                valid_till=valid_till,
                category=car_category,
                creator=user1,
            )
            product.save()

    def test_product_is_available(self):
        car_category = Category.objects.get(title="Car")
        user1 = User.objects.get(username="testuser1")
        SECONDS = 2
        valid_till = datetime.now(tz=timezone.utc) + timedelta(seconds=SECONDS)
        product = Product(
            title="test",
            description="test",
            base_price=1200,
            valid_till=valid_till,
            category=car_category,
            creator=user1,
        )
        self.assertEqual(product.is_available, True)
        time.sleep(SECONDS)
        self.assertEqual(product.is_available, False)
