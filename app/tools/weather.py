from semantic_kernel.functions import kernel_function


class WeatherTools:

    @kernel_function(
        name="get_weather",
        description="Get weather for a city"
    )
    def get_weather(
        self,
        city: str
    ) -> dict:

        try:

            # Mock response for now

            return {
                "location": city,
                "temperature": 22,
                "condition": "Partly Cloudy"
            }

        except Exception as e:

            return {
                "error": str(e)
            }