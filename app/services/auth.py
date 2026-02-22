from app.core.utils import utcnow
from app.core.db import MongoDatabase, oid_str, parse_object_id
from app.core.security import get_password_hash
from app.schema.auth import UserDetails, UserInDB
from typing import Any




async def get_users(db: MongoDatabase) -> list[UserDetails]:
    users = await db["users"].find().to_list(length=None)
    out: list[UserDetails] = []
    for doc in users:
        out.append(
            UserDetails(
                id=oid_str(doc["_id"]),
                username=doc["username"],
                full_name=doc["full_name"],
                created_at=doc["created_at"]
            )
        )

    return out

async def create_user(db: MongoDatabase, user: UserInDB) -> UserDetails:
    customer_doc: dict[str, Any] = {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "hashed_password": get_password_hash(user.password),
            "active": True,
            "created_at": utcnow(),
    }
    print(customer_doc)
    result = await db["users"].insert_one(customer_doc)
    return UserDetails(id=oid_str(result.inserted_id), **customer_doc)

async def update_user(db: MongoDatabase, user_id: str, name: str | None = None, email: str | None = None):
    update_doc: dict[str, Any] = {}
    if name is not None:
        update_doc["name"] = name
    if email is not None:
        update_doc["email"] = email

    result = await db["users"].update_one({"_id": parse_object_id(user_id)}, {"$set": update_doc})
    return result.matched_count > 0

async def archive_user(db: MongoDatabase, user_id: str):
    result = await db["users"].update_one({"_id": parse_object_id(user_id)}, {"$set": {"active": False}})
    return result.matched_count > 0