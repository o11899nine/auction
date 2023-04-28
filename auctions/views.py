from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404

from .models import User, Listing
from .forms import CreateListingForm
from .globals import PLACEHOLDER_IMG

def show_listings(request, title, header, listings):
    return render(request, f"auctions/show_listings.html",{
        "title": title,
        "header": header,
        "listings": listings.order_by("-created_at"),
        "placeholder_img": PLACEHOLDER_IMG
    })

def index(request):
    """Homepage. Shows all listings by all users."""

    return show_listings(request, "Auctions", "All listings", Listing.objects.all())

@login_required
def watchlist(request):
    """Shows user's watched listings"""

    return show_listings(request, "My watchlist", "My watchlist", request.user.watched_listing.all())

@login_required
def user_listings(request):
    """Shows user's listings"""

    return show_listings(request, "My listings", "My listings", Listing.objects.filter(user_id=request.user.id))


def listing(request, listing_id):
    """Listing page. Shows information about the listing.
    User can add listing to watchlist and bid on listing here"""

    # Check if listing url exists.
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404
    
    # Show listing info   
    if request.method == "GET":
        if request.user.is_authenticated:
            on_watchlist = listing in request.user.watched_listing.all()
        else:
            on_watchlist = False
    
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "on_watchlist": on_watchlist,
            "placeholder_img": PLACEHOLDER_IMG
        })
    
    # Add or remove listing from watchlist    
    elif request.method == "POST":
        if "add_watchlist" in request.POST:
            request.user.watched_listing.add(listing_id)
        elif "rm_watchlist" in request.POST:
            request.user.watched_listing.remove(listing_id)

        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing.id}))



@login_required
def create_listing(request):
    """Page where user creates a new listing"""

    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():

            # If for mis valid, create listing in database
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing.id}))

        else:
            # If form is not valid, rerender page with user input intact
            return render(request, "auctions/create_listing.html", {
                "form": CreateListingForm(initial=request.POST.dict())
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


@login_required
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
