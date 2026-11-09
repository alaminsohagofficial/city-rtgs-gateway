import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CITY_BANK_API_URL: str = os.getenv("CITY_BANK_API_URL", "https://api.citybankplc.com/rtgs/v1")
    BANK_API_KEY: str = os.getenv("BANK_API_KEY", "")
    BANK_API_SECRET: str = os.getenv("BANK_API_SECRET", "")
    VAT_PERCENTAGE: float = float(os.getenv("VAT_PERCENTAGE", 15.0))
    RTGS_FEE: float = float(os.getenv("RTGS_FEE", 100.0))

settings = Settings()
