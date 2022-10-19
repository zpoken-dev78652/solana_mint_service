import time

import requests


class ChronicleDriver:
    api_key: str
    base_url: str

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def notify_on_successful_mint(self, nft_id, token_id):
        url = f"{self.base_url}/api/v1/nft/{nft_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        body = {
            "auth_token": self.api_key,
            "tokenId": token_id
        }

        retry = 0
        res = requests.post(url=url, headers=headers, json=body)
        while not res.ok and retry < 20:
            time.sleep(5)
            retry += 1
            res = requests.post(url=url, headers=headers, json=body)

        return res.ok
