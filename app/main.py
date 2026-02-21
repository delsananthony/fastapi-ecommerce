from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI


from datetime import datetime, timezone
from typing import Annotated, Any, Literal, Optional
from .db.mongo import get_db, oid_str, shutdown_db
from pydantic import BaseModel, BeforeValidator, Field

SALES_COLL = "sales"

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()

    # Practical indexes for common queries (still one collection)
    await db[SALES_COLL].create_index("status")
    await db[SALES_COLL].create_index("updated_at")

    yield

    await shutdown_db()

app = FastAPI(lifespan=lifespan)

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

PyObjectId = Annotated[str, BeforeValidator(str)]

class Customer(BaseModel):
    name: str
    email: str

class CustomerDetails(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    id: str
    name: str
    email: str
    created_at: datetime

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    price: float
    created_at: datetime

class Sale(BaseModel):
    id: str
    customer_id: str
    status: Literal["pending", "completed", "cancelled"]
    amount: float
    updated_at: datetime


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/customers", response_model=CustomerDetails)
async def create_customer(name: str, email: str):
    db = get_db()
    customer_doc: dict[str, Any] = {
        "name": name,
        "email": email,
        "created_at": utcnow(),
    }
    result = await db["customers"].insert_one(customer_doc)
    res = oid_str(result.inserted_id)
    print(res)
    print(result)
    # return {"id": res, **customer_doc}
    return CustomerDetails(id=oid_str(result.inserted_id), **customer_doc)

@app.post("/products")
async def create_product(name: str, price: float):
    db = get_db()
    product_doc: dict[str, Any] = {
        "name": name,
        "price": price,
        "created_at": utcnow(),
    }
    result = await db["products"].insert_one(product_doc)
    return {"id": oid_str(result.inserted_id), **product_doc}

@app.post("/sales")
async def create_sale(customer_id: str, amount: float):
    db = get_db()
    sale_doc: dict[str, Any] = {
        "customer_id": customer_id,
        "status": "pending",
        "amount": amount,
        "updated_at": utcnow(),
    }
    result = await db[SALES_COLL].insert_one(sale_doc)
    return {"id": oid_str(result.inserted_id), **sale_doc}