from pydantic import BaseModel
from typing import List, Optional


class PredictDemandRequest(BaseModel):
    name_product: str
    type_predict: str
    id_market: Optional[str]


class PredictDemandResponse(BaseModel):
    dates: List[str]
    demands: List[int]
