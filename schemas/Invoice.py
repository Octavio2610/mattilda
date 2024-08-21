from pydantic import BaseModel
from datetime import date


class SchemaInvoice(BaseModel):
    id: int
    id_school: int
    id_student: int
    amount: float
    paid: bool
    creation_date: date
    canceled: bool
    grade: int