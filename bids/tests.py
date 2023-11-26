from categories.models import Category
from products.models import Product
from user.models import User
from django.test import TestCase
from .models import Bid
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError
import time


class BidModelTests(TestCase):
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

        User.objects.create(
            first_name="Test",
            last_name="User3",
            email="testuser3@test.com",
            username="testuser3",
        ).set_password("test12345")

    def test_create_bid_for_available_product(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        car_category = Category.objects.get(title="Car")
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(weeks=1),
        )
        bid = Bid.objects.create(product=car, bidder=user2, bid_amount=1300000)
        self.assertIsNotNone(bid)

    def test_create_bid_for_own_product(self):
        user1 = User.objects.get(username="testuser1")
        car_category = Category.objects.get(title="Car")
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(weeks=1),
        )
        with self.assertRaises(ValidationError):
            Bid.objects.create(product=car, bidder=user1, bid_amount=1300000)

    def test_create_bid_with_invalid_bid_amount(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        car_category = Category.objects.get(title="Car")
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(weeks=1),
        )
        with self.assertRaises(ValidationError):
            Bid.objects.create(product=car, bidder=user2, bid_amount=1100000)

    def test_create_bid_for_invalid_product(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        car_category = Category.objects.get(title="Car")
        SECONDS = 2
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(seconds=SECONDS),
        )
        time.sleep(SECONDS)
        with self.assertRaises(ValidationError):
            Bid.objects.create(product=car, bidder=user2, bid_amount=1300000)

    def test_create_two_bids_for_same_product(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        car_category = Category.objects.get(title="Car")
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(weeks=1),
        )
        Bid.objects.create(product=car, bidder=user2, bid_amount=1300000)
        with self.assertRaises(ValidationError):
            Bid.objects.create(product=car, bidder=user2, bid_amount=1400000)

    def test_highest_bid_for_product(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        user3 = User.objects.get(username="testuser3")
        car_category = Category.objects.get(title="Car")
        car = Product.objects.create(
            title="title",
            description="description",
            base_price=1200000,
            creator=user1,
            category=car_category,
            valid_till=datetime.now(tz=timezone.utc) + timedelta(weeks=1),
        )

        self.assertIsNone(car.highest_bid)

        bid2 = Bid.objects.create(product=car, bidder=user2, bid_amount=1300000)
        bid3 = Bid.objects.create(product=car, bidder=user3, bid_amount=1400000)

        self.assertIs(car.highest_bid.pk, bid3.pk)
