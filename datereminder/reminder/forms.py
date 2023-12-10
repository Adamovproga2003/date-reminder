import datetime

from django import forms
from django.forms import TextInput, Select

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
    day = forms.ChoiceField(choices=[(str(day), str(day)) for day in range(1, 32)])
    year = forms.ChoiceField(choices=[(f"{year}", f"{year}") for year in range(1950, datetime.datetime.now().year + 1)])

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget = Select(attrs={
                'id': 'day',
                'name': 'day'
            }, choices=((str(day), str(day)) for day in range(1, 32)))
        self.fields['year'].widget = Select(attrs={
                'id': 'year',
                'name': 'year'
            }, choices=((f"{year}", f"{year}") for year in range(1950, datetime.datetime.now().year + 1)))
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

    def clean(self):
        cleaned_data = super(DateForm, self).clean()
        name = cleaned_data.get('name')
        relationship = cleaned_data.get('relationship')
        month = cleaned_data.get('month')
        day = cleaned_data.get('day')
        year = cleaned_data.get('year')
        if not name and not relationship and not month and not day and not year:
            raise forms.ValidationError('You have to write something!')
