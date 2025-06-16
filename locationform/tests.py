"""
ABOUTME: Unit tests for the LocationForm and location input view.
ABOUTME: Validates form logic and view behavior for location input.
"""
from django.test import TestCase
from .forms import LocationForm
from django.urls import reverse

class LocationFormTests(TestCase):
    def test_form_requires_city_and_state(self):
        form = LocationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)
        self.assertIn('state', form.errors)

    def test_form_defaults_country_to_usa(self):
        form = LocationForm(data={'city': 'Boston', 'state': 'MA'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], 'USA')

    def test_form_accepts_all_fields(self):
        form = LocationForm(data={'city': 'Toronto', 'state': 'ON', 'country': 'Canada'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['country'], 'Canada')

class LocationInputViewTests(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse('location_input'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter Location')

    def test_post_valid_data_shows_submitted(self):
        response = self.client.post(reverse('location_input'), {
            'city': 'Chicago', 'state': 'IL', 'country': 'USA'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submitted Data')
        self.assertContains(response, 'Chicago')
        self.assertContains(response, 'IL')
        self.assertContains(response, 'USA')

    def test_post_missing_fields_shows_errors(self):
        response = self.client.post(reverse('location_input'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'City is required.')
        self.assertContains(response, 'State/Province/Region is required.')
