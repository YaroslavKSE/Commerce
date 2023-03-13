from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings, "watchlist": True})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = int(request.POST["starting_bid"])
        image = request.POST["image"]
        category = Category(name_of_category=request.POST["category"])
        category.save()
        listing = Listing(title=title, description=description, bid=bid, image=image, category=category)
        listing.save()
        if listing is not None:
            return render(request, "auctions/create_listing.html", {"massage": "success"})
        else:
            return render(request, "auctions/create_listing.html", {"massage": "notSuccess"})
    return render(request, "auctions/create_listing.html")


def listing(request, listing):
    obj = Listing.objects.get(pk=listing)
    return render(request, "auctions/listing.html", {"listing": obj})


def watchlist(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {"listings": listings, "watchlist": True})
