import os
import json
import logging
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

logger = logging.getLogger(__name__)

class SalsabilahAIEngine:
    def __init__(self, api_key: str = None):
        """
        Gemini API কনফিগারেশন এবং ভেরিফাইড বেনিফিশিয়ারি ডাটাবেস ইনিশিয়ালাইজেশন।
        """
        active_api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_api_key:
            raise ValueError("Gemini API key is missing. Set GEMINI_API_KEY environment variable.")
            
        genai.configure(api_key=active_api_key)
        
        # Gemini মডেল সেটআপ with JSON enforcement
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        # অফিশিয়াল সাপ্লাই চেইন রেকর্ড অনুযায়ী ভেরিফাইড অ্যাকাউন্ট ডাটাবেস
        self.verified_beneficiaries = {
            "MINISTER_BANANI_IBBL": {
                "company_name": "Minister Hi-Tech Park Electronics Ltd.",
                "bank_name": "Islami Bank Bangladesh PLC (IBBL)",
                "branch_name": "Banani Branch",
                "routing_number": "125260433",
                "account_number": "20503910100020103"
            }
        }

    def extract_invoice_data(self, invoice_text: str) -> dict:
        """
        Gemini API ব্যবহার করে পেমেন্ট রিকোয়েস্ট বা ইনভয়েস থেকে স্ট্রাকচারড JSON ডেটা এক্সট্র্যাক্ট করে।
        """
        prompt = f"""
        You are an AI financial data extraction agent for Salsabilah Empires & S.R. Electronics Park.
        Extract payment details from the given text/invoice into a strict JSON format with keys:
        - "amount": (float, numeric value only)
        - "beneficiary_key": (string, default to "MINISTER_BANANI_IBBL" if it matches Minister Banani IBBL)
        - "remarks": (string, brief description or purpose of payment)

        Input Text: {invoice_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            extracted_data = json.loads(response.text.strip())
            
            # Basic validation of keys
            if "amount" not in extracted_data or "beneficiary_key" not in extracted_data:
                raise ValueError("Extracted JSON missing required keys.")
                
            return extracted_data
            
        except Exception as e:
            logger.error(f"Failed to extract invoice data via AI: {e}")
            # Safe failure: Raise exception rather than executing a default 5M payment!
            raise RuntimeError(f"Invoice extraction failed: {str(e)}")

    def validate_beneficiary(self, beneficiary_key: str) -> dict | None:
        return self.verified_beneficiaries.get(beneficiary_key)
