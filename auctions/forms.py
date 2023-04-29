from django.forms import ModelForm, Textarea, NumberInput
from .models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        exclude = ['user', 'highest_bid']
        widgets = {
            'description': Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
            'starting_bid': NumberInput(attrs={'min': 0, 'max': 1000000, 'placeholder': "00.00"})
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
        exclude = ['user', 'listing']
        widgets = {
            'amount': NumberInput(attrs={'min': 0, 'max': 1000000, 'placeholder': "00.00"})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ['user', 'listing']
        widgets = {
            'text': Textarea(attrs={'rows': 1, 'style': 'resize:none;', 'placeholder': "Write a comment..."})
        }
