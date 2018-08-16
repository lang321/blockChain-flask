# coding:utf-8
import hashlib
import json
import time
import datetime

# {
#     "index":0,   #节点索引
#     "timestamp":"",  # 时间戳
#     "transactions":[
#         {
#             "sender":"",  # 发送者
#             "recipient":"",  # 接受者
#             "amouont":100
#         }
#     ],  # 交易
#     "proof":"",   # 工作量证明 int
#     "previous_hash":"",  # 上一个区块的hash值
# }
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

import requests


class BlockChain(object):
    def __init__(self):
        # 存储区块链
        self.chain = []
        # 存储交易
        self.current_transactions = []
        # 节点
        self.nodes = set()


        # 创世纪区块,工作量证明任意
        self.new_block(proof=100, previous_hash=1)

    def register_node(self, address: str):
        '''
        address : 172.0.0.1:5000
        :param address:
        :return:
        '''
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        """
        共识算法解决冲突
        使用网络中最长的链.
        :return:  如果链被取代返回 True, 否则为False
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None) -> Dict[str, Any]:
        '''
        创建新块
        :param proof: 工作量证明
        :param previous_hash: 上一个hash值
        :return:
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        # 清空交易信息，交易信息已经打包成新的区块，因此需要清空交易信息
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        '''
        添加新的交易
        :param sender: 交易发送者
        :param recipient: 接受者
        :param amount: 数量
        :return: 下一个区块的index
        '''
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        '''
        计算区块的hash值
        :param block: 块
        :return:
        '''
        # 序列化成就送格式的string
        block_str = json.dumps(block, sort_keys=True)
        # hash对象 -》摘要信息
        return hashlib.sha256(block_str.encode()).hexdigest()

    @property
    def last_block(self) -> Dict[str, Any]:
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        '''
        寻找工作量证明：是否hash(last_proof, proof)以4个0开头
        :param last_proof: 上一个工作量证明
        :return:
        '''
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    def valid_proof(self, last_proof: int, proof: int) ->bool:
        '''
        是否hash(last_proof, proof)以4个0开头
        :param last_proof: previous proof
        :param proof: current proof
        :return:
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(guess_hash)
        return guess_hash[:4] == "0000"

# 实例化区块链
blockChain = BlockChain()

if __name__ == '__main__':
    t = time.time()
    print(t)  # 原始时间
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 日期格式化
    print(b"hello")

    b = BlockChain()
    b.new_transaction('', '', 10)
    # p = b.proof_of_word(100)
    # print(p)
