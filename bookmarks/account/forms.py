#!/usr/bin/env python3
""" Forms """
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(forms.Form):
    """ Login form """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """ User Registration Form """
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        """ Validates password """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')

        return cd['password2']


class UserEditForm(forms.ModelForm):
    """ Allow users to edit their bio """
    class Meta:
        """ Metadata """
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    """ Allow users to edit their profile """
    class Meta:
        """ Metadata """
        model = Profile
        fields = ['date_of_birth', 'photo']
