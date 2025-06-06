from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    organizer = 'organizer'
    companion = 'companion'


class Address(BaseModel):
    address = 'address'


class Organizer(BaseModel):
    first_name = "Organizer"
    last_name: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    role = Role.organizer.value
    group_id: int


class Companion(BaseModel):
    first_name = "Companion"
    last_name: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    role = Role.companion.value
    group_id: int
