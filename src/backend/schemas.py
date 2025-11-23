from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None
    farm_location: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ScanBase(BaseModel):
    image_hash: str
    disease_name: str
    confidence: float
    recommendation: Optional[str] = None

class ScanCreate(ScanBase):
    pass

class ScanOut(ScanBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
