from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'user_name', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'example:.. +48 123 456 789'}),
        }


class ConfirmMailForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {}
