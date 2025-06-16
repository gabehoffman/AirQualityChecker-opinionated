"""
ABOUTME: View for displaying and processing the location input form.
ABOUTME: Renders form, handles validation, and displays submitted data.
"""

from django.shortcuts import render
from .forms import LocationForm

def location_input(request):
    submitted_data = None
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            submitted_data = form.cleaned_data
            form = LocationForm()  # Reset form after successful submit
    else:
        form = LocationForm()
    return render(request, 'locationform/location_form.html', {
        'form': form,
        'submitted_data': submitted_data,
    })
