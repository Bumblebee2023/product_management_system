from pydantic import BaseModel
from typing import List, Optional


class PredictRequest(BaseModel):
    name_product: str
    type_predict: str
    id_market: Optional[str]


class PredictDemandResponse(BaseModel):
    dates: List[str]
    demands: List[int]


class _Demand(BaseModel):
    prices: List[int]
    demands: List[int]


class _Profit(BaseModel):
    prices: List[int]
    profits: List[int]


class PredictPriceResponse(BaseModel):
    demand: _Demand
    profit: _Profit
    best_price: int


class Categories(BaseModel):
    categories: List[str]
