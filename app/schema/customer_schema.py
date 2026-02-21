from pydantic import BaseModel
from app.schema.base import SchemaBase

class Customer(BaseModel):
    name: str
    email: str

class CustomerDetails(SchemaBase):
    id: str
    name: str
    email: str