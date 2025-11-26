from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str
    name: str
    email: str

class UserUpdateSchema(BaseModel):
    id: int
    username: str | None = None
    name: str | None = None
    email: str | None = None

class UserCreateSchema(BaseModel):
    username: str
    name: str 
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str