# coding:utf-8
'''
@author: fight139
@file: blockChain.py
@time: 2018/7/30 8:49
@desc: 
'''
from uuid import uuid4

from flask import request
from flask.json import jsonify

from blockChain import blockChain
from app.web import web


@web.route('/index', methods=['GET'])
@web.route('/', methods=['GET'])
def index():
    return 'hello blockchain'


# 添加交易信息
@web.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    # 检查参数是否齐全
    if values is None:
        return jsonify({'status': '400', 'error': 'Missing params'})
    if not all(k in values for k in required):
        return jsonify({'status': '400', 'error': 'Missing params'})
    index = blockChain.new_transaction(values['sender'], values['recipient'], values['amount'])
    return f'Transaction will be added to block {index}'


# 挖矿
@web.route('/mine', methods=['GET'])
def mine():
    last_block = blockChain.last_block
    last_proof = last_block['proof']
    proof = blockChain.proof_of_work(last_proof)

    # 给自己的奖励交易, 接受者为自己，为自己生成一个UUID
    # 发送者为 "0" 表明是新挖出的币
    node_id = str(uuid4()).replace('-', '')
    blockChain.new_transaction(sender='0', recipient=node_id, amount=1)

    # Forge the new Block by adding it to the chain
    block = blockChain.new_block(proof=proof, previous_hash=None)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@web.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockChain.chain,
        'length': len(blockChain.chain)
    }
    return jsonify(response), 200


@web.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockChain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockChain.nodes),
    }
    return jsonify(response), 201


@web.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockChain.resolve_conflicts()
    response = {}
    if replaced:
        response = {
            'message': 'Our chian was replaced',
            'new chain is ': blockChain.chain
        }
    else:
        response = {
            'message': 'Our chian is authorized',
            'new chain is ': blockChain.chain
        }
    return jsonify(response), 200
