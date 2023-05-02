from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from .models import User, Listing, Bid, Comment
from .helpers import place_bid, show_listings, post_comment
from .forms import CreateListingForm, BidForm, CommentForm
from .globals import PLACEHOLDER_IMG, POST_ICON, BID_ICON, CATEGORIES


def index(request):
    """Homepage. Shows all listings by all users."""

    return show_listings(request, "Auctions", "All listings", Listing.objects.all())

def categories(request, category):
    """Shows all listing of a certain category"""

    # If category exists, show listings. Else, throw 404.
    if (any(category in i for i in CATEGORIES)):
        return show_listings(request, "Auctions", f"{category}", Listing.objects.filter(category=category))
    else:
        raise Http404


@login_required
def watchlist(request):
    """Shows user's watched listings"""

    return show_listings(request, "My watchlist", "My watchlist", request.user.watched_listing.all())


@login_required
def user_listings(request):
    """Shows user's listings"""

    return show_listings(request, "My listings", "My listings", Listing.objects.filter(user_id=request.user.id))


def listing(request, id):
    """Listing page. Shows information about the listing.
    User can add listing to watchlist and bid on listing here"""

    # Check if listing url exists.
    try:
        listing = Listing.objects.get(pk=id)
    except Listing.DoesNotExist:
        raise Http404

    if request.method == "GET":

        # Show watchlist buttons if user is logged in and user is not listing highlight
        if request.user.is_authenticated:
            on_watchlist = listing in request.user.watched_listing.all()
        else:
            on_watchlist = False

        top_bids = Bid.objects.filter(
            listing_id=listing.id).order_by('-amount')[:3]
        comments = Comment.objects.filter(
            listing_id=listing.id).order_by('-date')

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "on_watchlist": on_watchlist,
            "placeholder_img": PLACEHOLDER_IMG,
            "bid_form": BidForm(),
            "bids": top_bids,
            "bid_icon": BID_ICON,
            "comment_form": CommentForm(),
            "comments": comments,
            "post_icon": POST_ICON,
        })

    elif request.method == "POST":

        # Add or remove listing from watchlist
        if "add_watchlist" in request.POST and request.user != listing.user:
            request.user.watched_listing.add(listing.id)
        elif "rm_watchlist" in request.POST and request.user != listing.user:
            request.user.watched_listing.remove(listing.id)

        # Place bid
        if "place_bid" in request.POST and request.user != listing.user:
            place_bid(request, listing)

        # Post comment
        if "post_comment" in request.POST:
            post_comment(request, listing)

        # Close auction
        if "close_auction" in request.POST and request.user == listing.user and listing.active:
            listing.active = False
            listing.save()

        # If form is not valid, rerender page with user input intact
        return HttpResponseRedirect(reverse('listing', kwargs={'id': listing.id}))


@login_required
def create_listing(request):
    """Page where user creates a new listing"""

    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():

            # If form is valid, create listing in database
            listing = form.save(commit=False)
            listing.user = request.user
            listing.highest_bid = listing.starting_bid
            listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'id': listing.id}))

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
