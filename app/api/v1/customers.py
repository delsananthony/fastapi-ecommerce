from fastapi import APIRouter, HTTPException, Depends
from app.core.db import MongoDatabase
from app.schema.customer_schema import Customer, CustomerDetails

from app.services.customer_service import create_customer, get_customers, update_customer, archive_customer

router = APIRouter(
    prefix="/customer",
    tags=["customer"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_customers(db: MongoDatabase) -> list[CustomerDetails]:
    customers: list[CustomerDetails] = await get_customers(db)
    return customers

@router.post("/", response_model=CustomerDetails)
async def new_customer(db: MongoDatabase, customer: Customer):
    customer: CustomerDetails = await create_customer(db, customer)
    return customer


@router.patch("/{customer_id}")
async def edit_customer(db: MongoDatabase, customer_id: str, name: str | None = None, email: str | None = None):
    success = await update_customer(db, customer_id, name, email)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer updated successfully"}


@router.patch("/archive/{customer_id}")
async def archived_customer(db: MongoDatabase, customer_id: str):
    success = await archive_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer archived successfully"}