#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/8 17:12
# @Author : 詹荣瑞
# @File : crud.py
# @desc : 本代码未经授权禁止商用
import datetime
from sqlalchemy.orm import Session
from database import models, schemas


def get_user(db: Session, name: str):
    return db.query(models.User).filter(models.User.User_Name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.User_Password
    db_user = models.User(User_ID=user.User_Name, User_Name=user.User_Name, User_Password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, update_user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_dict = update_user.dict(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(db_user, k, v)
        db.commit()
        db.flush()
        db.refresh(db_user)
        return db_user


def delete_user(db: Session, name: str):
    db_user = db.query(models.User).filter(models.User.User_Name == name).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        db.flush()
        return db_user


def get_empty_box(db: Session, Fridge_ID: str):
    db_box = db.query(models.Box).filter_by(Box_isOccupied=False, Fridge_ID=Fridge_ID).first()
    return db_box


def get_boxes(db: Session, User_ID: str, skip: int = 0, limit: int = 100):
    return db.query(models.Box).offset(skip).limit(limit).filter_by(
        User_ID=User_ID
    ).all()


def open_box(db: Session, Box_ID: str):
    db_box = db.query(models.Box).filter_by(
        Box_ID=Box_ID
    ).first()
    if db_box:
        db_box.Box_State = True
        db_box.Box_isOccupied = True
        db.commit()
        db.flush()
        db.refresh(db_box)
        print("open the box")
    return db.query(models.Box).filter_by(
        Box_ID=Box_ID
    ).all()


def query_orders(db: Session, User_ID: str):
    return db.query(models.User).filter_by(
        User_ID=User_ID
    ).first().orders


def query_current_order(db: Session, User_ID: str, skip: int = 0, limit: int = 100):
    db_order = db.query(models.Order).filter_by(
        User_ID=User_ID, Order_End_Time=None
    ).offset(skip).limit(limit).first()
    return db_order


def query_box(db: Session, User_ID: str, skip: int = 0, limit: int = 100):
    db_order = query_current_order(db, User_ID, skip, limit)
    if db_order.Box_ID and db_order.box.Box_isOccupied:
        return db_order.box


def create_order(db: Session, User_ID: str, Box_ID: str, Order_Type: bool = True):
    db_order = models.Order(
        Order_ID=str(datetime.datetime.now()) + User_ID,
        User_ID=User_ID, Box_ID=Box_ID, Order_Type=Order_Type,
        Order_Start_Time=datetime.datetime.now()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def close_order(db: Session, Order_ID: str):
    db_order = db.query(models.Order).filter_by(
        Order_ID=Order_ID
    ).first()
    if db_order:
        db_order.Order_End_Time = datetime.datetime.now()
        db_order.Order_Amount = 100  # TODO:
        db_order.Order_isPaid = False
        db.commit()
        db.flush()
        db.refresh(db_order)
    return db_order


def pay_order(db: Session, Order_ID: str):
    db_order = db.query(models.Order).filter_by(
        Order_ID=Order_ID
    ).first()
    if db_order:
        db_order.Order_Payment_Time = datetime.datetime.now()
        db_order.Order_isPaid = True
    return db_order


def create_case(db: Session, User_ID: str, Order_ID: str, Case_Operating_Type: bool = True):
    db_case = models.Case(
        Case_ID=str(datetime.datetime.now()) + User_ID,
        User_ID=User_ID, Order_ID=Order_ID, Case_Operating_Type=Case_Operating_Type,
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

