from semantic_kernel.functions import kernel_function


class CardTools:

    @kernel_function(
        name="recommend_card",
        description="Recommend best travel card"
    )
    def recommend_card(
        self,
        destination: str
    ) -> dict:

        return {

            "card_name": "BankGold",

            "benefit":
                "4x dining points worldwide",

            "fx_fee":
                "None",

            "source":
                "Internal Travel Card Policy"
        }