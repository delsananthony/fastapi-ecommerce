from typing import Any, Mapping,Annotated
from fastapi import Depends

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient

import os

MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "ecommerce"

type Database = AsyncDatabase[Any, Mapping[str, Any]]
mongo_client = AsyncMongoClient[Mapping[str, Any]](MONGODB_URI)
db: Database | None = None


def get_db() -> Database:
    return mongo_client[DATABASE_NAME]

async def shutdown_db() -> None:
    await mongo_client.close()


def oid_str(oid: ObjectId) -> str:
    return str(oid)


def parse_object_id(ticket_id: str) -> ObjectId:
    return ObjectId(ticket_id)

MongoDatabase = Annotated[Database, Depends(get_db)]