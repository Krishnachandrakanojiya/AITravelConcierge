import pytest

from pydantic import ValidationError

from app.models.schemas import (
    Weather,
    SearchResult,
    CardRecommendation,
    CurrencyInfo,
    TripPlan
)


def test_weather_model_valid():
    weather = Weather(
        location="Paris",
        temperature=22.0,
        condition="Partly Cloudy"
    )

    assert weather.location == "Paris"


def test_weather_requires_location():
    with pytest.raises(ValidationError):
        Weather(
            temperature=22.0,
            condition="Cloudy"
        )


def test_search_result_model_valid():
    result = SearchResult(
        title="Example",
        url="https://example.com",
        snippet="Sample snippet"
    )

    assert result.title == "Example"


def test_card_recommendation_model_valid():
    card = CardRecommendation(
        card_name="BankGold",
        benefit="4x dining points",
        fx_fee="None",
        source="Internal Travel Card Policy"
    )

    assert card.card_name == "BankGold"


def test_currency_info_model_valid():
    currency = CurrencyInfo(
        from_currency="USD",
        to_currency="EUR",
        rate=0.92
    )

    assert currency.rate == 0.92


def test_trip_plan_model_valid():
    weather = Weather(
        location="Paris",
        temperature=22.0,
        condition="Partly Cloudy"
    )

    card = CardRecommendation(
        card_name="BankGold",
        benefit="4x dining points",
        fx_fee="None",
        source="Internal Travel Card Policy"
    )

    currency = CurrencyInfo(
        from_currency="USD",
        to_currency="EUR",
        rate=0.92
    )

    trip = TripPlan(
        destination="Paris",
        start_date="2026-09-01",
        end_date="2026-09-08",
        weather=weather,
        attractions=["Eiffel Tower"],
        restaurants=["Frenchie"],
        card_recommendation=card,
        currency_info=currency
    )

    assert trip.destination == "Paris"


def test_trip_plan_requires_destination():
    weather = Weather(
        location="Paris",
        temperature=22.0,
        condition="Partly Cloudy"
    )

    card = CardRecommendation(
        card_name="BankGold",
        benefit="4x dining points",
        fx_fee="None",
        source="Internal Travel Card Policy"
    )

    currency = CurrencyInfo(
        from_currency="USD",
        to_currency="EUR",
        rate=0.92
    )

    with pytest.raises(ValidationError):
        TripPlan(
            start_date="2026-09-01",
            end_date="2026-09-08",
            weather=weather,
            attractions=["Eiffel Tower"],
            restaurants=["Frenchie"],
            card_recommendation=card,
            currency_info=currency
        )


def test_trip_plan_json_dump():
    weather = Weather(
        location="Paris",
        temperature=22.0,
        condition="Partly Cloudy"
    )

    card = CardRecommendation(
        card_name="BankGold",
        benefit="4x dining points",
        fx_fee="None",
        source="Internal Travel Card Policy"
    )

    currency = CurrencyInfo(
        from_currency="USD",
        to_currency="EUR",
        rate=0.92
    )

    trip = TripPlan(
        destination="Paris",
        start_date="2026-09-01",
        end_date="2026-09-08",
        weather=weather,
        attractions=["Eiffel Tower"],
        restaurants=["Frenchie"],
        card_recommendation=card,
        currency_info=currency
    )

    json_output = trip.model_dump_json()

    assert "Paris" in json_output