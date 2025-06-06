from typing import Optional
from pydantic import BaseModel


class SingUp(BaseModel):
    id: int
    name: str
    email: str
    password: str
