ABOUTME: Project journal for technical insights, issues, and lessons learned.
ABOUTME: Documents test setup challenges and solutions for future reference.

# Project Journal: Test Setup and Lessons Learned

## Pytest and Django Test Discovery
- Initial Django tests ran cleanly with `manage.py test`.
- Added `pytest` and `pytest-django` for improved reporting and developer experience.
- Created a `conftest.py` with an incorrect `pytest_plugins` line, which caused an ImportError:
  - `ImportError: No module named 'django.contrib.auth.plugins'`
- Solution: Removed the unnecessary `pytest_plugins` line from `conftest.py`.
- Lesson: For standard Django+pytest usage, a minimal or empty `conftest.py` is best unless custom plugins/fixtures are needed.

## Test Discovery with Pytest
- Pytest did not discover tests when run from the project root without specifying the test module.
- Solution: Run `pytest locationform/tests.py` or ensure test files are named with the `test_*.py` pattern for auto-discovery.
- Lesson: Pytest requires test files to match its naming conventions for automatic discovery.

## General Testing Lessons
- Always verify both Django and Pytest test runs after changes to test config or dependencies.
- Use `unittest.mock.patch` for API mocking in Django tests.
- Keep test output pristine and deterministic for CI and local runs.

## Geocoding Regression and Test Coverage (June 2025)
- Issue: Geocoding for well-known cities (e.g., Atlanta, GA, USA) failed due to incorrect use of both structured and free-text parameters in Nominatim API requests.
- Root Cause: Nominatim returns a 400 error if both structured parameters (city, state, country) and the 'q' parameter are used together.
- Solution: Refactored geocode_location to use only the 'q' parameter for all requests.
- Regression Safety: Added a test (GeocodeKnownCitiesTests) to ensure geocoding works for five well-known cities (New York, Los Angeles, Chicago, London, Paris). This prevents silent failures for common locations and ensures future regressions are caught early.
- Lesson: Always verify API parameter requirements and add regression tests for critical user-facing functionality.

## Open-Meteo Air Quality API Variable Bug (June 2025)
- Issue: AQI fetch failed with a 400 error due to unsupported or derived variables in the 'hourly' parameter.
- Root Cause: The Open-Meteo API only supports a specific set of variable names for the 'hourly' parameter (e.g., pm10, pm2_5, carbon_monoxide, nitrogen_dioxide, sulphur_dioxide, ozone, us_aqi). Including unsupported or derived variables (like main_pollutant, us_aqi_pm2_5, etc.) causes a hard failure.
- Solution: Patched fetch_air_quality to use only supported variables in the 'hourly' parameter, per the official API documentation.
- Lesson: Always consult and follow the latest API documentation for allowed parameter values, and add comments referencing the source.

## Open-Meteo API Optional Field Handling (June 2025)

- Problem: The Open-Meteo air quality API sometimes omits optional fields like `main_pollutant` and `time` in its response, even for valid locations.
- Initial implementation treated these as required, causing the app to show errors and hide otherwise valid AQI data.
- Solution: Now, only `us_aqi` is required. If `main_pollutant` or `time` is missing, the app fills in a sensible default ("Unknown") so users always see available AQI data.
- Rationale: This approach is pragmatic, improves UX, and aligns with our core principles—optional fields should not break the app or hide useful information.
- All tests and error handling updated to reflect this behavior. If `us_aqi` is missing, an error is still shown.

---
Add new journal entries here as new issues or insights arise.
