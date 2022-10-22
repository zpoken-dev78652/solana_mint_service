import json
import logging
import random
import time

from app import chronicle_driver
from app import metaplex_api
from app import redis_client
from app import solana_client
from utils.solana_driver.metaplex.metadata import get_metadata


def deploy_and_mint_in_blockchain(nft_token):
    deploy_response = metaplex_api.deploy("Chronicle NFT", "XNFT", 0)
    logging.info(f"Deploy: {deploy_response}")
    assert deploy_response["status"] == 200

    contract = deploy_response.get("contract")
    mint_response = metaplex_api.mint(contract, f"https://stage.xnl.zpoken.io/nft/id/{nft_token}")
    logging.info(f"Mint: {mint_response}")
    assert mint_response["status"] == 200
    return contract, mint_response


def validate_mint(request_key: str, nft_id: str, net='devnet'):
    token_id = redis_client.hget('token_id_by_nft_id', nft_id)
    if token_id:
        mint_request_key = redis_client.hget("mint_request_key_by_token_id", token_id)
        try:
            mint_request_result_json = redis_client.hget("request_results", mint_request_key)  # todo: try except
            redis_client.hset("request_results", request_key, mint_request_result_json)
        except Exception as err:
            raise Exception(err)
        redis_client.hget("request_results", request_key)
    else:
        token_id = len(redis_client.hgetall('token_id_by_nft_id'))
        logging.info(f"GOT NEW TOKEN ID {token_id}")
        try:
            contract, mint_response = deploy_and_mint_in_blockchain(nft_token=token_id)
        except TypeError as err:
            logging.info('---------------')
            logging.error(err)
            logging.error("error to mint")
            return None

        contract_metadata = get_metadata(solana_client, contract)
        token_uri = contract_metadata['data']['uri']
        owner = str(metaplex_api.public_key)
        redis_client.hset("mint_results", request_key, json.dumps(mint_response))

        try:
            mint_result_by_request_key = json.loads(redis_client.hget("mint_results", request_key))  # todo: try except
            logging.debug(mint_result_by_request_key)
            res = solana_client.get_confirmed_transaction(tx_sig=mint_result_by_request_key['result'])
        except Exception as err:
            logging.error(err)
            logging.error('failed to get results on solana')
            return None

        result = {
            'tokenId': token_id,
            'nftId': str(nft_id),
            'tokenURI': str(token_uri),
            'owner': str(owner),
            'gasUsed': res['result']['meta']['fee'],
            'mint': str(res['result']['meta']['postTokenBalances'][0]['mint']),
            'solanascanTransactionURL': f"https://explorer.solana.com/address/{res['result']['meta']['postTokenBalances'][0]['mint']}?cluster={net}"
        }
        redis_client.hset("request_results", request_key, json.dumps(result))
        try:
            redis_client.hget("request_results", request_key)
            redis_client.hset("mint_request_key_by_token_id", token_id, request_key)
        except Exception:
            return None

        redis_client.hset("token_id_by_nft_id", nft_id, token_id)

    return token_id


def poll():
    while True:
        nft_id = redis_client.lindex("token_mint_queue", 0)

        if nft_id:
            logging.info(f"nft_id={nft_id} in process")
            request_key = f"{int(time.time())}{random.choice(range(1000))}"
            token_id = validate_mint(request_key=request_key, nft_id=nft_id)
            logging.info(f'NEW TOKEN ID {token_id}')
            if token_id:
                a = nft_id.decode('utf-8')
                response = chronicle_driver.notify_on_successful_mint(nft_id=a, token_id=token_id.decode('utf-8'))
                match response.status_code:
                    case 400 | 500:
                        logging.error(response.text)
                        redis_client.rpush('token_mint_queue', nft_id)

                redis_client.lpop('token_mint_queue')
        else:
            logging.info('start sleep')

            logging.info('end sleep')
        time.sleep(2)


if __name__ == '__main__':
    poll()
