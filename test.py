import os

from utils.config import Config
from utils.account import Account
from utils.infura import Infura
from utils.ipfs import IPFS

CONFIG_PATH = os.path.join(os.environ['HOME'], '.lly')

config = Config(CONFIG_PATH, 'DEFAULT')
infura = Infura(config.attributes['infura_token'], config.attributes['eth_net'])
ipfs = IPFS('127.0.0.1', 5001)
account = Account(config, infura)

res = ipfs.connection.add_bytes(b'boom')
import pdb; pdb.set_trace()
