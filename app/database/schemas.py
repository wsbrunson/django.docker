from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str

    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    is_active: bool

    class Config:
        orm_mode = True
