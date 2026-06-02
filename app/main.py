from fastapi import FastAPI,Depends,HTTPException
from app.database import Base,get_db,engine
from schemas.expense_schema import ExpenseCreate,ExpenseResponse
from schemas.user_schema import UserCreate,UserResponse,UserLogin
from models.user import User
from models.expense import Expense
from sqlalchemy.orm import Session
from core.security import get_password_hash,verify_password
Base.metadata.create_all(bind=engine)


app=FastAPI()

@app.get("/")
def get_user():
    print("U r ready!!")

    return "U r ready!!!"
 #============== USER ROUTES ================
 #CREATE USER (REGISTER)
@app.post("/register",response_model=UserResponse)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email is already registered")
    #Extract user data and pop out plain text password
    user_data=user.model_dump()
    raw_password=user_data.pop("password")
    #scramble the password securely
    hashed_pass=get_password_hash(raw_password)
    #save the user containing the scrambled password string to the HD
    new_user=User(**user_data,hashed_password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# USER LOGIN
@app.post("/login")
def login_user(user_credentials:UserLogin,db:Session=Depends(get_db)):
    #look up the user by their email address
    user=db.query(User).filter(User.email==user_credentials.email).first()
#if email doesn't exist,stop immediately
    if not user:
        raise HTTPException(status_code=400,detail="Invalid Credentials")
#check if typed password matches the scrambled db
    is_password_correct=verify_password(user_credentials.password,user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
    return {"message":"Login sucessful!!","username":user.username}
    
































#CREATE
@app.post("/expenses")
def create_expenses(expense:ExpenseCreate,db:Session=Depends(get_db)):
    new_expense=Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense
#READ
@app.get("/expenses")
def get_all_expenses(db:Session=Depends(get_db)):
    expenses=db.query(Expense).all()
    return expenses
#READ BY ID
@app.get("/expenses/{id}")
def get_expense_by_id(id:int,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()

    if not expense:
        raise HTTPException(status_code=404,detail="expense not found")
    
    return expense
#UPDATE
@app.put("/expenses/{id}")
def update_expense(id:int,updated_expense:ExpenseCreate,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="expense not found")
    update_data=updated_expense.model_dump()
    for key,value in update_data.items():
        setattr(expense,key,value)
    db.commit()
    db.refresh(expense)
    return expense
#DELETE
@app.delete("/expenses/{id}")
def delete_expense(id:int,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message":"Expense deleted sucessfully!!!"}
#PATCH
@app.patch("/expenses/{id}",response_model=ExpenseResponse)
def update_fields_expense(id:int,updated_fields:ExpenseCreate,db:Session=Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    update_data=updated_fields.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(expense,key,value)
    
    db.commit()
    db.refresh(expense)

    return expense
