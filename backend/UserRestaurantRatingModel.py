from xmlrpc.client import boolean
from pydantic import BaseModel


class UserRatingoModelClass(BaseModel):
    user_id:int	
    restaurant_id: int
    rating: int
    group: bool