"""The account command."""
from .initialized_base import InitializedBase

from json import dumps
import sys

from ethereum.utils import denoms

class Account(InitializedBase):
    """lly account"""

    def run(self):
        if not self.initialized:
            return

        attributes = self.client.config.attributes
        print(" Account config:")
        print("\tMnemonic: %s" % attributes['mnemonic'])

        if self.options["--private-key"]:
            print("\tPrivate key: %s" % self.client.account.private_key.to_hex())

        print("\tPublic address: %s" % self.client.account.public_key)
        print("\tDefault gas price: %sgwei" % str(int(int(attributes['default_gas_price']) / denoms.gwei)))
        print("\tBalance: %s" % self.client.account.balance)

    # def send(self, address, amount):
    #     response = self.client.account.send_transaction(100, 100000, value=amount, to=address)
    #     print(response.json())
