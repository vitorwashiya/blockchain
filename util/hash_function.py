import hashlib
import json
from blockchain.ENVIRONMENT_VARIABLES import HEX_TO_BINARY_CONVERSION_TABLE


def hex_to_binary(hex_string):
    binary_string = ""
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]
    return binary_string


def hash_function(*args, encoding="utf-8"):
    """
    Return a sha-256 hash of the given arguments.
    """
    str_args = sorted(map(json.dumps, args))
    joined_data = "".join(str_args)
    return hashlib.sha256(joined_data.encode(encoding)).hexdigest()


def main():
    j = {"a": 1}
    print(f"hash('foo'): {hash_function('one', 2, [3])}")
    print(f"hash('foo'): {hash_function(2, [3], 'one')}")

    number = 451
    hex_number = hex(number)[2:]
    print(f"hex_number: {hex_number}")

    binary_number = hex_to_binary(hex_number)
    print(f"binary_number: {binary_number}")

    original_number = int(binary_number, 2)
    print(f"original_number: {original_number}")

    hex_to_binary_hash = hex_to_binary(hash_function("test-data"))
    print(f"hex to binary hash: {hex_to_binary_hash}")


if __name__ == "__main__":
    main()
