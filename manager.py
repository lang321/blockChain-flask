# coding:utf-8
'''
@author: fight139
@file: manager.py
@time: 2018/7/30 8:42
@desc: 
'''
from argparse import ArgumentParser

from app import create_app


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=port, threaded=True)
