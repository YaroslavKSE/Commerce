from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2000)
    bid = models.IntegerField()

    def __str__(self):
        return f"Title: {self.title} Bid: {self.bid}$ " \
            f"Description: {self.description}"
