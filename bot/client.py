import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv


class BinanceRESTClient:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        if not self.api_key or not self.api_secret:
            raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env")

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _sign_params(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return f"{query_string}&signature={signature}"

    def ping(self):
        url = f"{self.base_url}/fapi/v1/ping"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def create_order(self, params: dict):
        params["timestamp"] = int(time.time() * 1000)
        signed_query = self._sign_params(params)

        url = f"{self.base_url}/fapi/v1/order"
        response = self.session.post(
            url,
            data=signed_query,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )

        try:
            data = response.json()
        except Exception:
            data = {"raw_response": response.text}

        response.raise_for_status()
        return data