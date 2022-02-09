import time

from transaction import Transaction
from util import *

class Block:
    def __init__(self, timestamp, prev_hash, transactions_root, nonce, hash) -> None:
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.transactions_root = transactions_root
        self.nonce = nonce
        self.hash = hash

    def __repr__(self) -> str:
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"prev_hash: {self.prev_hash}, "
            f"transactions_root: {self.transactions_root}, "
            f"nonce: {self.nonce}, "
            f"hash: {self.hash})"
        )

    @staticmethod
    def genesis():
        timestamp = 0
        prev_hash = "0" * 64
        transactions_root = Transaction.genesis_root()
        nonce = 0

        hash = crypto_hash(timestamp, prev_hash, transactions_root, nonce)
        while not starts_with_n_zeros(hash, 1):
            nonce += 1
            hash = crypto_hash(timestamp, prev_hash, transactions_root, nonce)

        return Block(timestamp, prev_hash, transactions_root, nonce, hash)

    @staticmethod
    def mine_block(last_block, transactions_root, difficulty):
        timestamp = time.time_ns()
        prev_hash = last_block.hash
        nonce = 0
        hash = crypto_hash(timestamp, prev_hash, transactions_root, nonce)

        while not starts_with_n_zeros(hash, difficulty):
            nonce += 1
            hash = crypto_hash(timestamp, prev_hash, transactions_root, nonce)

        return Block(timestamp, prev_hash, transactions_root, nonce, hash)

    @staticmethod
    def is_valid_block(last_block, block, difficulty) -> bool:
        if block.prev_hash != last_block.hash:
            raise Exception("Chain not connected")

        if not starts_with_n_zeros(hash, difficulty):
            raise Exception("PoW not met")

        reconstructed_hash = crypto_hash(
            block.timestamp, block.prev_hash, block.transactions_root, block.nonce
        )
        if block.hash != reconstructed_hash:
            raise Exception("Wrong hash")