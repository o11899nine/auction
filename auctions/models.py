from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = (
        ('Toys', 'Toys'),
        ('Cars', 'Cars'),
        ('Clothing', 'Clothing'),
        ('Furniture', 'Furniture'),
        ('Instruments', 'Instruments'),
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=5000)
    starting_bid = models.FloatField()
    image_url = models.URLField()
    category = models.CharField(max_length=1, choices=CATEGORIES)
