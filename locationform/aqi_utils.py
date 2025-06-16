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
        # Only supported variables per Open-Meteo docs
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi",
        "timezone": "auto"
    }
    try:
        resp = requests.get(AIR_QUALITY_URL, params=params, timeout=10)
        print(f"[DEBUG] AQI request URL: {resp.url}")
        print(f"[DEBUG] AQI response status: {resp.status_code}")
        print(f"[DEBUG] AQI response body: {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        # Only require 'us_aqi' to be present and non-empty
        if "hourly" not in data or "us_aqi" not in data["hourly"] or not data["hourly"]["us_aqi"]:
            raise ValueError("Air quality data is incomplete. Missing: us_aqi")
        # Fill in optional fields with defaults if missing
        for field in ["main_pollutant", "time"]:
            if field not in data["hourly"] or not data["hourly"][field]:
                # Fill with 'Unknown' or a list of 'Unknown' matching us_aqi length
                n = len(data["hourly"]["us_aqi"])
                data["hourly"][field] = ["Unknown"] * n
        return data
    except Exception as e:
        print(f"[ERROR] AQI exception: {e}")
        return {"error": str(e)}
