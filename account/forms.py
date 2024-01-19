from django import forms
from account.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'full name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number = phone).exists()

        if user:
            raise ValidationError('this phone already exists')
        return phone
    

class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}))


class RegisterVerifyForm(forms.Form):
    verify_code = forms.CharField()


class LoginVerifyForm(forms.Form):
    code = forms.CharField()


