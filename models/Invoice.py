from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, Date

Base = declarative_base()


class ModelInvoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    id_school = Column(Integer, nullable=False)
    id_student = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    paid = Column(Boolean, default=False)
    creation_date = Column(Date)
    canceled = Column(Boolean, default=False)
    grade = Column(Integer, nullable=False)
