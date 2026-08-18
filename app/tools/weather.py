import requests

from semantic_kernel.functions import kernel_function


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm"
}


class WeatherTools:
    """
    WeatherTools provides live weather lookup using Open-Meteo.

    Flow:
    1. Convert city name to latitude/longitude using Open-Meteo Geocoding API.
    2. Fetch current weather using Open-Meteo Forecast API.
    """

    @kernel_function(
        name="get_weather",
        description="Get live weather for a city using Open-Meteo"
    )
    def get_weather(
        self,
        city: str
    ) -> dict:

        try:
            geo_response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": city,
                    "count": 1,
                    "language": "en",
                    "format": "json"
                },
                timeout=10
            )

            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if "results" not in geo_data or not geo_data["results"]:
                return {
                    "location": city,
                    "temperature": None,
                    "condition": "Location not found",
                    "source": "Open-Meteo"
                }

            location = geo_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]
            resolved_name = location.get("name", city)

            weather_response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,weather_code",
                    "timezone": "auto"
                },
                timeout=10
            )

            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current = weather_data.get("current", {})

            temperature = current.get("temperature_2m")
            weather_code = current.get("weather_code")

            return {
                "location": resolved_name,
                "temperature": float(temperature) if temperature is not None else None,
                "condition": WEATHER_CODES.get(weather_code, "Unknown"),
                "source": "Open-Meteo"
            }

        except requests.exceptions.Timeout:
            return {
                "location": city,
                "temperature": None,
                "condition": "Weather request timed out",
                "source": "Open-Meteo"
            }

        except requests.exceptions.RequestException as error:
            return {
                "location": city,
                "temperature": None,
                "condition": f"Weather API error: {error}",
                "source": "Open-Meteo"
            }

        except Exception as error:
            return {
                "location": city,
                "temperature": None,
                "condition": f"Unexpected weather error: {error}",
                "source": "Open-Meteo"
            }