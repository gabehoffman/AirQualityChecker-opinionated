"""
ABOUTME: View for displaying and processing the location input form.
ABOUTME: Renders form, handles validation, fetches AQI, and displays results/errors.
"""

from django.shortcuts import render
from .forms import LocationForm
from .aqi_utils import geocode_location, fetch_air_quality

def location_input(request):
    submitted_data = None
    aqi_data = None
    error = None
    show_submitted = False
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            submitted_data = form.cleaned_data
            # Geocode location
            geo = geocode_location(
                submitted_data['city'],
                submitted_data['state'],
                submitted_data.get('country', 'USA')
            )
            if not geo:
                error = 'Location not found. Please check your input.'
                submitted_data = None
            else:
                aqi_raw = fetch_air_quality(geo['lat'], geo['lon'])
                if not aqi_raw:
                    error = 'Could not fetch air quality data. Please try again later.'
                    aqi_data = None
                    show_submitted = False
                elif 'error' in aqi_raw:
                    error = aqi_raw['error']
                    aqi_data = None
                    show_submitted = False
                elif 'hourly' not in aqi_raw:
                    error = 'Could not fetch air quality data. Please try again later.'
                    aqi_data = None
                    show_submitted = False
                else:
                    # Find the latest AQI and main pollutant
                    try:
                        idx = -1  # Use latest available
                        aqi = aqi_raw['hourly']['us_aqi'][idx]
                        main_pollutant = aqi_raw['hourly']['main_pollutant'][idx]
                        time = aqi_raw['hourly']['time'][idx]
                        aqi_data = {
                            'aqi': aqi,
                            'main_pollutant': main_pollutant,
                            'time': time,
                            'location': geo['display_name'],
                        }
                        show_submitted = True
                    except Exception:
                        error = 'Air quality data is incomplete.'
                        aqi_data = None
                        show_submitted = False
        # Only reset form if everything succeeded
        if show_submitted:
            form = LocationForm()
        else:
            submitted_data = None
    else:
        form = LocationForm()
    return render(request, 'locationform/location_form.html', {
        'form': form,
        'submitted_data': submitted_data if show_submitted else None,
        'aqi_data': aqi_data,
        'error': error,
    })
