from typing import Optional
from pydantic import BaseModel


class ProgressModelClass(BaseModel):
    user_id:int	
    column_name: str
    personal_info: Optional[bool]
    pre_rating: Optional[bool]
    post_rating: Optional[bool]
    group_construction: Optional[bool]
    decision_making: Optional[bool]
    questionnaire: Optional[bool]