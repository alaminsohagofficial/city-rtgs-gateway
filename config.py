import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CITY_BANK_API_URL = os.getenv("CITY_BANK_API_URL")
    BANK_API_KEY = os.getenv("BANK_API_KEY")
    BANK_API_SECRET = os.getenv("BANK_API_SECRET")
    RTGS_FEE = float(os.getenv("RTGS_FEE", 100))
    VAT_RATE = float(os.getenv("VAT_PERCENTAGE", 15)) / 100

    @staticmethod
    def calculate_total_charge(amount: float) -> float:
        vat = Config.RTGS_FEE * Config.VAT_RATE
        return Config.RTGS_FEE + vat
