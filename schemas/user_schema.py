from pydantic import BaseModel,EmailStr
from datetime import datetime
#Base structure shared across user schemas
class UserBase(BaseModel):
    username:str
    email:EmailStr
# when user registers 
class UserCreate(UserBase):
    password:str
# when user logs in 
class Userlogin(BaseModel):
    email:EmailStr
    password:str

#when returning user profiles(outgoing response)
class UserResponse(BaseModel):
    id:int
    Username:str
    email:EmailStr
    created_at:datetime
    
    class Config:
        from_attributes=True
