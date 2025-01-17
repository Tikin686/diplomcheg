from django.forms import ModelForm
from restaurants.models import Restaurant


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ("free_seats", )