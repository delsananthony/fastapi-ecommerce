from pydantic import BaseModel
from datetime import datetime

class SchemaBase(BaseModel):

    # create_uid: str
    # write_uid: str
    created_at: datetime
    # updated_at: datetime