from django.db import models
from common.models import TimestampedModel
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ValidationError
import uuid


def no_past(value):
    now = datetime.now(tz=timezone.utc)
    if value < now:
        raise ValidationError("valid_till cannot be in the past.")


def upload_to(instance, filename):
    ext = filename.split(sep=".")[-1]
    filename = uuid.uuid1()
    return "images/{filename}.{ext}".format(filename=filename, ext=ext)


class Product(TimestampedModel):
    """
    `Product` is an item whose ad is created by the `User`.
    A `User` can create multiple `Product`s.
    """

    # Columns
    title = models.CharField(max_length=100, verbose_name="Product Title")
    description = models.CharField(max_length=500, verbose_name="Product Description")
    base_price = models.PositiveIntegerField(verbose_name="Base Price")
    valid_till = models.DateTimeField(validators=[no_past], verbose_name="Valid Till")
    is_sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_to)

    # Foreign keys
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Category",
    )
    creator = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Creator",
    )

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

        return time_left

    @property
    def highest_bid(self):
        if self.bids.count() == 0:
            return None

        return self.bids.order_by("-bid_amount")[0]

    @property
    def bid_count(self):
        return self.bids.count()
    
    @property
    def status(self):
        if self.is_sold:
            return "sold"
        elif self.valid_till > datetime.now(tz=timezone.utc):
            return "ongoing"
        else:
            return "finished"

    def clean(self):
        now = datetime.now(tz=timezone.utc)
        if self.valid_till < now:
            raise ValidationError("valid_till cannot be in the past.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
