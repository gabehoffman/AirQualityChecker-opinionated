"""
ABOUTME: Utility functions for geocoding and air quality API integration.
ABOUTME: Handles location-to-coordinates and AQI data retrieval for the app.
"""
import requests

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def geocode_location(city: str, state: str, country: str = "USA"):
    params = {
        "q": f"{city}, {state}, {country}",
        "format": "json",
        "limit": 1,
    }
    try:
        resp = requests.get(GEOCODE_URL, params=params, headers={"User-Agent": "AirQualityChecker/1.0"}, timeout=10)
        # Optionally keep debug prints for now
        print(f"[DEBUG] Geocode request URL: {resp.url}")
        print(f"[DEBUG] Geocode response status: {resp.status_code}")
        print(f"[DEBUG] Geocode response body: {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"]),
            "display_name": data[0]["display_name"]
        }
    except Exception as e:
        print(f"[ERROR] Geocode exception: {e}")
        return None

def fetch_air_quality(lat: float, lon: float):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi_pm2_5,us_aqi_pm10,us_aqi_o3,us_aqi_no2,us_aqi_so2,us_aqi_co,main_pollutant",
        "timezone": "auto"
    }
    try:
        resp = requests.get(AIR_QUALITY_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception:
        return None
