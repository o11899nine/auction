from django.forms import ModelForm, Textarea, NumberInput, URLField
from .models import Listing

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        exclude = ['user']  # exclude user field from form
        widgets = {
            'description': Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
            'starting_bid': NumberInput(attrs={'min': 0, 'max': 1000000, 'placeholder': "00.00"})
        }
