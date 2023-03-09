from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name_of_category = models.CharField(max_length=64)

    def __str__(self):
        return f"Category: {self.name_of_category}"


class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=2000, blank=True)
    bid = models.FloatField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    image = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Title: {self.title} Bid: {self.bid}$ " \
               f"Description: {self.description}"
