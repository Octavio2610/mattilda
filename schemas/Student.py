from pydantic import BaseModel


class SchemaStudent(BaseModel):
    id: int
    name: str
    last_name: str
    age: int
    grade: int
    status: bool
    id_school: int
