from util.hash_function import hash_function, hex_to_binary


def test_hash_function():
    # It should create the same hash with arguments of different data types in any order
    assert hash_function(1, [2], "three") == hash_function("three", 1, [2])
    assert hash_function("foo") == "b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b"


def test_hex_to_binary():
    original_number = 789
    hex_number = hex(original_number)[2:]
    binary_number = hex_to_binary(hex_number)
    assert int(binary_number, 2) == original_number
