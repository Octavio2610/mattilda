from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()


class ModelSchool(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50))
    phone = Column(String(15))
    status = Column(Boolean, default=True)
