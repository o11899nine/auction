
from django.shortcuts import render

from .forms import BidForm, CommentForm
from .globals import PLACEHOLDER_IMG

def post_comment(request, listing):
    form = CommentForm(request.POST)

    if form.is_valid():
        # record bid
        comment = form.save(commit=False)
        comment.listing = listing
        comment.user = request.user
        comment.save()

def place_bid(request, listing):
    if listing.active:
        form = BidForm(request.POST)

        if form.is_valid():
            # record bid
            bid = form.save(commit=False)
            if bid.amount > listing.highest_bid:
                bid.listing = listing
                bid.user = request.user
                bid.save()

                # update listing highest_bid
                listing.highest_bid = bid.amount
                listing.save()


def show_listings(request, title, header, listings):
    return render(request, f"auctions/show_listings.html", {
        "title": title,
        "header": header,
        "listings": listings.order_by("-date"),
        "placeholder_img": PLACEHOLDER_IMG
    })
