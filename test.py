#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/9 16:46
# @Author : 詹荣瑞
# @File : test.py
# @desc : 本代码未经授权禁止商用
class DatabaseModel(object):

    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: str):
        return db.query(self.model).filter(self.model.User_Name == id).first()

    def gets(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.User_Password
        db_base = self.model(User_ID=user.User_Name, User_Name=user.User_Name, User_Password=fake_hashed_password)
        db.add(db_base)
        db.commit()
        db.refresh(db_base)
        return db

    def update(self, db: Session, id: int, update: schemas.UserUpdate):
        db = db.query(self.model).filter(self.model.id == id).first()
        if db:
            update_dict = update.dict(exclude_unset=True)
            for k, v in update_dict.items():
                setattr(db, k, v)
            db.commit()
            db.flush()
            db.refresh(db)
            return db

    def delete(self, db: Session, name: str):
        db = db.query(self.model).filter(self.model.User_Name == name).first()
        if db:
            db.delete(db)
            db.commit()
            db.flush()
            return db
