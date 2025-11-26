from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    name: str
    email: str

class UserUpdateSchema(BaseModel):
    id: int
    username: str | None = None
    name: str | None = None
    email: str | None = None