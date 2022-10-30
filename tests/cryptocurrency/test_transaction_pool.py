from cryptocurrency.transaction_pool import TransactionPool
from cryptocurrency.transaction import Transaction
from cryptocurrency.wallet import Wallet
from blockchain.blockchain import Blockchain


def test_add_transaction_to_map():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), "recipient", 50)
    transaction_pool.add_transaction_to_map(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_blockchain_transaction():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), "recipient", 1)
    transaction_2 = Transaction(Wallet(), "recipient", 2)

    transaction_pool.add_transaction_to_map(transaction_1)
    transaction_pool.add_transaction_to_map(transaction_2)

    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json()])

    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transaction(blockchain)

    assert not transaction_1.id in transaction_pool.transaction_map
    assert not transaction_2.id in transaction_pool.transaction_map
