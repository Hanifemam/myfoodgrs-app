from typing import Optional
from pydantic import BaseModel


class RememberingModel(BaseModel):
    id: int
    name: Optional[str] = ""
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
    french: Optional[bool] = False
    chinese: Optional[bool] = False
    jpan: Optional[bool] = False
    italian: Optional[bool] = False
    greek: Optional[bool] = False
    indian: Optional[bool] = False
    spain: Optional[bool] = False
    lebanan: Optional[bool] = False
    moroccan: Optional[bool] = False
    turkish: Optional[bool] = False
    thai: Optional[bool] = False
    gender: Optional[str] = ""
    nationality: Optional[str] = ""
    age: Optional[int] = 0