from pydantic import BaseModel, ConfigDict

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float


class ItemOut(BaseModel):
    item_id: int
    name: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)