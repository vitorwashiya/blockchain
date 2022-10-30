import time

from blockchain.ENVIRONMENT_VARIABLES import GENESIS_DATA, MINE_RATE
from util.hash_function import hash_function, hex_to_binary


class Block:
    """
    Block: a unit of storage
    Store transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE
        Increase the difficulty for quickly mined blocks.
        Decrease the difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    def mine_block(self, last_block, data):
        """
        Mine a block base on the given last_block and data, until a block hash is found that meets the
        leading 0's proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = self.adjust_difficulty(last_block, timestamp)
        nonce = 0

        hash = hash_function(timestamp, last_hash, data, difficulty, nonce)
        while hex_to_binary(hash)[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = hash_function(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing the following rules
            - the block must have proper last_hash reference
            - the block must meet the proof of work requirements
            - the difficulty must only adjust by 1
            - the block hash must be a valid combination of the block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception("The block last_hash must be correct")
        if hex_to_binary(block.hash)[0:block.difficulty] != "0" * block.difficulty:
            raise Exception("The proof of work requirement was not met")
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("The block difficulty must only adjust by 1")
        reconstructed_hash = hash_function(
            block.timestamp
            , block.last_hash
            , block.data
            , block.nonce
            , block.difficulty
        )
        if block.hash != reconstructed_hash:
            raise Exception("The block hash must be correct")

    @staticmethod
    def genesis_block():
        """
        Generate the genesis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block`s json representation back into a block isntance
        """
        return Block(**block_json)

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes
        """
        return self.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"hash: {self.hash}, "
            f"data: {self.data}, "
            f"difficulty: {self.difficulty}, "
            f"nonce: {self.nonce})"
        )


def main():
    genesis = Block.genesis_block()
    good_block = Block.mine_block(Block, genesis, "foo")
    # bad_block.last_hash = "Evil Data"
    print(abs(genesis.difficulty - good_block.difficulty))
    try:
        Block.is_valid_block(genesis, good_block)
    except Exception as e:
        print(f"is_valid_block: {e}")


if __name__ == "__main__":
    main()
