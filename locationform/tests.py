"""
ABOUTME: Unit tests for the LocationForm and location input view.
ABOUTME: Validates form logic and view behavior for location input.
"""
from django.test import TestCase
from .forms import LocationForm
from django.urls import reverse
from unittest.mock import patch

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

    @patch('locationform.views.geocode_location')
    @patch('locationform.views.fetch_air_quality')
    def test_post_valid_data_shows_submitted(self, mock_fetch, mock_geocode):
        mock_geocode.return_value = {'lat': 41.88, 'lon': -87.63, 'display_name': 'Chicago, IL, USA'}
        mock_fetch.return_value = {
            'hourly': {
                'us_aqi': [50],
                'main_pollutant': ['pm10'],
                'time': ['2025-06-16T12:00:00Z']
            }
        }
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

"""
ABOUTME: Unit and integration tests for AQI/geocoding utilities and view.
ABOUTME: Validates error handling, API integration, and AQI display logic.
"""
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .aqi_utils import geocode_location, fetch_air_quality

class AQIUtilsTests(TestCase):
    @patch('locationform.aqi_utils.requests.get')
    def test_geocode_location_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            'lat': '42.36', 'lon': '-71.06', 'display_name': 'Boston, MA, USA'
        }]
        result = geocode_location('Boston', 'MA', 'USA')
        self.assertIsNotNone(result)
        self.assertEqual(result['lat'], 42.36)
        self.assertEqual(result['lon'], -71.06)
        self.assertIn('Boston', result['display_name'])

    @patch('locationform.aqi_utils.requests.get')
    def test_geocode_location_not_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        result = geocode_location('Nowhere', 'ZZ', 'USA')
        self.assertIsNone(result)

    @patch('locationform.aqi_utils.requests.get')
    def test_fetch_air_quality_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'hourly': {
                'us_aqi': [42],
                'main_pollutant': ['pm2_5'],
                'time': ['2025-06-16T12:00:00Z']
            }
        }
        result = fetch_air_quality(42.36, -71.06)
        self.assertIn('hourly', result)
        self.assertEqual(result['hourly']['us_aqi'][0], 42)

    @patch('locationform.aqi_utils.requests.get')
    def test_fetch_air_quality_api_error(self, mock_get):
        mock_get.side_effect = Exception('API error')
        result = fetch_air_quality(0, 0)
        self.assertIsNone(result)

class LocationInputViewAQITests(TestCase):
    @patch('locationform.views.geocode_location')
    @patch('locationform.views.fetch_air_quality')
    def test_aqi_display_success(self, mock_fetch, mock_geocode):
        mock_geocode.return_value = {'lat': 42.36, 'lon': -71.06, 'display_name': 'Boston, MA, USA'}
        mock_fetch.return_value = {
            'hourly': {
                'us_aqi': [42],
                'main_pollutant': ['pm2_5'],
                'time': ['2025-06-16T12:00:00Z']
            }
        }
        response = self.client.post(reverse('location_input'), {
            'city': 'Boston', 'state': 'MA', 'country': 'USA'
        })
        self.assertContains(response, 'Air Quality Index (AQI)')
        self.assertContains(response, '42')
        self.assertContains(response, 'pm2_5')
        self.assertContains(response, 'Boston, MA, USA')

    @patch('locationform.views.geocode_location')
    @patch('locationform.views.fetch_air_quality')
    def test_aqi_api_error(self, mock_fetch, mock_geocode):
        mock_geocode.return_value = {'lat': 42.36, 'lon': -71.06, 'display_name': 'Boston, MA, USA'}
        mock_fetch.return_value = None
        response = self.client.post(reverse('location_input'), {
            'city': 'Boston', 'state': 'MA', 'country': 'USA'
        })
        self.assertContains(response, 'Could not fetch air quality data')

    @patch('locationform.views.geocode_location')
    def test_aqi_location_not_found(self, mock_geocode):
        mock_geocode.return_value = None
        response = self.client.post(reverse('location_input'), {
            'city': 'Nowhere', 'state': 'ZZ', 'country': 'USA'
        })
        self.assertContains(response, 'Location not found')

class GeocodeKnownCitiesTests(TestCase):
    def test_geocode_known_cities(self):
        # These are well-known cities that should always be found by Nominatim
        cities = [
            ("New York", "NY", "USA"),
            ("Los Angeles", "CA", "USA"),
            ("Chicago", "IL", "USA"),
            ("London", "ENG", "UK"),
            ("Paris", "IDF", "France"),
        ]
        for city, state, country in cities:
            result = geocode_location(city, state, country)
            self.assertIsNotNone(result, f"Geocoding failed for {city}, {state}, {country}")
            self.assertIn(city.split()[0], result["display_name"], f"City name not in display_name for {city}")
