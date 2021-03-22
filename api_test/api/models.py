from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_id/filename
    return 'user_{0}/{1}'.format(instance, filename)


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    full_name = models.CharField(max_length=100)
    phone = models.PositiveIntegerField(validators=[MinLengthValidator(10)], blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(validators=[MinLengthValidator(6)], max_length=6)



class Content(models.Model):
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to=user_directory_path)
    categories = models.CharField(max_length=100,choices=[("test1", "test1"), ("test2", "test2")], blank=True, null=True)
    is_author = models.BooleanField(default=False)
