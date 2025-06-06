from ast import Str
from typing import Optional
from pydantic import BaseModel

class InteractionModel(BaseModel):
    group_id: int
    interaction: str
    
class ConflictModel(BaseModel):
    user_id: int
    group_id: int
    user_to_add_id: int
    
class BookModel(BaseModel):
    user_id: int
    group_id: int
    rest_id: int
    avialble_rest: int
    sort_pop: Optional[bool] = False
    sort_fit: Optional[bool] = False
    sort_sim: Optional[bool] = False
    fit_score: int
    sim_score: int
    c1_fit: Optional[int] = -1
    c2_fit: Optional[int] = -1
    c3_fit: Optional[int] = -1
    c4_fit: Optional[int] = -1
    c5_fit: Optional[int] = -1
    fit_rank: int
    sim_rank: int
    pop_rank: int
    tip: int
    category: int
    dish: int
    price: str
    
class ConflictUsageModel(BaseModel):
    user_id: int
    group_id: int
    vconflict_id: int
    limiting_member: Optional[bool] = False
    CROSTACEI_E_MOLLUSCHI: Optional[bool] = False
    FUNGHI: Optional[bool] = False
    FORMAGGI: Optional[bool] = False
    VERDURE: Optional[bool] = False
    PESCE: Optional[bool] = False
    RISO: Optional[bool] = False
    PASTA: Optional[bool] = False
    INTERIORA: Optional[bool] = False
    LEGUMI: Optional[bool] = False
    TORTELLINI: Optional[bool] = False
    GNOCCHI: Optional[bool] = False
    CARNE: Optional[bool] = False
    PIZZA: Optional[bool] = False
    SALUMI: Optional[bool] = False
    revision_number: int
    avialble_before: int
    avialble_after: int
    user_available_before: Optional[int] = -1
    user_available_after: Optional[int] = -1
    
class ExplainModel(BaseModel):
    user_id: int
    group_id: int
    popularity: Optional[bool] = False
    fitness: Optional[bool] = False
    sim: Optional[bool] = False
    trip: Optional[bool] = False
    category: Optional[bool] = False
    dish: Optional[bool] = False
    
class RemberingModel(BaseModel):
    user_id: int
    group_id: int
    remembring_pop: Optional[bool] = False
    remembring_detialed: Optional[bool] = False
    remebr_user_id: int

class RemeberUsageModel(BaseModel):
    user_id: int
    group_id: int
    rembering_id: int
    CROSTACEI_E_MOLLUSCHI: Optional[bool] = False
    FUNGHI: Optional[bool] = False
    FORMAGGI: Optional[bool] = False
    VERDURE: Optional[bool] = False
    PESCE: Optional[bool] = False
    RISO: Optional[bool] = False
    PASTA: Optional[bool] = False
    INTERIORA: Optional[bool] = False
    LEGUMI: Optional[bool] = False
    TORTELLINI: Optional[bool] = False
    GNOCCHI: Optional[bool] = False
    CARNE: Optional[bool] = False
    PIZZA: Optional[bool] = False
    SALUMI: Optional[bool] = False
    avialble_before: int
    avialble_after: int
    user_available_before: Optional[int] = -1
    user_available_after: Optional[int] = -1

class SortingModel(BaseModel):
    user_id: int
    group_id: int
    sorting_book: Optional[bool] = False
    sorting_fit: Optional[bool] = False
    sorting_sim: Optional[bool] = False