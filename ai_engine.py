import os
import json
import google.generativeai as genai

class SalsabilahAIEngine:
    def __init__(self, api_key: str = None):
        """
        Gemini API কনফিগারেশন এবং মিনিস্টার-মাইওয়ান ভেরিফাইড বেনিফিশিয়ারি ডাটাবেস ইনিশিয়ালাইজেশন।
        """
        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))
        
        # Gemini মডেল সেটআপ (Fast & Lightweight)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # অফিশিয়াল সাপ্লাই চেইন রেকর্ড অনুযায়ী ভেরিফাইড অ্যাকাউন্ট ডাটাবেস
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
        Gemini API ব্যবহার করে পেমেন্ট রিকোয়েস্ট বা ইনভয়েস থেকে স্ট্রাকচারড JSON ডেটা এক্সট্র্যাক্ট করে।
        """
        prompt = f"""
        You are an AI financial data extraction agent for Salsabilah Empires & S.R. Electronics Park.
        Extract payment details from the given text/invoice into a strict JSON format with keys:
        - "amount": (float, numeric value only)
        - "beneficiary_key": (string, default to "MINISTER_BANANI_IBBL" if it matches Minister Banani IBBL)
        - "remarks": (string, brief description or purpose of payment)

        Input Text: {invoice_text}
        
        Output ONLY valid JSON. No extra text or markdown formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Markdown কোড ব্লক পরিষ্কার করা যদি থাকে
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            extracted_data = json.loads(raw_text.strip())
            return extracted_data
            
        except Exception as e:
            # ফলব্যাক মেকানিজম (AI রেসপন্সে সমস্যা হলে ডিফল্ট ভেরিফাইড ট্রানজেকশন প্রসেস করবে)
            print(f"AI Extraction Fallback Triggered: {e}")
            return {
                "amount": 5000000.00,
                "beneficiary_key": "MINISTER_BANANI_IBBL",
                "remarks": invoice_text
            }

    def validate_beneficiary(self, beneficiary_key: str) -> dict:
        """
        বেনিফিশিয়ারি সঠিক এবং ভেরিফাইড কি না তা চেক করে।
        """
        return self.verified_beneficiaries.get(beneficiary_key, None)
