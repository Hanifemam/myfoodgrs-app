from typing import Optional
from pydantic import BaseModel


class ExplanationModel(BaseModel):
    restaurantId: int
    groupId: int

class ExplanationModelAll(BaseModel):
    restaurantId: list = []
    groupId: int

