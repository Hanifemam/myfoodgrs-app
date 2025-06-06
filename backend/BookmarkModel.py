from typing import Optional
from pydantic import BaseModel


class BookmarkModel(BaseModel):
    restaurant_id: int
    group_id: int
