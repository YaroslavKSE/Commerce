from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name_of_category = models.CharField(max_length=64)

    def __str__(self):
        return f"Category: {self.name_of_category}"


class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"Bid: {self.bid}"


class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=2000, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=False, related_name="bid_price")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    image = models.CharField(max_length=300, blank=True)
    active = models.BooleanField(default=True, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name="owner_of_listing")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")

    def __str__(self):
        return f"Title: {self.title} Bid: {self.bid}$ " \
               f"Description: {self.description}"


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"Comment on {self.listing} by {self.owner}"


# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
#     listing = models.ManyToManyField(Listing, blank=True, related_name="listing_watchlist")
#
#     def __str__(self):
#         return f"Personal watchlist for: {self.user}"
