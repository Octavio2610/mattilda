from fastapi import FastAPI
from endpoints import api_school, api_student, api_invoice

app = FastAPI()
app.include_router(api_school.router, prefix="/api", tags=["Escuelas"])
app.include_router(api_student.router, prefix="/api", tags=["Estudiantes"])
app.include_router(api_invoice.router, prefix="/api", tags=["Facturas"])

