# from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from datetime import datetime, timezone
from typing import Annotated, Any, Literal, Optional

from app.core.db import get_db, oid_str, shutdown_db
from app.core.exception import ServiceValidationError
from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customer_router


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


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(customer_router)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

PyObjectId = Annotated[str, BeforeValidator(str)]

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

@app.exception_handler(ServiceValidationError)
async def service_error_handler(request: Request, exc: ServiceValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.get("/healthcheck")
async def root():
    return {"status": "Good"}


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