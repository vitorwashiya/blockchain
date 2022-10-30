from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
from cryptocurrency.transaction import Transaction
from blockchain.block import Block

pn_config = PNConfiguration()
# pn_config.subscribe_key =
# pn_config.publish_key =
# pn_config.secret_key =
# pn_config.uuid =

CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK",
    "TRANSACTION": "TRANSACTION"
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f"\n-- Channel: {message_object.channel} | Message: {message_object.message}")

        if message_object.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain.copy()
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print(f"\n-- Successfully replaced the local chain")
            except Exception as e:
                print(f"\n-- Did not replace chain: {e}")
        elif message_object.channel == CHANNELS["TRANSACTION"]:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.add_transaction_to_map(transaction)
            print(f"\n Set the new transaction in the transaction pool")


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pn = PubNub(pn_config)
        self.pn.subscribe().channels(CHANNELS.values()).execute()
        self.pn.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pn.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS["BLOCK"], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        self.publish(CHANNELS["TRANSACTION"], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish("TEST", {"foo": "bar"})


if __name__ == "__main__":
    main()
