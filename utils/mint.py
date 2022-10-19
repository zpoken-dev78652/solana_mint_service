import argparse
import json

import base58
from cryptography.fernet import Fernet
from solana.keypair import Keypair


# def parse_commandline_arguments():
#     global divinity_json_file
#
#     parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#                                      description='Specify the json file')
#
#     parser.add_argument("-j", "--jsonf", dest="jsonf",
#                         type=str, help="Specify the json file from https://arweave.net")
#
#     args = parser.parse_args()
#     divinity_json_file = str(args.jsonf)


# def parse_commandline_arguments():
#     global divinity_json_file
#
#     parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#                                      description='Specify the json file')
#
#     parser.add_argument("-j", "--jsonf", dest="jsonf",
#                         type=str, help="Specify the json file from https://arweave.net")
#
#     args = parser.parse_args()
#     divinity_json_file = str(args.jsonf)


from utils.solana_driver import MetaplexAPI

if __name__ == '__main__':
    # parse_commandline_arguments()

    api = MetaplexAPI("/Users/alexriaronc/.config/solana/id.json")

    api_endpoint = "https://api.devnet.solana.com/"

    # requires a JSON file with metadata. best to publish on Arweave
    divinity_json_file = 'https://stage.xnl.zpoken.io/nft/id/99999'
    print(divinity_json_file)
    # deploy a contract. will return a contract key.

    # print(api.wallet())
    print("Deploy:")
    result = api.deploy("Chronicle NFT", "XNFT", fees=300)
    print("Deploy completed. Result: %s", result)

    print("Load contract key:")
    contract_key = json.loads(result).get('contract')
    print("Contract key loaded. Conract key: %s", contract_key)
    print("Mint:")
    # conduct a mint, and send to a recipient, e.g. wallet_2
    mint_res = api.mint(contract_key, divinity_json_file)
    print("Mint completed. Result: %s", mint_res)
