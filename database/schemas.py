#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/8 17:11
# @Author : 詹荣瑞
# @File : schemas.py
# @desc : 本代码未经授权禁止商用
from typing import List
from pydantic import BaseModel
from datetime import datetime


class Box(BaseModel):
    Fridge_ID: str
    Box_ID: str
    Box_isOccupied: bool
    Box_State: bool

    class Config:
        orm_mode = True


class Order(BaseModel):
    Order_ID: str
    User_ID: str
    Box_ID: str
    Order_Type: bool
    Order_Start_Time: datetime
    Order_End_Time: datetime = None
    Order_Payment_Time: datetime = None
    Order_Amount: int = None
    Order_isPaid: bool = None

    class Config:
        orm_mode = True


class Case(BaseModel):
    Case_ID: str
    Order_ID: str
    Case_Operating_Type: bool
    User_ID: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    User_Name: str


class UserCreate(UserBase):
    User_Password: str


class UserUpdate(UserBase):
    User_Balance: int


class User(UserBase):
    User_ID: str
    User_Balance: int
    orders: List = []
    cases: List = []

    class Config:
        orm_mode = True
