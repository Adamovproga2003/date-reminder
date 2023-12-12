import datetime

from django import forms
from django.contrib.auth import authenticate
from django.forms import TextInput, Select

from .models import User
from .utils import check_leap

monthDay = {
    "January": 31,
    "February": 29,
    "March": 30,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31,
}


class ChangeForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    new_password = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={
            'type': 'text',
            'id': 'username',
            'class': '',
            'name': 'username',
            'placeholder': 'username'})
        self.fields['password'].widget = TextInput(attrs={
            'type': 'password',
            'id': 'password',
            'class': '',
            'name': 'password',
            'placeholder': 'password'})
        self.fields['new_password'].widget = TextInput(attrs={
            'type': 'password',
            'id': 'new_password',
            'class': '',
            'name': 'new_password',
            'placeholder': 'New password'})

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            username = self.cleaned_data.get("username")
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid password")
        return password


class AuthForm(forms.Form):
    password = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={
            'type': 'text',
            'id': 'username',
            'class': '',
            'name': 'username',
            'placeholder': 'username'})
        self.fields['password'].widget = TextInput(attrs={
            'type': 'password',
            'id': 'password',
            'class': '',
            'name': 'password',
            'placeholder': 'password'})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            User.objects.get(username=username)
        except Exception as err:
            return username

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password")
        return username



class DateForm(forms.Form):
    name = forms.CharField(max_length=200)
    relationship = forms.CharField(max_length=200)
    month = forms.ChoiceField(choices=[("January", "January"),
                        ("February", "February"),
                        ("March", "March"),
                        ("April", "April"),
                        ("May", "May"),
                        ("June", "June"),
                        ("July", "July"),
                        ("August", "August"),
                        ("September", "September"),
                        ("October", "October"),
                        ("November", "November"),
                        ("December", "December")])
    year = forms.ChoiceField(choices=[(str(year), str(year)) for year in range(1950, datetime.datetime.now().year + 1)])
    day = forms.ChoiceField(choices=[(str(day), str(day)) for day in range(1, 32)])


    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget = Select(attrs={
                'id': 'day',
                'name': 'day'
            }, choices=((str(day), str(day)) for day in range(1, 32)))
        self.fields['year'].widget = Select(attrs={
                'id': 'year',
                'name': 'year'
            }, choices=((str(year), str(year)) for year in range(1950, datetime.datetime.now().year + 1)))
        self.fields['month'].widget = Select(attrs={
                'id': 'month',
                'name': 'month'
            }, choices=(("January", "January"),
                        ("February", "February"),
                        ("March", "March"),
                        ("April", "April"),
                        ("May", "May"),
                        ("June", "June"),
                        ("July", "July"),
                        ("August", "August"),
                        ("September", "September"),
                        ("October", "October"),
                        ("November", "November"),
                        ("December", "December")
                        ))
        self.fields['name'].widget = TextInput(attrs={
                'id': 'name',
                'class': '',
                'name': 'name',
                'placeholder': 'e.g: Yokesh'})
        self.fields['relationship'].widget = TextInput(attrs={
                'id': 'relationship',
                'class': '',
                'name': 'relationship',
                'placeholder': 'e.g: Brother..'})

    def clean_day(self):
        day = self.cleaned_data.get("day")
        month = self.cleaned_data.get("month")
        year = self.cleaned_data.get("year")

        # Check if all required fields are present
        if not (day and month and year):
            # You can raise a ValidationError or just return the existing value
            return day

        # Now you can safely perform your validation logic
        try:
            year = int(year)
        except ValueError:
            raise forms.ValidationError("Invalid year")

        if month in ["April", "June", "September", "November"] and int(day) > 30:
            raise forms.ValidationError("Day must be less or equal 30")
        elif month == 'February':
            if check_leap(year):
                if int(day) > 29:
                    raise forms.ValidationError("Day must be less or equal 29")
            elif int(day) > 28:
                raise forms.ValidationError("Day must be less or equal 28")

        return day
