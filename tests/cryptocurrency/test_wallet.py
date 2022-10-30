from cryptocurrency.wallet import Wallet
from blockchain.blockchain import Blockchain
from blockchain.ENVIRONMENT_VARIABLES import STARTING_BALANCE
from cryptocurrency.transaction import Transaction


def test_verify_valid_signature():
    data = {"foo": "test_data"}
    wallet = Wallet()
    signature = wallet.sign_data(data)

    assert Wallet.verify_data_signature(wallet.public_key, data, signature)


def test_verify_invalid_signature():
    data = {"foo": "test_data"}
    wallet = Wallet()
    signature = wallet.sign_data(data)

    assert not Wallet.verify_data_signature(Wallet().public_key, data, signature)


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Transaction(wallet, "recipient", amount)
    blockchain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount

    received_amount_1 = 25
    received_transaction_1 = Transaction(Wallet(), wallet.address, received_amount_1)
    received_amount_2 = 50
    received_transaction_2 = Transaction(Wallet(), wallet.address, received_amount_2)

    blockchain.add_block([received_transaction_1.to_json(), received_transaction_2.to_json()])

    assert Wallet.calculate_balance(blockchain,
                                    wallet.address) == STARTING_BALANCE - amount + received_amount_1 + received_amount_2
