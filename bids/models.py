from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from common.models import TimestampedModel
from products.models import Product


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

    def clean(self) -> None:
        if self.bid_amount < self.product.base_price:
            raise ValidationError(
                "Bid amount must not be less than the product's base price"
            )

        if self.bidder.pk == self.product.creator.pk:
            raise ValidationError("The product creators cannot bid on their products")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
