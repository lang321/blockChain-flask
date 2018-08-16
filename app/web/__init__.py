# coding:utf-8
'''
@author: fight139
@file: __init__.py.py
@time: 2018/7/30 8:43
@desc: 
'''

# 蓝图  name, 所在的模块
from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import blockChain