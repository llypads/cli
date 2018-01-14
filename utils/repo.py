import binascii
import json

from ethereum.abi import ContractTranslator
from ethereum.utils import sha3, encode_hex, zpad

class Repo(object):
    def __init__(self, account, infura, bin_path, abi_path):
        self.account = account
        self.infura = infura

        with open(bin_path, 'rb') as contract_file:
            contract_bin = contract_file.read().replace(b"\n", b"")
            self.contract_bin = binascii.unhexlify(contract_bin)

        with open(abi_path, 'r') as abi_file:
            self.contract = ContractTranslator(json.load(abi_file))

    def create(self, ref_head, gasprice, startgas):
        constructor_args = self.contract.encode_constructor_arguments([ref_head])
        tx, response = self.account.send_transaction(gasprice, startgas, self.contract_bin + constructor_args)
        contract_address = '0x' + encode_hex(tx.creates)
        return contract_address, response.json()

    def transact(self, contract_address, function, args, value=0, gasprice=15000000000, gaslimit=140000):
        txdata = self.contract.encode_function_call(function, args)
        tx, response = self.account.send_transaction(gasprice, gaslimit, txdata, to=contract_address, value=value)
        return response.json()

    def call(self, contract_address, function, args):
        txdata = self.contract.encode_function_call(function, args)
        params = {
            "params": json.dumps([{
                "to": contract_address,
                "data": "0x" + encode_hex(txdata)
            }, 'latest'])
        }

        response = self.infura.get('eth_call', params).json()

        if 'result' in response and response['result'] == '0x':
            response['result'] = []
        elif 'result' in response:
            response['result'] = self.contract.decode_function_result(function, binascii.unhexlify(response['result'][2:]))
        return response
