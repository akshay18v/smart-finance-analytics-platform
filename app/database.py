from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

db_url="postgresql://postgres:Shree%4018@localhost:5000/expense_db"
engine=create_engine(db_url)
SessionLocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()