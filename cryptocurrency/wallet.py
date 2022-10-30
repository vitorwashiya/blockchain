import uuid
import json
from blockchain.ENVIRONMENT_VARIABLES import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miner`s balance.
    Allows a miner to authorize transactions.
    """

    def __init__(self, blockchain=None):
        self.address = str(uuid.uuid4())
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        self.public_key = self.serialized_public_key()
        self.blockchain = blockchain

    @property
    def balance(self):
        return self.calculate_balance(self.blockchain, self.address)

    def sign_data(self, data, encoding="utf-8"):
        """
        Generate a signature based on the data using the local private key.
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode(encoding),
            ec.ECDSA(hashes.SHA256())
        ))

    @staticmethod
    def verify_data_signature(public_key, data, signature, encoding="utf-8"):
        """
        Verify a signature based on the original public key and data.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode("utf-8"),
            default_backend()
        )
        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode(encoding),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    def serialized_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        public_key = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")
        return public_key

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calcualte the balance of the given address considering the transaction data within the blockchain.

        The balance is found by adding the output values that belong to the address since the most recent
        transaction by that address
        """
        balance = STARTING_BALANCE
        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction["input"]["address"] == address:
                    # any time the address conducts a new transaction it resets its balance
                    balance = transaction["output"][address]
                elif address in transaction["output"]:
                    balance += transaction["output"][address]
        return balance


def main():
    wallet = Wallet()
    print(f"wallet: {wallet.__dict__}")

    data = {"foo": "bar"}
    signature = wallet.sign_data(data)
    print(f"signature: {signature}")

    should_be_valid = Wallet.verify_data_signature(wallet.public_key, data, signature)
    print(f"should_be_valid: {should_be_valid}")

    should_be_invalid = Wallet.verify_data_signature(Wallet().public_key, data, signature)
    print(f"should_be_invalid: {should_be_invalid}")


if __name__ == "__main__":
    main()
