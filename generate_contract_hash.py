import json
import hashlib
import requests
import os
import time

asset_name = os.environ['ASSET_NAME']
asset_ticker = os.environ['ASSET_TICKER']

address = os.popen(
    f'docker run elements-cli getnewaddress'
).read()

address_info = os.popen(
    f'docker run elements-cli getaddressinfo {address}'
).read()

pubkey = json.loads(address_info)['pubkey']

contract = {
    "entity": {"domain": "reusable-asset-domain.herokuapp.com"},
    "issuer_pubkey": pubkey,
    "name": asset_name,
    "precision": 0,
    "ticker": asset_ticker,
    "version": 0,
}

contract_json = json.dumps(contract, sort_keys=True).replace(
    " ", ""
)
contract_hash = hashlib.sha256(contract_json.encode("ascii")).hexdigest()
contract_hash_reversed = (bytes.fromhex(contract_hash)[::-1]).hex()

asset_result_json = os.popen(
    f'docker run elements-cli issueasset 10 0 false "{contract_hash_reversed}"'
).read()

asset_result = json.loads(asset_result_json)
asset_id = asset_result["asset"]

print(f'Link to your asset: https://blockstream.info/liquidtestnet/asset/{asset_id}')

print("Waiting for confirmation...")
TWO_MINUTES = 120
time.sleep(TWO_MINUTES)

print("Registering...")
url = "https://assets-testnet.blockstream.info/"
payload = json.dumps({"asset_id": asset_id, "contract": json.loads(contract_json)})
response = requests.post(url, data=payload)
print(response.text)
