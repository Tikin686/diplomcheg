from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя с использованием стилей
    """

    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["password1"].widget.attrs["class"] = "form-control"
            self.fields["password2"].widget.attrs["class"] = "form-control"


class UserManagerForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя с использованием стилей
    """

    class Meta:
        model = User
        fields = ("is_active", "first_name", "last_name", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле 'password'
        if "password" in self.fields:
            del self.fields["password"]
