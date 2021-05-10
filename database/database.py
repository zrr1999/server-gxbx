#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/8 17:06
# @Author : 詹荣瑞
# @File : database.py
# @desc : 本代码未经授权禁止商用
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./refrigerator.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
