import os

from utils.account import Account
from utils.infura import Infura
from utils.ipfs import IPFS
from utils.crypto import HDPrivateKey
from utils.repo import Repo
from utils.config import Config

dir_path = os.path.dirname(os.path.realpath(__file__))
CONTRACT_BIN = os.path.join(dir_path, '../contract/contract_Repo_sol_Repo.bin')
CONTRACT_ABI = os.path.join(dir_path, '../contract/contract_Repo_sol_Repo.abi')

CONFIG_PATH = os.path.join(os.environ['HOME'], '.lly')

class Client(object):
    def __init__(self):
        self.config = Config(CONFIG_PATH, 'DEFAULT')

        eth_net = self.config.attributes['eth_net'] if 'eth_net' in self.config.attributes else 'mainnet'

        if 'infura_token' in self.config.attributes:
            self.infura = Infura(self.config.attributes['infura_token'], eth_net)
            self.account = Account(self.config, self.infura)
            self.repo = Repo(self.account, self.infura, CONTRACT_BIN, CONTRACT_ABI)

        if 'ipfs_gateway' in self.config.attributes:
            self.ipfs = IPFS(self.config.attributes['ipfs_gateway'])
