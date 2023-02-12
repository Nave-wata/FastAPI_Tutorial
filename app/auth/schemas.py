from pydantic import BaseModel

class BaseUser(BaseModel):
    name: str

class CreateUser(BaseUser):
    password: str

    class Config:
        orm_mode = True

class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
    