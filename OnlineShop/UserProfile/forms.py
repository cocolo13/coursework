from django import forms
from .models import *


class AddFeedInBasketForm(forms.ModelForm):
    class Meta:
        model = Baskets
        fields = '__all__'
