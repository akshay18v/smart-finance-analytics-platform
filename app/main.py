from fastapi import FastAPI,Depends,HTTPException
from app.database import Base,get_db,engine
from schemas.expense_schema import ExpenseCreate,ExpenseResponse
from models.expense import Expense
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)


app=FastAPI()

@app.get("/")
def get_user():
    print("U r ready!!")

    return "U r ready!!!"
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
