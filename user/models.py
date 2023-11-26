from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


def upload_to(instance, filename):
    ext = filename.split(sep=".")[-1]
    filename = uuid.uuid1()
    return "images/profile_images/{filename}.{ext}".format(filename=filename, ext=ext)


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    profile_image = models.ImageField(upload_to=upload_to, blank=True, null=True)