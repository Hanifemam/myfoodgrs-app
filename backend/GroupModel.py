from typing import Optional
from pydantic import BaseModel


class GroupModel(BaseModel):
    distance: Optional[int] = 1000000000
    price_eco: Optional[bool] = True
    price_mid: Optional[bool] = True
    price_expensive: Optional[bool] = True
    service_home_delivery: Optional[bool] = False


class GroupResults(BaseModel):
    groupId: int
    description: str

class Selected(BaseModel):
    group_id: int
    restaurant_id: int

class SelectedOrganizer(BaseModel):
    user_id: int
    organizer: Optional[int] = 0
    member: Optional[int] = 0
    restaurant_id: int

class SUS(BaseModel):
    group_id: int
    q1: int
    q2: int
    q3: int
    q4: int
    q5: int
    q6: int
    q7: int
    q8: int
    q9: int
    q10: int
    f1: Optional[bool] = False
    f2: Optional[bool] = False
    f3: Optional[bool] = False
    f4: Optional[bool] = False
    f5: Optional[bool] = False
    f6: Optional[bool] = False
    f7: Optional[bool] = False
    f8: Optional[bool] = False
    f9: Optional[bool] = False
    f10: Optional[bool] = False
    f11: Optional[bool] = False
    f12: Optional[bool] = False
    f13: Optional[bool] = False
    f14: Optional[bool] = False
    f15: Optional[str] = None
    c1: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None