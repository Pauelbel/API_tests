from pydantic import BaseModel, Field
from typing import List

""" 
Cхемы для проверки ответов сервиса
"""
class USERS_LIST_DATA(BaseModel):
    id:         int = Field(ge=0)
    email:      str
    first_name: str
    last_name:  str
    avatar:      str = Field(min_length=1)

class USERS_LIST_RESPONSE(BaseModel):
    page:        int = Field(ge=0)
    per_page:    int = Field(ge=1)
    total:       int = Field(ge=1)
    total_pages: int = Field(le=2)
    data:       List[USERS_LIST_DATA]
    
