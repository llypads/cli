import json
import os
import ipfsapi

class IPFS(object):
    def __init__(self, gateway, base=None):
        self.connection = ipfsapi.connect(gateway)
