import time

from blockchain.ENVIRONMENT_VARIABLES import MINING_REWARD_INPUT
from cryptocurrency.transaction import Transaction
from cryptocurrency.wallet import Wallet

from blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis_block()]

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block.mine_block(Block, last_block, data)
        self.chain.append(new_block)

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - blocks must be formatted correctly
        """

        if chain[0] != Block.genesis_block():
            raise Exception("The genesis block must be valid")

        for i in range(1, len(chain)):
            last_block = chain[i - 1]
            block = chain[i]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions.
            - Each transaction must only appear once in the chain.
            - There can only be one mining reward per block.
            - Each transaction must be valid.
        """
        transactions_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transactions_json in block.data:
                transaction = Transaction.from_json(transactions_json)
                if transaction.id in transactions_ids:
                    raise Exception(f"Transaction {transaction.id} is not unique.")
                transactions_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            f"There can only be one mining reward per block. Check block with hash {block.hash}"
                        )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input["address"]
                    )
                    if historic_balance != transaction.input["amount"]:
                        raise Exception(f"Transaction {transaction.id} has an invalid input amount.")

                Transaction.is_valid_transaction(transaction)

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
            - The incoming chain is longer than the local one.
            - The incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. Incoming chain must be longer.")
        try:
            self.is_valid_chain(chain)
            self.chain = chain
        except Exception as e:
            raise Exception(f"Cannot replace. Incoming chain is invalid: {e}")

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return [block.to_json() for block in self.chain]

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain  a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = [Block.from_json(block) for block in chain_json]
        return blockchain

    def __repr__(self):
        return f"Blockchain: {self.chain}"


def main():
    from blockchain.ENVIRONMENT_VARIABLES import SECONDS
    blockchain = Blockchain()
    times = []
    for i in range(1000):
        start_time = time.time_ns()
        blockchain.add_block(i)
        end_time = time.time_ns()

        time_to_mine = (end_time - start_time) / SECONDS
        times.append(time_to_mine)

        average_time = sum(times) / len(times)
        print(f"Time to mine new block: {time_to_mine} s")
        print(f"New block difficulty: {blockchain.chain[-1].difficulty}")
        print(f"average_time: {average_time}\n")


if __name__ == "__main__":
    main()
