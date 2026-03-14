from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string.")
    return symbol.strip().upper()


def validate_side(side: str) -> str:
    value = side.strip().upper()
    if value not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL.")
    return value


def validate_order_type(order_type: str) -> str:
    value = order_type.strip().upper()
    if value not in VALID_ORDER_TYPES:
        raise ValueError("Order type must be MARKET or LIMIT.")
    return value


def validate_quantity(quantity) -> float:
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a valid number.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity


def validate_price(order_type: str, price: Optional[float]) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid number.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        return price
    return None