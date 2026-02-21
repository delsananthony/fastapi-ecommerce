from app.core.utils import utcnow
from app.db.mongo import MongoDatabase, oid_str, parse_object_id
from app.schema.customer_schema import Customer, CustomerDetails
from fastapi import Depends
from typing import Any

async def get_customers(db: MongoDatabase) -> list[CustomerDetails]:
    customers = await db["customers"].find().to_list(length=None)

    out: list[CustomerDetails] = []
    for doc in customers:
        out.append(
            CustomerDetails(
                id=oid_str(doc["_id"]),
                name=doc["name"],
                email=doc["email"],
                created_at=doc["created_at"]
            )
        )

    return out

async def create_customer(db: MongoDatabase, customer: Customer) -> CustomerDetails:
    customer_doc: dict[str, Any] = {
            "name": customer.name,
            "email": customer.email,
            "created_at": utcnow(),
    }
    result = await db["customers"].insert_one(customer_doc)
    return CustomerDetails(id=oid_str(result.inserted_id), **customer_doc)

async def update_customer(db: MongoDatabase, customer_id: str, name: str | None = None, email: str | None = None):
    update_doc: dict[str, Any] = {}
    if name is not None:
        update_doc["name"] = name
    if email is not None:
        update_doc["email"] = email

    result = await db["customers"].update_one({"_id": parse_object_id(customer_id)}, {"$set": update_doc})
    return result.matched_count > 0

async def archive_customer(db: MongoDatabase, customer_id: str):
    result = await db["customers"].update_one({"_id": parse_object_id(customer_id)}, {"$set": {"archived": True}})
    return result.matched_count > 0