from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import CreateListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings": Listing.objects.all().order_by("-created_at"),
    })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        # TODO: notfoundpage
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })

def create_listing(request):
    
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            # Create listing in database
            listing = Listing(title=title, category=category, description=description, image_url=image_url, starting_bid=starting_bid)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/create_listing.html", {
                "form": CreateListingForm(initial={"title": title, "category": category, "description": description, "image_url": image_url, "starting_bid": starting_bid})
                })

    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm()
        })

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
