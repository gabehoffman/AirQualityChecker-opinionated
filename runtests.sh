# ABOUTME: Run Django tests with correct settings module for local/dev use
# ABOUTME: Ensures DJANGO_SETTINGS_MODULE is set for pytest
DJANGO_SETTINGS_MODULE=airquality.settings pytest "$@"
