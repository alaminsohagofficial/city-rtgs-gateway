import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    bank_api_endpoint: str | None = os.getenv("BANK_API_ENDPOINT")
    bank_api_token: str | None = os.getenv("BANK_API_TOKEN")
    ledger_api_url: str | None = os.getenv("LEDGER_API_URL")
    api_token: str | None = os.getenv("API_TOKEN")
    rtgs_fee_bdt: float = float(os.getenv("RTGS_FEE_BDT", "100.0"))
    vat_rate: float = float(os.getenv("VAT_RATE", "0.15"))


config = AppConfig()
