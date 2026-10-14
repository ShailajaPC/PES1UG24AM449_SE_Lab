
"""Digital wallet demo for Lab 5 static code analysis."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime, timezone

GATEWAY_SECRET = os.environ.get("GATEWAY_SECRET", "")
WALLET_PIN = os.environ.get("WALLET_PIN", "")
wallet = {"balance": 0.0}
settings = {"daily_limit": 1000}
transactions = []


def hash_pin(pin):
    """Return the SHA-256 hash of a PIN."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def add_money(amount, source="UPI", log=None):
    """Add money to the wallet and record the credit."""
    if amount <= 0:
        return False

    if log is None:
        log = []

    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now(timezone.utc).isoformat(),
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Update the wallet's daily payment limit."""
    if new_limit < 0:
        raise ValueError("Daily limit cannot be negative")
    settings["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Validate a PIN and process a merchant payment."""
    if not WALLET_PIN or not hmac.compare_digest(
        hash_pin(pin), hash_pin(WALLET_PIN)
    ):
        print("Wrong PIN for payment to", merchant)
        return False

    if amount <= 0:
        return False

    if amount > wallet["balance"] or amount > settings["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now(timezone.utc).isoformat(),
    })
    return True


def mini_statement(count=3):
    """Print the most recent wallet transactions."""
    if count <= 0:
        return

    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type):
    """Calculate cashback using the merchant category."""
    if amount <= 0:
        return 0.0

    rate = 0.02 if merchant_type.lower() == "health" else 0.01
    return round(amount * rate, 2)


def check_gateway(secret):
    """Check a supplied secret against the configured gateway secret."""
    return bool(GATEWAY_SECRET) and hmac.compare_digest(
        secret, GATEWAY_SECRET
    )


def receipt_path():
    """Create a temporary file safely for a receipt."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf", prefix="wallet_receipt_", delete=False
    ) as receipt:
        return receipt.name


def main():
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("Demo OTP:", otp)

    if not WALLET_PIN:
        print("Set the WALLET_PIN environment variable to enable payments.")

    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)

    if WALLET_PIN:
        pay_merchant("Coffee Corner", 180, WALLET_PIN)
        pay_merchant("Book Store", 5000, WALLET_PIN)
        pay_merchant("Grocery Mart", 350, "0000")
        pay_merchant("Pharmacy", 420, WALLET_PIN)

    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])

    credit_amounts = [
        entry["amount"]
        for entry in transactions
        if entry["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
