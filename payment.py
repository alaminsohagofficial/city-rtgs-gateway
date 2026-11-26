from typing import Any
import requests
from config import config


def calculate_rtgs_settlement(amount: float) -> dict[str, float]:
    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    rtgs_charge = round(config.rtgs_fee_bdt, 2)
    vat_amount = round(rtgs_charge * config.vat_rate, 2)
    total_charge = round(rtgs_charge + vat_amount, 2)
    net_settlement = round(amount - total_charge, 2)

    return {
        "gross_amount": round(amount, 2),
        "rtgs_charge": rtgs_charge,
        "vat_amount": vat_amount,
        "total_charges": total_charge,
        "net_settlement": net_settlement,
    }


def validate_rtgs_details(routing_number: str, account_number: str) -> bool:
    clean_routing = (routing_number or "").strip()
    clean_account = (account_number or "").strip()
    return len(clean_routing) == 9 and clean_routing.isdigit() and len(clean_account) >= 6


def dispatch_rtgs_payment(payload: dict[str, Any]) -> dict[str, Any]:
    if not config.bank_api_endpoint or not config.bank_api_token:
        return {
            "status": "SKIPPED_NO_BANK_CREDENTIALS",
            "payload": payload,
        }

    url = f"{config.bank_api_endpoint.rstrip('/')}/v1/rtgs/payments"
    headers = {
        "Authorization": f"Bearer {config.bank_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json() if response.text else {"status": "SUBMITTED"}
