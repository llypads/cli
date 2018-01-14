"""The init command."""
from .base import Base

from json import dumps
import sys

from protos.repo_pb2 import Repo
from ethereum.utils import denoms
from utils.cli import query_yes_no

class Init(Base):
    """lly init"""

    def run(self):
        from utils.client import Client
        from utils.crypto import HDPrivateKey

        client = Client()

        import_mnemonic = query_yes_no("Would you like to import an ethereum wallet using a mnemonic phrase?")
        if import_mnemonic:
            mnemonic = input("Enter mnemonic phrase: ")
            master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
        else:
            master_key, mnemonic = HDPrivateKey.master_key_from_entropy()
            print("Generated wallet with mnemonic: %s" % mnemonic)

        client.config.attributes['mnemonic'] = mnemonic

        eth_net = self.query_network("Which ethereum network would you like to use?")
        print('Using ethereum network: %s' % eth_net)
        client.config.attributes['eth_net'] = eth_net

        default_gas_price = self.query_default_gas_price("Default gas price in gwei:")
        print('Using default gas price: %dgwei' % default_gas_price)

        client.config.attributes['default_gas_price'] = str(int(default_gas_price) * denoms.gwei)
        client.config.attributes['ipfs_gateway'] = '127.0.0.1'
        client.config.attributes['infura_token'] = 'nuux6RAf126jNtpRZJO0'

        client.config.write()

    def query_network(self, question):
        default="mainnet"
        valid = {
            "mainnet": True,
            "ropsten": True
        }
        prompt = " [MAINNET/ropsten] "

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if choice == '':
                return default
            elif choice in valid:
                return choice
            else:
                sys.stdout.write("Possible networks are \"mainnet\" or \"ropsten\".\n")

    def query_default_gas_price(self, question):
        default=15
        prompt = " [%d] " % default

        while True:
            sys.stdout.write(question + prompt)
            choice = input()
            if choice == '':
                return default
            elif choice.isdigit():
                return int(choice)
            else:
                sys.stdout.write("Please enter a valid gas price i.e. 15\n")
