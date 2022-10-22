import json
import logging
from flask import jsonify
import time
from app import metaplex_api
from app import redis_client
from app import solana_client
from utils.solana_driver.metaplex.metadata import get_metadata

from config import Config

def await_full_confirmation(client, txn, max_timeout=60):
    if txn is None:
        return
    elapsed = 0
    while elapsed < max_timeout:
        sleep_time = 1
        time.sleep(sleep_time)
        elapsed += sleep_time
        resp = client.get_confirmed_transaction(txn)
        while 'result' not in resp:
            resp = client.get_confirmed_transaction(txn)
        if resp["result"]:
            print(f"Took {elapsed} seconds to confirm transaction {txn}")
            break

def mint_new_token(data: dict):

    nft_id = data["nft_id"]
    redis_client.rpush('token_mint_queue', nft_id)
    return {"ok": True}

    ## CONTRACT 'DHU9B5skQiFiFUf13mPtMpkYZSPTWTM2vdqdML7erBHs'

    # wallet2 = json.loads(metaplex_api.wallet())
    # address2 = wallet2.get('address')
    # encrypted_pk2 = metaplex_api.cipher.encrypt(bytes(wallet2.get('private_key')))
    # print(client.request_airdrop(metaplex_api.public_key, int(1e10)))
    # topup_response2 = json.loads(metaplex_api.topup(api_endpoint, address2))
    # print(f"Topup {address2}:", topup_response2)
    # # await_confirmation(client, topup_response2['tx'])
    # assert topup_response2["status"] == 200
    # send_response = json.loads(metaplex_api.send(api_endpoint, contract, address1, address2, encrypted_pk1))
    # assert send_response["status"] == 200
    # # await_confirmation(client, send_response['tx'])
    # burn_response = json.loads(metaplex_api.burn(api_endpoint, contract, address2, encrypted_pk2))
    # print("Burn:", burn_response)
    # # await_confirmation(client, burn_response['tx'])
    # assert burn_response["status"] == 200
    # print("Success!")


def get_token_info():
    ...


if __name__ == '__main__':
    mint_new_token({"nft_id": "11"})