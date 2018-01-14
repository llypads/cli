import configparser
import json
import rlp

from ethereum.transactions import Transaction

from utils.crypto import HDPrivateKey, HDKey

class Account(object):
    def __init__(self, config, infura):
        self.infura = infura
        self.config = config
        self.master_key = HDPrivateKey.master_key_from_mnemonic(self.config.attributes['mnemonic'])
        self.root_keys = HDKey.from_path(self.master_key, "m/44'/60'/0'")
        self.acct_priv_key = self.root_keys[-1]
        self.acct_pub_key = self.acct_priv_key.public_key

    def send_transaction(self, gasprice, startgas, tx_data='', to='', value=0):
        tx = Transaction(
            nonce=self.transaction_count,
            gasprice=gasprice,
            startgas=startgas,
            to=to,
            value=value,
            data=tx_data,
        )

        tx.sign(self.private_key.to_hex())
        raw_tx = rlp.encode(tx)
        raw_tx_hex = raw_tx.hex()

        payload = {
          "jsonrpc": "2.0",
          "id": 0,
          "method": "eth_sendRawTransaction",
          "params": ['0x' + raw_tx_hex]
        }

        request = self.infura.post(payload)
        return tx, request

    @property
    def transaction_count(self):
        params = {
            "params": json.dumps([self.public_key, 'pending'])
        }
        request = self.infura.get('eth_getTransactionCount', params)
        response = request.json()

        count = int(response['result'], 16)
        return count

    @property
    def balance(self):
        params = {
            "params": json.dumps([self.public_key, 'latest'])
        }
        request = self.infura.get('eth_getBalance', params)
        response = request.json()
        balance = int(response['result'], 16)
        return balance

    @property
    def mnemonic(self):
        """Get menomic phrase"""
        return self.config.attributes['mnemonic']

    @mnemonic.setter
    def mnemonic(self, mnemonic):
        self.config.attributes['mnemonic'] = mnemonic
        self.config.write()

    @property
    def public_key(self):
        path_public_keys = HDKey.from_path(self.acct_pub_key, '{change}/{index}'.format(change=0, index=0))
        path_public_key = path_public_keys[-1]
        address = path_public_key.address()
        return address

    @property
    def private_key(self):
        path_private_keys = HDKey.from_path(self.acct_priv_key, '{change}/{index}'.format(change=0, index=0))
        path_private_key = path_private_keys[-1]
        return path_private_key._key
