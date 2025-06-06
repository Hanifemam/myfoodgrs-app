from typing import Optional
from pydantic import BaseModel


class PreferenceModel(BaseModel):
    user_id: int
    PASTA: Optional[bool] = False
    CARNE: Optional[bool] = False
    PIZZA: Optional[bool] = False
    TORTELLINI: Optional[bool] = False
    SALUMI: Optional[bool] = False
    PESCE: Optional[bool] = False
    LEGUMI: Optional[bool] = False
    FUNGHI: Optional[bool] = False
    CROSTACEI_E_MOLLUSCHI: Optional[bool] = False
    VERDURE: Optional[bool] = False
    GNOCCHI: Optional[bool] = False
    INTERIORA: Optional[bool] = False
    FORMAGGI: Optional[bool] = False
    RISO: Optional[bool] = False
