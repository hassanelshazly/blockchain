import time

from transaction import Transaction
from block import Block
from util import *

BLOCK_GENERATION_INTERVAL = 0.01


class Blockchain:
    def __init__(self) -> None:
        self.chains = [[Block.genesis()]]
        self.status = "trusted"
        self.set_difficulty(BLOCK_GENERATION_INTERVAL)
        

    def __repr__(self) -> str:
        return (
            "Blockchain(\n"
            f"\tdifficulty: {self.difficulty}\n"
            f"\tchains: {self.chains}\n"
            ")"
        )
    
    def simple_repr(self):
        chains = [f"\tchain_{idx}: {[block.hash[0:8] for block in chain]}\n" for idx, chain in enumerate(self.chains)]
        return (
            "Blockchain(\n" +
            f"\tdifficulty: {self.difficulty}\n" +
            "".join(chains) +
            ")"
        )
    
    @staticmethod
    def get_block_idx(chain, block_hash) -> int:
        for idx, block in reversed(list(enumerate(chain))):
            if block.hash == block_hash:
                return idx
        return -1

    def add_block(self, block) -> None:
        self.chains.sort(key=lambda chain: -len(chain))

        appeneded_to_chain = False
        for chain in self.chains:
            block_idx = Blockchain.get_block_idx(chain, block.prev_hash)
            if block_idx == -1:
                continue
    
            if block_idx == len(chain) - 1:
                chain.append(block)
            else:
                self.chains.append(chain[:block_idx + 1] + [block])
            appeneded_to_chain = True
            break

        if not appeneded_to_chain:
            raise Exception("Block not found")

    def get_chain_by_hash(self, block_hash) -> list:
        return [chain for chain in self.chains if block_hash == chain[-1].hash][0]
    

    def status(self):
        chain_lens = [len(chain) for chain in self.chains]
        if len(chain_lens) == 1:
            return "trusted"
        chain_lens = sorted(chain_lens).reverse()
        if chain_lens[0] - chain_lens[1] >= 5:
            return "trusted"
        else:
            return "untrusted"
        

    @staticmethod
    def is_valid_chain(chain, difficulty) -> bool:
        if chain[0] != Block.genesis():
            raise Exception("Genesis Block mismatch")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(block, last_block, difficulty)

    def set_difficulty(self, interval) -> None:
        self.difficulty = 1
        curr_timestamp = time.time_ns()
        transactions_root = Transaction().root()
        mined_block = Block.mine_block(Block.genesis(), transactions_root, self.difficulty)

        while curr_timestamp - mined_block.timestamp  < interval * 1000 * 1000 * 1000:
            self.difficulty += 1
            mined_block = Block.mine_block(Block.genesis(), transactions_root, self.difficulty)
            curr_timestamp = time.time_ns()
        print("Estimated difficulty for", interval, "interval is:", self.difficulty, "zeors")
