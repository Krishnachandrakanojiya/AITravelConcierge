from pydantic import BaseModel
from typing import List, Optional


class Weather(BaseModel):
    location: str
    temperature: float
    condition: str


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class CardRecommendation(BaseModel):
    card_name: str
    benefit: str
    fx_fee: str
    source: str


class CurrencyInfo(BaseModel):
    from_currency: str
    to_currency: str
    rate: float


class TripPlan(BaseModel):
    destination: str
    start_date: str
    end_date: str

    weather: Optional[Weather]

    attractions: List[str]

    restaurants: List[str]

    card_recommendation: CardRecommendation

    currency_info: CurrencyInfo
    