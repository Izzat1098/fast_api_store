from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    user_id: int
    user_name: str
    email: str
    full_name: str

    model_config = ConfigDict(from_attributes=True)