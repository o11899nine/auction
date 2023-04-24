from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Listing(models.Model):
    CATEGORIES = (
        ('Toys', 'Toys'),
        ('Cars', 'Cars'),
        ('Clothing', 'Clothing'),
        ('Furniture', 'Furniture'),
        ('Instruments', 'Instruments'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=5000)
    starting_bid = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
    )
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
