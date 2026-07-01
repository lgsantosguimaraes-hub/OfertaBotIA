import os
import json
import time
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()


class ShopeeAPI:
    def __init__(self):
        self.url = os.getenv("SHOPEE_API_URL")
        self.app_id = os.getenv("SHOPEE_APP_ID")
        self.secret = os.getenv("SHOPEE_APP_SECRET")

    def execute(self, query: str, variables=None):

        payload = {
            "query": query
        }

        if variables:
            payload["variables"] = variables

        payload_json = json.dumps(
            payload,
            separators=(",", ":"),
            ensure_ascii=False
        )

        timestamp = str(int(time.time()))

        sign_string = (
            self.app_id +
            timestamp +
            payload_json +
            self.secret
        )

        signature = hashlib.sha256(
            sign_string.encode("utf-8")
        ).hexdigest()

        headers = {
            "Authorization": (
                f"SHA256 Credential={self.app_id}, "
                f"Timestamp={timestamp}, "
                f"Signature={signature}"
            ),
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.url,
            data=payload_json,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()