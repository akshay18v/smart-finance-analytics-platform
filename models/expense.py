from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime
from app.database import Base

class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    description=Column(String)
    category=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    amount=Column(Float,nullable=False)

