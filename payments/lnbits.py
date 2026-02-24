import requests
from django.conf import settings

BASE_URL = settings.LNBITS_URL.rstrip("/")

def get_headers(invoice_key: bool = True):
    api_key = settings.LNBITS_INVOICE_KEY if invoice_key else settings.LNBITS_ADMIN_KEY
    return {
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }

def get_wallet_details():
    url = f"{BASE_URL}/api/v1/wallet"
    r = requests.get(url, headers=get_headers(invoice_key=True), timeout=10)
    r.raise_for_status()
    return r.json()

def create_invoice(amount_sats: int, memo: str = ""):
    """
    Crée une invoice entrante (out=False) via LNbits.
    """
    url = f"{BASE_URL}/api/v1/payments"
    payload = {
        "out": False,
        "amount": amount_sats,
        "memo": memo or "POS Django",
    }
    r = requests.post(url, json=payload, headers=get_headers(invoice_key=True), timeout=15)
    r.raise_for_status()
    data = r.json()
    return {
        "payment_hash": data["payment_hash"],
        "payment_request": data["payment_request"],  # BOLT11
        "checking_id": data.get("checking_id", data["payment_hash"]),
    }

def check_invoice(payment_hash: str):
    """
    Vérifie si l’invoice est payée.
    """
    url = f"{BASE_URL}/api/v1/payments/{payment_hash}"
    r = requests.get(url, headers=get_headers(invoice_key=True), timeout=10)
    r.raise_for_status()
    return r.json()
