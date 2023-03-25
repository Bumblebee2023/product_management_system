from pydantic import BaseModel
from typing import List, Optional


class NewUserTg(BaseModel):
    user_tg_id: int
    username: str
