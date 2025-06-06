from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel


class UserInfoModelClass(BaseModel):
    user_id:int	
    gender:Optional[str] = ""
    nationality:Optional[str] = ""	
    age:Optional[int] = 0		
    TORTELLINI:Optional[bool] = False	
    PESCE:Optional[bool] = False	
    CARNE:Optional[bool] = False	
    GNOCCHI:Optional[bool] = False	
    PIZZA:Optional[bool] = False	
    RISO:Optional[bool] = False	
    FORMAGGI:Optional[bool] = False	
    LEGUMI:Optional[bool] = False
    VERDURE:Optional[bool] = False	
    INTERIORA:Optional[bool] = False	
    FUNGHI:Optional[bool] = False	
    CROSTACEI_E_MOLLUSCHI:Optional[bool] = False	
    PASTA:Optional[bool] = False	
    SALUMI:Optional[bool] = False
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
    

class UserSupportModelClass(BaseModel):
    user_id:int	
    info_level:int	
    expansion:int	
    contradiction:int	