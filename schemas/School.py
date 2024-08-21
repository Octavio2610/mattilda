from pydantic import BaseModel


class SchemaSchool(BaseModel):
    id: int
    name: str
    address: str = None
    phone: str = None
    status: bool
