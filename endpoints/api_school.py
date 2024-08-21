from config.db import Session, get_db
from models.Invoice import ModelInvoice
from models.School import ModelSchool
from schemas.School import SchemaSchool
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post('/schools/', response_model=SchemaSchool)
async def create_school(name: str, address: str = None, phone: str = None, db: Session = Depends(get_db)):
    new_school = ModelSchool(name=name, address=address, phone=phone)
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school


@router.get("/schools/")
def get_schools(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    schools = db.query(ModelSchool).offset(skip).limit(limit).all()
    return schools


@router.get("/schools/{school_id}")
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(ModelSchool).filter(ModelSchool.id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return school


@router.put("/schools/{school_id}")
def update_school(school_id: int, name: str = None, address: str = None, phone: str = None,
                  db: Session = Depends(get_db)):
    data_school = db.query(ModelSchool).filter(ModelSchool.id == school_id).first()

    if data_school is None:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    if name is not None:
        data_school.name = name
    if address is not None:
        data_school.address = address
    if phone is not None:
        data_school.price = phone

    db.commit()
    db.refresh(data_school)

    return data_school


@router.delete("/schools/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(ModelSchool).filter(ModelSchool.id == school_id).first()

    if school is None:
        raise HTTPException(status_code=404, detail="Item not found")

    school.status = False
    db.commit()
    db.refresh(school)
    return {"message": "Escuela dada de baja"}


@router.get("/schools/pending_payments/{school_id}")
def get_school(school_id: int, db: Session = Depends(get_db)):
    query = db.query(ModelInvoice)
    query = query.filter(ModelInvoice.id_school == school_id)
    query = query.filter(ModelInvoice.canceled == False)
    query = query.filter(ModelInvoice.paid == False)
    schools = query.all()

    if not schools:
        raise HTTPException(status_code=404, detail="Sin pendientes de pago")

    total_sum = 0
    contador = 0
    for school in schools:
        total_sum += school.amount
        contador += 1
    total_sum = sum(school.amount for school in schools)
    schools.append({
        "Facturas": contador,
        "Total por cobrar": total_sum
    })
    return schools


@router.get("/schools/without_pending_payments/{school_id}")
def get_school(school_id: int, db: Session = Depends(get_db)):
    query = db.query(ModelInvoice)
    query = query.filter(ModelInvoice.id_school == school_id)
    query = query.filter(ModelInvoice.canceled == False)
    query = query.filter(ModelInvoice.paid == True)
    schools = query.all()

    if not schools:
        raise HTTPException(status_code=404, detail="Sin pendientes de pago")

    total_sum = 0
    contador = 0
    for school in schools:
        total_sum += school.amount
        contador += 1
    total_sum = sum(school.amount for school in schools)
    schools.append({
        "Facturas": contador,
        "Total cobrado": total_sum
    })
    return schools
