import requests

def encode_address(address):
    return "{0:#0{1}x}".format(address, 42)

def current_price():
    response = requests.get("https://api.infura.io/v1/ticker/ethusd")
    return response.json()
