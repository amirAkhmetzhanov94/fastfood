from django import forms
from django.db.models.fields import BooleanField 
from .models import Dish, CATEGORY_CHOICES
from django.forms import widgets, ModelForm


class DishForm(forms.ModelForm):
    title = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Write a dish..'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    price = forms.CharField(widget=widgets.NumberInput(attrs={'placeholder': 'Give price..'}))
    activated = BooleanField(default=False)

    class Meta:
        model = Dish 
        fields = '__all__'