import requests

from semantic_kernel.functions import kernel_function


class FxTools:
    """
    FxTools provides live currency conversion using Frankfurter API.
    """

    @kernel_function(
        name="convert_currency",
        description="Convert currency values using live exchange rates"
    )
    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> dict:

        try:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()

            if from_currency == to_currency:
                return {
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "exchange_rate": 1.0,
                    "converted_amount": round(amount, 2),
                    "source": "Frankfurter"
                }

            response = requests.get(
                "https://api.frankfurter.dev/v1/latest",
                params={
                    "base": from_currency,
                    "symbols": to_currency
                },
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            rates = data.get("rates", {})

            if to_currency not in rates:
                return {
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "exchange_rate": None,
                    "converted_amount": None,
                    "error": f"No rate returned for {to_currency}",
                    "source": "Frankfurter"
                }

            rate = float(rates[to_currency])
            converted_amount = amount * rate

            return {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": rate,
                "converted_amount": round(converted_amount, 2),
                "source": "Frankfurter"
            }

        except requests.exceptions.Timeout:
            return {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": None,
                "converted_amount": None,
                "error": "Currency request timed out",
                "source": "Frankfurter"
            }

        except requests.exceptions.RequestException as error:
            return {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": None,
                "converted_amount": None,
                "error": f"Currency API error: {error}",
                "source": "Frankfurter"
            }

        except Exception as error:
            return {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": None,
                "converted_amount": None,
                "error": f"Unexpected currency error: {error}",
                "source": "Frankfurter"
            }