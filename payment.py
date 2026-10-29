import requests
from config import Config

class RTGSPaymentProcessor:
    def __init__(self):
        self.api_url = Config.CITY_BANK_API_URL
        self.api_key = Config.BANK_API_KEY
        self.api_secret = Config.BANK_API_SECRET

    def process_payment(self, transaction_data: dict) -> dict:
        amount = transaction_data.get("amount", 0.0)
        account_number = transaction_data.get("account_number")
        routing_number = transaction_data.get("routing_number")

        total_charge = Config.calculate_total_charge(amount)
        grand_total = amount + total_charge

        payload = {
            "account_number": account_number,
            "routing_number": routing_number,
            "principal_amount": amount,
            "rtgs_charge": total_charge,
            "total_debited": grand_total,
            "currency": "BDT"
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(f"{self.api_url}/transfer", json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "টাকা সফলভাবে পরিশোধ করা হয়েছে।",
                    "gateway_response": response.json()
                }
            else:
                return {
                    "status": "failed",
                    "message": "ব্যাংক গেটওয়ে পেমেন্ট প্রত্যাখ্যান করেছে।",
                    "error": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": "নেটওয়ার্ক বা সার্ভার ত্রুটি ঘটেছে।",
                "details": str(e)
            }
