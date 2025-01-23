from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from users.forms import UserRegisterForm, UserManagerForm
from users.models import User
from django.urls import reverse_lazy


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


class UserUpdateView(UpdateView):
    model = User
    form_class = UserManagerForm
    success_url = reverse_lazy("users:user_list")