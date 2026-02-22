from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    password: str

class UserAuth(User):
    hashed_password: str
    active: bool

class UserDetails(BaseModel):
    id: str
    username: str
    full_name: str
    created_at: datetime
    active: bool | None = None