#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/8 17:12
# @Author : 詹荣瑞
# @File : main.py
# @desc : 本代码未经授权禁止商用
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, name=user.User_Name)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_name}", response_model=schemas.User)
def read_user(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete('/users/{user_name}', response_model=schemas.User)
def delete_user(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, update_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, update_user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.get("/rent/start", response_model=schemas.Order)
def rent_start(User_ID: str, Fridge_ID: str, db: Session = Depends(get_db)):
    if crud.query_boxes(db, User_ID):
        raise HTTPException(status_code=502, detail="用户有正在进行的订单")
    db_box = crud.get_empty_box(db, Fridge_ID)
    if db_box is None:
        raise HTTPException(status_code=404, detail="未找到指定冰柜空箱子")
    else:
        db_order = crud.create_order(db, User_ID, db_box.Box_ID)
        crud.open_box(db, db_box.Box_ID)
        return db_order


@app.get("/rent/open", response_model=schemas.Box)
def rent_open(User_ID: str, Box_ID: str, db: Session = Depends(get_db)):
    db_order = crud.query_user_box_order(db, User_ID, Box_ID)
    if db_order:
        crud.open_box(db, db_order.box.Box_ID)
        return db_order.box
    else:
        raise HTTPException(status_code=404, detail="未找到指定订单")


@app.get("/rent/stop", response_model=schemas.Order)
def rent_stop(User_ID: str, Box_ID: str, db: Session = Depends(get_db)):
    db_order = crud.query_user_box_order(db, User_ID, Box_ID)
    if db_order:
        crud.close_order(db, db_order.Order_ID)
        return db_order
    else:
        raise HTTPException(status_code=404, detail="未找到指定订单")


@app.get("/query/box", response_model=List[schemas.Box])
def query_box(User_ID: str, db: Session = Depends(get_db)):
    db_boxes = crud.query_boxes(db, User_ID)
    if db_boxes:
        return db_boxes
    else:
        raise HTTPException(status_code=404, detail="未找到正在进行的订单")


@app.get("/query/order", response_model=List[schemas.Order])
def query_orders(User_ID: str, db: Session = Depends(get_db)):
    db_order = crud.query_orders(db, User_ID)
    if db_order is None:
        raise HTTPException(status_code=404, detail="未找到用户订单")
    else:
        return db_order


if __name__ == '__main__':
    import uvicorn

    # uvicorn server_http:app --host 172.17.0.2 --port 7474
    uvicorn.run(app)
