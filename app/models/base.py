# coding:utf-8
'''
@author: fight139
@file: base.py
@time: 2018/7/20 21:45
@desc: 
'''
from contextlib import contextmanager
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer

__all__ = ['db', 'Base']

class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield    # 业务逻辑
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # current_app.log
            if throw:
                raise e

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    # 不生成Base表，仅作为抽象类
    __abstract__ = True

    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, nullable=False, default=1)

    def __init__(self):
        # 时间戳
        self.create_time = int(datetime.now().timestamp())

    # 将字典属性加入类属性
    def set_attrs(self, attr_dict):
        for key, value in attr_dict.items():
            # 如果Base对象存在key属性，将attr_dictd的value赋值给self
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)