from semantic_kernel.functions import kernel_function


class SearchTools:

    @kernel_function(
        name="search_web",
        description="Search travel information"
    )
    def search_web(
        self,
        query: str
    ) -> list:

        return [

            {
                "title": "Le Comptoir du Relais",
                "url": "https://example.com",
                "snippet":
                    "Classic French Bistro"
            },

            {
                "title": "Frenchie",
                "url": "https://example.com",
                "snippet":
                    "Modern French Cuisine"
            }
        ]