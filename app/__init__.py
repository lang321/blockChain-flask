# coding:utf-8
'''
@author: fight139
@file: __init__.py.py
@time: 2018/7/30 8:42
@desc: 
'''

from flask import Flask

from app.models.base import db


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

#创建一个应用服务
def create_app():
    app = Flask(__name__, static_url_path='/static')
    # print(__name__)    应用的根路径：app, 静态文件路径从此开始
    # 导入配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    # 给app 注册蓝图
    register_blueprint(app)



    # Models
    db.init_app(app)
    # 使current_app生效：将应用上下文入栈
    with app.app_context():
        # db.drop_all()
        db.create_all()
    return app