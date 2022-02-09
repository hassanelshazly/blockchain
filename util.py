import random
import string
import json
import hashlib

HASH_LENGTH = 258

def rondom_string(len):
  letters = string.ascii_lowercase
  ''.join(random.choice(letters) for i in range(len))

def rondom_double():
  return random.random()


def crypto_hash(*args) -> str:
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = "".join(stringified_args)

    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()

def starts_with_n_zeros(hash: str, n: int) -> bool:
    return len(bin(int(hash, 16))) <= HASH_LENGTH - n
