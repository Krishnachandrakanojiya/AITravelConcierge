from semantic_kernel.functions import kernel_function


class FxTools:

    @kernel_function(
        name="convert_currency",
        description="Convert currency values"
    )
    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> dict:

        try:

            # Mock rate for now

            rate = 0.92

            converted_amount = amount * rate

            return {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": rate,
                "converted_amount": round(
                    converted_amount,
                    2
                )
            }

        except Exception as e:

            return {
                "error": str(e)
            }