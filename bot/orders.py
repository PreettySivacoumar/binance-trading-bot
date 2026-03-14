from typing import Any, Dict


class OrderService:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
    ) -> Dict[str, Any]:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        self.logger.info(f"Order request: {params}")

        try:
            response = self.client.create_order(params)
            self.logger.info(f"Order response: {response}")
            return response
        except Exception as exc:
            self.logger.exception(f"Order placement failed: {exc}")
            raise