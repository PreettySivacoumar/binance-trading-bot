import argparse
import sys
import requests

from bot.client import BinanceRESTClient
from bot.logging_config import setup_logging
from bot.orders import OrderService
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot using direct REST API"
    )
    parser.add_argument("--symbol", required=True, help="Example: BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order_type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, help="Required for LIMIT orders")
    return parser


def print_summary(symbol, side, order_type, quantity, price):
    print("\n=== ORDER REQUEST SUMMARY ===")
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Order Type : {order_type}")
    print(f"Quantity   : {quantity}")
    print(f"Price      : {price if price is not None else 'N/A'}")


def print_response(response):
    print("\n=== ORDER RESPONSE ===")
    print(f"Order ID       : {response.get('orderId')}")
    print(f"Status         : {response.get('status')}")
    print(f"Executed Qty   : {response.get('executedQty')}")
    print(f"Avg Price      : {response.get('avgPrice', 'N/A')}")
    print(f"Client Order ID: {response.get('clientOrderId', 'N/A')}")


def main():
    logger = setup_logging()

    try:
        parser = build_parser()
        args = parser.parse_args()

        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(order_type, args.price)

        print_summary(symbol, side, order_type, quantity, price)

        client = BinanceRESTClient()
        client.ping()

        service = OrderService(client, logger)
        response = service.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        print_response(response)
        print("\nSUCCESS: Order placed successfully.")

    except ValueError as exc:
        logger.error(f"Validation error: {exc}")
        print(f"\nERROR: Validation error: {exc}")
        sys.exit(1)

    except requests.HTTPError as exc:
        logger.exception("HTTP/API error")
        detail = ""
        try:
            detail = exc.response.text
        except Exception:
            detail = str(exc)
        print(f"\nERROR: API error: {detail}")
        sys.exit(1)

    except requests.RequestException as exc:
        logger.exception("Network error")
        print(f"\nERROR: Network error: {exc}")
        sys.exit(1)

    except Exception as exc:
        logger.exception("Unexpected application error")
        print(f"\nERROR: Unexpected error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()