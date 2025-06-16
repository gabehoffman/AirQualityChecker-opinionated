# AirQualityChecker-opinionated

ABOUTME: Minimal Django web app for entering city, state/province/region, and country.
ABOUTME: Demonstrates pragmatic, test-driven, and maintainable engineering practices.

## Overview
This project is a minimal Django web application that allows users to enter:
- A city, state/province/region, and country
- Or just a city and state (defaults country to USA)

The app features:
- Simple form with client-side and server-side validation
- Submitted data display after successful submission
- Test-driven development with comprehensive unit and integration tests

## Setup
1. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install django
   ```
3. Run migrations:
   ```sh
   python manage.py migrate
   ```
4. Start the development server:
   ```sh
   python manage.py runserver
   ```
5. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Testing
Run all tests with:
```sh
python manage.py test
```

### Pytest Support
This project supports running tests with [pytest](https://docs.pytest.org/) and [pytest-django](https://pytest-django.readthedocs.io/):
```sh
pytest locationform/tests.py --ds=airquality.settings --maxfail=1 --disable-warnings -v
```
- Pytest provides improved reporting and developer experience.
- All tests are compatible with both Django and Pytest runners.

## Air Quality Data API Field Handling

- The Open-Meteo API sometimes omits optional fields like `main_pollutant` and `time` in its air quality response, even for valid locations.
- The application now treats these fields as optional: if missing, the UI displays a sensible default ("Unknown") rather than failing or hiding available AQI data.
- Only the `us_aqi` field is required for a successful result. If it is missing, the app reports an error.
- This approach ensures users always see the best available air quality data, with clear indication when some details are unavailable.
- All error handling and test coverage have been updated to reflect this pragmatic, user-friendly behavior.

## Project Journal
See [`JOURNAL.md`](./JOURNAL.md) for technical insights, test setup issues, and lessons learned during development.

## Project Structure
- `airquality/` – Django project settings and configuration
- `locationform/` – App for the location input form and related logic
- `templates/locationform/location_form.html` – Main form template

## Principles
This project follows:
- Pragmatic simplicity and maintainability
- Test-driven development (TDD)
- Clear code documentation (ABOUTME headers)
- Consistent, domain-focused organization

See `.github/instructions/` for detailed engineering and core principles.
