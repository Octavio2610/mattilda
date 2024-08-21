from config.db import Session, get_db
from fastapi import APIRouter, Depends, HTTPException
from models.Student import ModelStudent
from schemas.Student import SchemaStudent

router = APIRouter()


@router.post('/students/', response_model=SchemaStudent)
async def create_student(name: str, last_name: str, age: int, grade: int, id_school: int, db: Session = Depends(get_db)):
    new_student = ModelStudent(
        name=name,
        last_name=last_name,
        age=age,
        grade=grade,
        id_school=id_school)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/students/")
def get_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(ModelStudent).offset(skip).limit(limit).all()
    return students


@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(ModelStudent).filter(ModelStudent.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return student


@router.put("/students/{student_id}")
def update_student(student_id: int, name: str, last_name: str, age: int, grade: int, id_school: int, db: Session = Depends(get_db)):
    data_student = db.query(ModelStudent).filter(ModelStudent.id == student_id).first()

    if data_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")

    data_student.name = name
    data_student.last_name = last_name
    data_student.age = age
    data_student.grade = grade
    data_student.id_school = id_school

    db.commit()
    db.refresh(data_student)

    return data_student


@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(ModelStudent).filter(ModelStudent.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Item not found")

    student.status = False
    db.commit()
    db.refresh(student)
    return {"message": "Estudiante dada de baja"}
