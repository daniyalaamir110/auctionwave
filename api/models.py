from django.db import models
from django.contrib.auth.models import User


class TimestampedModel(models.Model):
    """
    This is an abstract model containing `created_at`
    and `updated_at` attributes. This can be extended
    into concrete models so that we don't need to redefine
    these attributes
    """

    class Meta:
        # Declare this as an abstract class
        abstract = True

    # Columns
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(TimestampedModel):
    """
    The `Category` represents the type of `Product`.
    Each `Product` must have a single `Category`.
    For example: Car, Mobile
    """

    # Columns
    title = models.TextField(unique=True)

    def __str__(self):
        return self.title


class Product(TimestampedModel):
    """
    `Product` is an item whose ad is created by the `User`.
    A `User` can create multiple `Product`s.
    """

    # Columns
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    base_price = models.PositiveIntegerField()
    valid_till = models.DateTimeField()

    # Foreign keys
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.title} ({self.base_price})"


class Bid(TimestampedModel):
    """
    A `Bid` is a record representing the a `User`'s claim of interest
    or offer for a `Product`. A `User` can make only one `Bid` for a `Product`
    """

    class Meta:
        unique_together = (("bidder", "product"),)

    # Columns
    bid_amount = models.PositiveIntegerField()

    # Foreign keys
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid of {self.bid_amount} on {self.product} by {self.bidder}"
