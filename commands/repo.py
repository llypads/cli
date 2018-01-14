"""The repo command."""
from .initialized_base import InitializedBase

import base58
from json import dumps
import sys

from ethereum.utils import denoms, encode_hex

from utils.cli import query_yes_no
from utils.eth import current_price, encode_address

class Repo(InitializedBase):
    """lly repo commands"""

    def run(self):
        if not self.initialized:
            return

        if self.options['status']:
            self.status()
        elif self.options['deploy']:
            self.deploy()
        elif self.options['create-bounty']:
            self.create_bounty()

    def deploy(self):
        def confirm(gas_price, gas_limit):
            ref_head = "refs/heads/master"
            contract_address, response = self.client.repo.create(ref_head, gas_price, gas_limit)
            if 'result' in response:
                address = response['result']
                print("\nContract deploying...")
                print("  Address: %s" % contract_address)
                print("  Transaction: %s" % (address))
                print("\n  https://etherscan.io/tx/%s\n" % (address))


            else:
                print(response)
        def reject():
            print("Rejected")

        self.execute("Deploying repository contract", 850000, confirm, reject)

    def status(self):
        address = self.options['<address>']
        # Get head ref
        response = self.client.repo.call(address, 'getHead', [])
        ref_head = response['result'][0].decode("utf-8")

        # Get anchor for ref
        response = self.client.repo.call(address, 'getRef', [ref_head])
        ref_anchor = response['result'][0]

        print("\n Repo: %s" % address)
        print(" Refs (ref -> git hash -> ipfs hash):")
        if int.from_bytes(ref_anchor, byteorder="little") > 0:
            response = self.client.repo.call(address, 'getAnchor', [ref_anchor])
            content_address = response['result'][0]
            print("  ", ref_head, "->", encode_hex(ref_anchor)[:40], "->", base58.b58encode(b'\x12 ' + content_address))
        else:
            print("  ", ref_head, "->", encode_hex(ref_anchor)[:40])

    def create_bounty(self):
        bounty_id = self.options['<bountyid>']

        def confirm(gas_price, gas_limit):
            address = self.options['<address>']
            response = self.client.repo.transact(address, "createBounty", [bounty_id, 'active'], value=1, gasprice=gas_price, gaslimit=gas_limit)
            if 'result' in response:
                address = response['result']
                print("\nCreating transaction:")
                print("  Transaction: %s" % address)
                print("\n  https://etherscan.io/tx/%s\n" % (address))

            else:
                print(response)
        def reject():
            print("Rejected")

        self.execute("Creating bounty", 30000, confirm, reject)
