from django.shortcuts import render
from restaurants.forms import RestaurantForm
from restaurants.models import Restaurant
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"


class RestaurantCreateView(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_list")


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/restaurant_detail.html"


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_list")


class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = "restaurant_confirm_delete.html"
    success_url = reverse_lazy("restaurant_list")
