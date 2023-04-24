from django.forms import ModelForm, TextInput, Textarea, FloatField, URLField
from .models import Listing

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
        }
