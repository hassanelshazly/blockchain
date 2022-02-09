from util import *

class Transaction:
    def __init__(self) -> None:
        self.from_pub = rondom_string(10)
        self.to_pub = rondom_string(10)
        self.amount = rondom_double()
        
    def root(self) -> str:
        return crypto_hash(self.from_pub, self.to_pub, self.amount)

    @staticmethod
    def genesis_root() -> str:
        return crypto_hash("0")

    def __repr__(self) -> str:
        return (
            "Transaction("
            f"from: {self.from_pub}, "
            f"to: {self.to_pub}, "
            f"amount: {self.amount})"
        )
