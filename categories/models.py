from django.db import models
from common.models import TimestampedModel


# Create your models here.
class Category(TimestampedModel):
    """
    The `Category` represents the type of `Product`.
    Each `Product` must have a single `Category`.
    For example: Car, Mobile
    """

    # Columns
    title = models.TextField(unique=True, verbose_name="Category Title")

    def __str__(self):
        return self.title
