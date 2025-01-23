from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField, ModelForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")



class UserManagerForm(ModelForm):
    class Meta:
        model = User
        fields = ("is_active",)