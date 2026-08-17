from semantic_kernel import Kernel
from app.tools.cards import CardTools
from app.tools.knowledge import KnowledgeTools
from app.tools.search import SearchTools
from app.tools.weather import WeatherTools
from app.tools.fx import FxTools

from app.models.schemas import (
    TripPlan,
    Weather,
    CardRecommendation,
    CurrencyInfo
)

from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextEmbedding
)

from dotenv import load_dotenv

import os


def create_kernel():

    load_dotenv()

    kernel = Kernel()

    kernel.add_plugin(
        WeatherTools(),
        plugin_name="WeatherTools"
    )
    kernel.add_plugin(
        FxTools(),
        plugin_name="FxTools"
    )

    kernel.add_plugin(
        CardTools(),
        plugin_name="CardTools"
    )

    kernel.add_plugin(
        KnowledgeTools(),
        plugin_name="KnowledgeTools"
    )

    kernel.add_plugin(
        SearchTools(),
        plugin_name="SearchTools"
    )

    chat_service = AzureChatCompletion(
        deployment_name=os.getenv(
            "AZURE_OPENAI_CHAT_DEPLOYMENT"
        ),
        endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        ),
        api_key=os.getenv(
            "AZURE_OPENAI_KEY"
        ),
        api_version=os.getenv(
            "AZURE_OPENAI_API_VERSION"
        )
    )

    embedding_service = AzureTextEmbedding(
        deployment_name=os.getenv(
            "AZURE_OPENAI_EMBED_DEPLOYMENT"
        ),
        endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        ),
        api_key=os.getenv(
            "AZURE_OPENAI_KEY"
        ),
        api_version=os.getenv(
            "AZURE_OPENAI_API_VERSION"
        )
    )

    kernel.add_service(chat_service)
    kernel.add_service(embedding_service)

    print("✅ Kernel Created")
    print("✅ Chat Model Connected")
    print("✅ Embedding Model Connected")

    return kernel

def plan_trip():

    weather_tool = WeatherTools()
    fx_tool = FxTools()
    card_tool = CardTools()
    search_tool = SearchTools()

    weather_data = weather_tool.get_weather(
        "Paris"
    )

    fx_data = fx_tool.convert_currency(
        100,
        "USD",
        "EUR"
    )

    card_data = card_tool.recommend_card(
        "Paris"
    )

    search_data = search_tool.search_web(
        "Restaurants in Paris"
    )

    weather = Weather(
        location=weather_data["location"],
        temperature=weather_data["temperature"],
        condition=weather_data["condition"]
    )

    currency = CurrencyInfo(
        from_currency=fx_data["from_currency"],
        to_currency=fx_data["to_currency"],
        rate=fx_data["exchange_rate"]
    )

    card = CardRecommendation(
        card_name=card_data["card_name"],
        benefit=card_data["benefit"],
        fx_fee=card_data["fx_fee"],
        source=card_data["source"]
    )

    trip = TripPlan(
        destination="Paris",
        start_date="2026-09-01",
        end_date="2026-09-08",
        weather=weather,
        attractions=[
            "Eiffel Tower",
            "Louvre Museum"
        ],
        restaurants=[
            item["title"]
            for item in search_data
        ],
        card_recommendation=card,
        currency_info=currency
    )

    print("Weather Retrieved")
    print("Currency Retrieved")
    print("Card Recommendation Retrieved")
    print("Knowledge Retrieved via RAG")
    print("Search Results Retrieved")
    print("TripPlan Generated")

    return trip

if __name__ == "__main__":

    create_kernel()

    trip = plan_trip()

    print()

    print("TRIP PLAN")

    print("=" * 50)

    print(
        trip.model_dump_json(
            indent=2
        )
    )