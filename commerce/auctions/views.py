from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid


def index(request):
    listings = Listing.objects.filter(active=True)
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
        price = request.POST["starting_bid"]
        bid = Bid(bid=price, user=request.user)
        bid.save()
        image = request.POST["image"]
        category = Category.objects.get(name_of_category=request.POST["category"])

        listing = Listing(title=title, description=description, bid=bid,
                          image=image, category=category, owner=request.user)
        listing.save()
        if listing is not None:
            return render(request, "auctions/create_listing.html", {"massage": "success"})
        else:
            return render(request, "auctions/create_listing.html", {"massage": "notSuccess"})
    return render(request, "auctions/create_listing.html")


def listing(request, listing):
    listing = Listing.objects.get(pk=listing)
    user = request.user
    all_comments = Comment.objects.filter(listing=listing)
    is_in_watchlist = user in listing.watchlist.all()
    return render(request, "auctions/listing.html", {"listing": listing,
                                                     "is_in_watchlist": is_in_watchlist,
                                                     "comments": all_comments})


def watchlist(request):
    return render(request, "auctions/watchlist.html", {"listings": Listing.objects.filter(watchlist=request.user)})


def add_to_watchlist(request, id):
    current_listing = Listing.objects.get(pk=id)
    user = request.user
    current_listing.watchlist.add(user)
    return render(request, "auctions/watchlist.html", {"listings": Listing.objects.filter(watchlist=user)})


def remove(request, id):
    current_listing = Listing.objects.get(pk=id)
    user = request.user
    current_listing.watchlist.remove(user)
    return render(request, "auctions/watchlist.html", {"listings": user.user_watchlist.all()})


def add_comment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    user_comment = request.POST['new_comment']
    new_comment = Comment(owner=user, listing=listing, comment=user_comment)
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def add_bid(request, id):
    user = request.user
    current_listing = Listing.objects.get(pk=id)
    current_bid = Listing.objects.get(pk=id).bid.bid
    new_bid = float(request.POST["user_bid_listing"])
    if current_bid < new_bid:
        higher_bid = Bid(bid=new_bid, user=user)
        higher_bid.save()
        current_listing.bid = higher_bid
        current_listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id,)))
