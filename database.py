from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Sessionmaker is a factory that will generate new database sessions
# autocommit=False: This means that we need to manually commit our transactions.
# autoflush=False: This means that we need to manually flush our transactions.
# bind=engine: This binds the engine to the sessionmaker.


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

