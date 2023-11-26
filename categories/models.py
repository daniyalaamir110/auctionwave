from django.db import models
from common.models import TimestampedModel
import uuid

def upload_to(instance, filename):
    ext = filename.split(sep=".")[-1]
    filename = uuid.uuid1()
    return "images/categories/{filename}.{ext}".format(filename=filename, ext=ext)

# Create your models here.
class Category(TimestampedModel):
    """
    The `Category` represents the type of `Product`.
    Each `Product` must have a single `Category`.
    For example: Car, Mobile
    """

    # Columns
    title = models.TextField(unique=True, verbose_name="Category Title")
    image = models.ImageField(upload_to=upload_to, null=True)

    def __str__(self):
        return self.title
