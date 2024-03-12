from django import forms
from account.models import UserBase


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(label='Enter email', min_length=4, max_length=100, help_text='Required', error_messages=
    {"required": "You need an email"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Re-enter password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')
