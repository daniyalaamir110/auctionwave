from django.db import models
from common.models import TimestampedModel
from categories.models import Category
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ValidationError


def no_past(value):
    now = datetime.now(tz=timezone.utc)
    if value < now:
        raise ValidationError("Purchase_Date cannot be in the future.")


class Product(TimestampedModel):
    """
    `Product` is an item whose ad is created by the `User`.
    A `User` can create multiple `Product`s.
    """

    # Columns
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    base_price = models.PositiveIntegerField()
    valid_till = models.DateTimeField(validators=[no_past])

    # Foreign keys
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.title} ({self.base_price})"

    @property
    def is_available(self) -> bool:
        return self.valid_till >= datetime.now(tz=timezone.utc)

    @property
    def time_left(self) -> str:
        time_left = timedelta(seconds=0)
        if self.is_available:
            time_left = self.valid_till - datetime.now(tz=timezone.utc)

        return str(time_left)

    @property
    def highest_bid(self) -> User | None:
        if self.is_available:
            return None

        if self.bids.count == 0:
            return None

        return self.bids.order_by("-bid_amount")[0]
