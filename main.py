import time

import requests

from cryptocurrency.wallet import Wallet

PORT = 5000
BASE_URL = f"http://localhost:{PORT}"


def get_blockchain():
    return requests.get(f"{BASE_URL}/blockchain").json()


def get_blockchain_mine():
    return requests.get(f"{BASE_URL}/blockchain/mine").json()


def post_wallet_transact(recipient, amount):
    return requests.post(
        f"{BASE_URL}/wallet/transact",
        json={"recipient": recipient, "amount": amount}
    ).json()


def get_wallet_info():
    return requests.get(f"{BASE_URL}/wallet/info").json()


def main():
    start_blockchain = get_blockchain()
    print(f"\nstart_blockchain: {start_blockchain}")

    recipient = Wallet().address
    post_wallet_transact_1 = post_wallet_transact(recipient, 21)
    print(f"\npost_wallet_transact_1: {post_wallet_transact_1}")
    time.sleep(1)
    post_wallet_transact_2 = post_wallet_transact(recipient, 13)
    print(f"\npost_wallet_transact_2: {post_wallet_transact_2}")

    time.sleep(1)
    mined_block = get_blockchain_mine()
    print(f"\nmined_block: {mined_block}")

    time.sleep(1)
    wallet_info = get_wallet_info()
    print(f"\nwallet_info: {wallet_info}")

    # from blockchain.ENVIRONMENT_VARIABLES import SECONDS
    # blockchain = Blockchain()
    # times = []
    # for i in range(20):
    #     start_time = time.time_ns()
    #     blockchain.add_block(i)
    #     end_time = time.time_ns()
    #
    #     time_to_mine = (end_time - start_time) / SECONDS
    #     times.append(time_to_mine)
    #
    #     average_time = sum(times) / len(times)
    #     print(f"Time to mine new block: {time_to_mine} s")
    #     print(f"New block difficulty: {blockchain.chain[-1].difficulty}")
    #     print(f"average_time: {average_time}\n")
    #
    # print(blockchain)

    # foo_blockchain = Blockchain()
    # foo_blockchain.add_block('one')
    # foo_blockchain.add_block('two')
    # foo_blockchain.add_block('three')

    # print(foo_blockchain)


if __name__ == "__main__":
    main()
