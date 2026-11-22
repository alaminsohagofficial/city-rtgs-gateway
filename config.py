import os
from dataclasses import dataclass


def _parse_vat_rate(raw_vat: str | None) -> float:
    if not raw_vat:
        return 0.15
    value = float(raw_vat.strip())
    # 15 -> 0.15, আর ইতিমধ্যে 0.15 দেওয়া থাকলে সেটিই রাখে
    return value / 100.0 if value > 1.0 else value


@dataclass(frozen=True)
class AppConfig:
    city_bank_api_url: str | None = os.getenv("CITY_BANK_API_URL")
    bank_api_key: str | None = os.getenv("BANK_API_KEY")
    bank_api_secret: str | None = os.getenv("BANK_API_SECRET")
    vat_rate: float = _parse_vat_rate(os.getenv("VAT_PERCENTAGE"))
    rtgs_fee_bdt: float = float(os.getenv("RTGS_FEE", "100"))
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


config = AppConfig()
