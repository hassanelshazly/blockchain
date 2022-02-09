import time

from transaction import Transaction
from blockchain import *
from util import *

ATTACK_START = 5
ATTACK_HEIGHT = 5
ATTACK_POWER = 0.49
BLOCK_DIFFERENCE_LIMIT = 5

def check_attack(blockchain, honest_prev_block, attacker_prev_block):
    honest_chain = blockchain.get_chain_by_hash(honest_prev_block.hash)
    attacker_chain = blockchain.get_chain_by_hash(attacker_prev_block.hash)
    print("\rHonest chain length:", len(honest_chain), "\tAttacker chain length:", len(attacker_chain), end="")
    if len(attacker_chain) - len(honest_chain) >= BLOCK_DIFFERENCE_LIMIT:
        print("\n\nAttack won!")
        print("Honest chain length:", len(honest_chain))
        print("Attacker chain length:", len(attacker_chain))
        return True
    elif len(honest_chain) - len(attacker_chain) >= BLOCK_DIFFERENCE_LIMIT:
        print("\n\nAttack lost!")
        print("Honest chain length:", len(honest_chain))
        print("Attacker chain length:", len(attacker_chain))
        return True
    return False


if __name__ == "__main__":
    blockchain = Blockchain()
    print("Chain with genesis block only")
    print(blockchain.simple_repr())

    honest_prev_block = Block.genesis()

    print("Mine a few blocks")
    for i in range(ATTACK_START + ATTACK_HEIGHT):
        transactions_root = Transaction().root()
        honest_prev_block = Block.mine_block(
            honest_prev_block, transactions_root, blockchain.difficulty
        )
        blockchain.add_block(honest_prev_block)
    print(blockchain.simple_repr())

    print("An attacker tries to mine his own blocks from the middle of the chain")
    chain = blockchain.get_chain_by_hash(honest_prev_block.hash)
    attacker_prev_block = chain[ATTACK_START]

    for i in range(ATTACK_HEIGHT):
        transactions_root = Transaction().root()
        attacker_prev_block = Block.mine_block(
            attacker_prev_block, transactions_root, blockchain.difficulty
        )
        blockchain.add_block(attacker_prev_block)
    print("Block Chain after the attack")
    print(blockchain.simple_repr())
    print("here the two chains are different but has the same length")

    honest_timestamp = time.time_ns()
    honest_nonce = 0
    honest_tx_root = Transaction().root()

    attacker_timestamp = time.time_ns()
    attacker_nonce = 0
    attacker_tx_root = Transaction().root()

    simulation_run = 0
    
    print("\nSimulation starts")
    print("Attack power:", ATTACK_POWER, "\n")

    # Here the honest miners and attackers will try to mine blocks with different speeds
    while True:
        try:
            if rondom_double() > ATTACK_POWER:
                # honest miners
                honest_hash = crypto_hash(
                    honest_timestamp, honest_prev_block.hash, honest_tx_root, honest_nonce
                )

                if starts_with_n_zeros(honest_hash, blockchain.difficulty):
                    honest_prev_block = Block(
                        honest_timestamp,
                        honest_prev_block.hash,
                        honest_tx_root,
                        honest_nonce,
                        honest_hash
                    )
                    blockchain.add_block(honest_prev_block)
                    
                    honest_timestamp = time.time_ns()
                    honest_nonce = 0
                    honest_tx_root = Transaction().root() 
                else:
                    honest_nonce += 1
            else:
                # attacker
                attacker_hash = crypto_hash(
                    attacker_timestamp, attacker_prev_block.hash, attacker_tx_root, attacker_nonce
                )

                if starts_with_n_zeros(attacker_hash, blockchain.difficulty):
                    attacker_prev_block = Block(
                        attacker_timestamp,
                        attacker_prev_block.hash,
                        attacker_tx_root,
                        attacker_nonce,
                        attacker_hash,
                    )
                    blockchain.add_block(attacker_prev_block)

                    attacker_timestamp = time.time_ns()
                    attacker_nonce = 0
                    attacker_tx_root = Transaction().root()
                else:
                    attacker_nonce += 1
            if(check_attack(blockchain, honest_prev_block, attacker_prev_block)):
                print("\nSimulation loops:", simulation_run)
                break
            simulation_run += 1
        except KeyboardInterrupt:
            print("\n\nSimulation loops:", simulation_run)
            break
