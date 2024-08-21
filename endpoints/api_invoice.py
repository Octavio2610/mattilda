from config.db import Session, get_db
from fastapi import APIRouter, Depends, HTTPException
from datetime import date

from models.Invoice import ModelInvoice
from schemas.Invoice import SchemaInvoice

router = APIRouter()


@router.post('/invoices/', response_model=SchemaInvoice)
async def create_invoice(id_school: int, id_student: int, amount: float, grade: int, db: Session = Depends(get_db)):
    new_invoice = ModelInvoice(
        id_school=id_school,
        id_student=id_student,
        amount=amount,
        creation_date=date.today(),
        grade=grade
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@router.get("/invoices/")
def get_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    invoices = db.query(ModelInvoice).offset(skip).limit(limit).all()
    return invoices


@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(ModelInvoice).filter(ModelInvoice.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return invoice


@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: int, paid: bool, db: Session = Depends(get_db)):
    data_invoice = db.query(ModelInvoice).filter(ModelInvoice.id == invoice_id).first()

    if data_invoice is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")

    data_invoice.paid = paid

    db.commit()
    db.refresh(data_invoice)

    return data_invoice


@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(ModelInvoice).filter(ModelInvoice.id == invoice_id).first()

    if invoice is None:
        raise HTTPException(status_code=404, detail="Item not found")

    invoice.canceled = True
    db.commit()
    db.refresh(invoice)
    return {"message": "Estudiante dada de baja"}

