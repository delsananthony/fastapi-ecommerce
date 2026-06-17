from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    # Field handles min/max constraints natively
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """Enforces 1 uppercase letter, 1 number, and 1 special character."""

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_+\-\[\]\/\\]", value):
            raise ValueError("Password must contain at least one special character.")

        return value


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
