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

---
Add new journal entries here as new issues or insights arise.
