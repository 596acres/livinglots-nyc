from django import forms
from django.contrib.auth.forms import AuthenticationForm as _AuthenticationForm


class AuthenticationForm(_AuthenticationForm):

    next = forms.CharField(
        initial='/map/',
        widget=forms.HiddenInput(),
    )
