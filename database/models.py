#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/8 17:07
# @Author : 詹荣瑞
# @File : models.py
# @desc : 本代码未经授权禁止商用
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __table__: Column
    __tablename__ = "users"

    # User_ID = Column(Integer, primary_key=True, index=True)
    User_ID = Column(String(12), primary_key=True, index=True)
    User_Name = Column(String(10), unique=True, index=True)
    User_Password = Column(String(20), )
    User_Balance = Column(Integer, default=0)

    orders = relationship("Order", back_populates="owner")
    cases = relationship("Case", back_populates="owner")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Box(Base):
    __table__: Column
    __tablename__ = "boxes"
    Box_ID = Column(String(12), primary_key=True, index=True)
    Fridge_ID = Column(String(12), )
    Box_isOccupied = Column(Boolean, )
    Box_State = Column(Boolean, )

    order = relationship("Order", back_populates="box")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(Base):
    __table__: Column
    __tablename__ = "orders"

    Order_ID = Column(String(12), primary_key=True, index=True)
    User_ID = Column(String(12), ForeignKey("users.User_ID"))
    Box_ID = Column(String(12), ForeignKey("boxes.Box_ID"))
    Order_Type = Column(Boolean, )
    Order_Start_Time = Column(DateTime, )
    Order_End_Time = Column(DateTime, )
    Order_Payment_Time = Column(DateTime, )
    Order_Amount = Column(Integer, )
    Order_isPaid = Column(Boolean, )

    owner = relationship("User", back_populates="orders")
    box = relationship("Box", back_populates="order")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Case(Base):
    __table__: Column
    __tablename__ = "cases"

    Case_ID = Column(String(12), primary_key=True, index=True)
    Order_ID = Column(String(12))
    Case_Operating_Type = Column(Boolean)
    User_ID = Column(String(12), ForeignKey("users.User_ID"))

    owner = relationship("User", back_populates="cases")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
