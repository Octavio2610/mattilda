from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="database-1.cv8goqaoukfb.us-east-1.rds.amazonaws.com",
    database="postgres",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
