import json
import logging

from app import metaplex_api
from app import redis_client


def mint_new_token(data: dict):

    nft_id = data["nft_id"]
    res = redis_client.rpush('token_mint_queue', nft_id)

    divinity_json_file = f'https://stage.xnl.zpoken.io/nft/id/{res}'
    logging.info("Deploy:")
    result = metaplex_api.deploy("Chronicle NFT", "XNFT", fees=300)
    logging.info("Deploy completed. Result: %s", result)

    logging.info("Load contract key:")
    contract_key = json.loads(result).get('contract')
    logging.info("Contract key loaded. Contract key: %s", contract_key)
    logging.info("Mint:")
    mint_res = metaplex_api.mint(contract_key, divinity_json_file)
    logging.info("Mint completed. Result: %s", mint_res)


def get_token_info():
    ...
