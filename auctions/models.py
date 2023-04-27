from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .globals import CATEGORIES

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watched_listing = models.ManyToManyField('Listing', related_name='watched_listing')

class Listing(models.Model):
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=5000)
    starting_bid = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
    )
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORIES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


