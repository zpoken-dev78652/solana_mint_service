import json

import base58
from cryptography.fernet import Fernet
from solana.keypair import Keypair

from ..metaplex.transactions import deploy, topup, mint, send, burn, update_token_metadata
from ..utils.execution_engine import execute


class MetaplexAPI:

    def __init__(self, json_key_path: str, api_endpoint: str):
        with open(json_key_path, "r") as file:
            lines = file.read()[1:-1].split(',')
        key = [int(i) for i in lines]
        keypair = Keypair.from_secret_key(bytes(key))

        cfg = {
            "PRIVATE_KEY": base58.b58encode(keypair.seed).decode("ascii"),
            "PUBLIC_KEY": str(keypair.public_key),
            "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
        }

        self.private_key = list(base58.b58decode(cfg["PRIVATE_KEY"]))[:32]
        self.public_key = cfg["PUBLIC_KEY"]
        self.keypair = keypair
        self.cipher = Fernet(cfg["DECRYPTION_KEY"])
        self.api_endpoint = api_endpoint

    def wallet(self):
        """ Generate a wallet and return the address and private key. """
        keypair = Keypair()
        pub_key = keypair.public_key
        private_key = list(keypair.seed)
        return json.dumps(
            {
                'address': str(pub_key),
                'private_key': private_key
            }
        )

    def deploy(
            self, name,
            symbol, fees,
            max_retries=3,
            skip_confirmation=False,
            max_timeout=60,
            target=20, finalized=True
    ):
        """
        Deploy a contract to the blockchain (on network that support contracts). Takes the network ID and contract name, plus initialisers of name and symbol. Process may vary significantly between blockchains.
        Returns status code of success or fail, the contract address, and the native transaction data.
        """
        try:
            tx, signers, contract = deploy(self.api_endpoint, self.keypair, name, symbol, fees)
            print(contract)
            resp = execute(
                self.api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["contract"] = contract
            resp["status"] = 200
            return resp
        except:
            return {"status": 400}

    def topup(self, to, amount=None, max_retries=3, skip_confirmation=False, max_timeout=60, target=20,
              finalized=True):
        """
        Send a small amount of native currency to the specified wallet to handle gas fees. Return a status flag of success or fail and the native transaction data.
        """
        try:
            tx, signers = topup(self.api_endpoint, self.keypair, to, amount=amount)
            resp = execute(
                self.api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return resp
        except:
            return {"status": 400}

    def mint(self, contract_key, link, max_retries=3, skip_confirmation=False, max_timeout=60,
             target=20, finalized=True, supply=1):
        """
        Mints an NFT to an account, updates the metadata and creates a master edition
        """
        tx, signers = mint(self.api_endpoint, self.keypair, contract_key, self.private_key, link, supply=supply)
        resp = execute(
            self.api_endpoint,
            tx,
            signers,
            max_retries=max_retries,
            skip_confirmation=skip_confirmation,
            max_timeout=max_timeout,
            target=target,
            finalized=finalized,
        )
        resp["status"] = 200
        return resp
        # except:
        #     return json.dumps({"status": 400})

    def update_token_metadata(self, mint_token_id, link, data, creators_addresses, creators_verified,
                              creators_share, fee, max_retries=3, skip_confirmation=False, max_timeout=60, target=20,
                              finalized=True, supply=1):
        """
        Updates the json metadata for a given mint token id.
        """
        tx, signers = update_token_metadata(self.api_endpoint, self.keypair, mint_token_id, link, data, fee,
                                            creators_addresses, creators_verified, creators_share)
        resp = execute(
            self.api_endpoint,
            tx,
            signers,
            max_retries=max_retries,
            skip_confirmation=skip_confirmation,
            max_timeout=max_timeout,
            target=target,
            finalized=finalized,
        )
        resp["status"] = 200
        return resp

    def send(self, contract_key, sender_key, dest_key, encrypted_private_key, max_retries=3,
             skip_confirmation=False, max_timeout=60, target=20, finalized=True):
        """
        Transfer a token on a given network and contract from the sender to the recipient.
        May require a private key, if so this will be provided encrypted using Fernet: https://cryptography.io/en/latest/fernet/
        Return a status flag of success or fail and the native transaction data. 
        """
        try:
            private_key = list(self.cipher.decrypt(encrypted_private_key))
            tx, signers = send(self.api_endpoint, self.keypair, contract_key, sender_key, dest_key, private_key)
            resp = execute(
                self.api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return resp
        except:
            return {"status": 400}

    def burn(self, contract_key, owner_key, encrypted_private_key, max_retries=3, skip_confirmation=False,
             max_timeout=60, target=20, finalized=True):
        """
        Burn a token, permanently removing it from the blockchain.
        May require a private key, if so this will be provided encrypted using Fernet: https://cryptography.io/en/latest/fernet/
        Return a status flag of success or fail and the native transaction data.
        """
        try:
            private_key = list(self.cipher.decrypt(encrypted_private_key))
            tx, signers = burn(self.api_endpoint, contract_key, owner_key, private_key)
            resp = execute(
                self.api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return json.dumps(resp)
        except:
            return json.dumps({"status": 400})
