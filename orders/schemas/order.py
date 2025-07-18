from pydantic import BaseModel, ConfigDict
from typing import List


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = 1

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    order_id: int
    user_id: int
    items: List[OrderItemOut] = []

    model_config = ConfigDict(from_attributes=True)