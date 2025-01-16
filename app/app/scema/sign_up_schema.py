from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, constr
from enum import Enum



class UserRole(str, Enum):
    SuperADMIN = "Superadmin"
    ADMIN = "admin"
    CUSTOMER = "customer"




class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str = Field(min_length=8, max_length=128)
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    role: UserRole = Field(default=UserRole.CUSTOMER)
    signup_date: datetime = Field(default=datetime.utcnow)
    is_active: bool = Field(default=True)




