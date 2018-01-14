import json
import os
import requests

class Infura(object):
    def __init__(self, api_token, eth_net='mainnet'):
        self.api_token = api_token
        self.base_url = os.path.join('https://api.infura.io/v1/jsonrpc/', eth_net)

    def get(self, method, params):
        params['token'] = self.api_token
        url = os.path.join(self.base_url, method)
        return requests.get(url, params)

    def post(self, payload):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        return requests.post(self.base_url + '?%s' % self.api_token, data=json.dumps(payload), headers=headers)
