from django import forms
from django.contrib.auth.forms import AuthenticationForm

from account.models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                             "placeholder": 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 "placeholder": 'Password', 'id': 'login-pwd'}))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(label='Enter email', min_length=4, max_length=100, help_text='Required',
                             error_messages={"required": "You need an email"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Re-enter password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_user_name(self):
        user_name = self.cleaned_data["user_name"].lower()
        data = UserBase.objects.filter(user_name=user_name)
        if data.count():
            raise forms.ValidationError("Username already exists.")
        return user_name

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("Password does not match.")
        return data["password2"]

    def clean_email(self):
        data = self.cleaned_data
        if UserBase.objects.filter(email=data["email"]).exists():
            raise forms.ValidationError("Email already in use.")
        return data["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
