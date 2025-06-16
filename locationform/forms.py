"""
ABOUTME: Django form for user to enter city, state, and country.
ABOUTME: Handles validation for required fields and USA default logic.
"""

from django import forms

class LocationForm(forms.Form):
    city = forms.CharField(label='City', max_length=100, required=True)
    state = forms.CharField(label='State/Province/Region', max_length=100, required=True)
    country = forms.CharField(label='Country', max_length=100, required=False, initial='USA')

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        country = cleaned_data.get('country')

        if not city:
            self.add_error('city', 'City is required.')
        if not state:
            self.add_error('state', 'State/Province/Region is required.')
        if not country:
            cleaned_data['country'] = 'USA'
        return cleaned_data
