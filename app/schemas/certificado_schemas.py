from pydantic import BaseModel, EmailStr
from typing import List

class EmailSchema(BaseModel): 
    email: List[EmailStr]