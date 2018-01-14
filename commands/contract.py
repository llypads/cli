"""The contract command."""
from .initialized_base import InitializedBase

import json
import sys

class Contract(InitializedBase):
    """lly exec"""

    def transact(self):
        address = self.options["<address>"]
        function = self.options["<function>"]
        args = json.loads(self.options["--args"])

        def confirm():
            print("Creating transaction")
            response = self.client.repo.transact(address, function, args)
            if 'result' in response:
                address = response['result']
                print("Success. Transaction: %s" % address)
            else:
                print(response)

        def reject():
            print("Transaction cancelled")

        self.execute("Calling contract %s::%s(%s)" % (address, function, json.dumps(args)), 210000, confirm, reject)

    def call(self):
        address = self.options["<address>"]
        function = self.options["<function>"]
        args = json.loads(self.options["--args"])

        print("Calling function %s::%s(%s)" % (address, function, json.dumps(args)))
        response = self.client.repo.call(address, function, args)
        if 'result' in response:
            result = response['result']
            print("Success. Result: %s" % result)
        else:
            print(response)

    def run(self):
        if not self.initialized:
            return

        if self.options['transact']:
            self.transact()
        elif self.options['call']:
            self.call()
        elif self.options['send']:
            self.send()
