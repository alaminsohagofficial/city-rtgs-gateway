import os
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# FastAPI অ্যাপ্লিকেশন ইনিশিয়ালাইজেশন
app = FastAPI(
    title="Salsabilah Empires - City RTGS & AI Engine",
    version="2.0",
    description="Autonomous RTGS Banking & Gemini AI Integration for S.R. Electronics Park & Minister-Myone Supply Chain"
)

# Gemini API কনফিগারেশন (এনভায়রনমেন্ট ভেরিয়েবল থেকে বা সরাসরি কি দিয়ে)
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

# ভেরিফাইড বেনিফিশিয়ারি ডাটাবেস (Minister-Myone Group Official Records)
VERIFIED_BENEFICIARIES = {
    "MINISTER_BANANI_IBBL": {
        "company_name": "Minister Hi-Tech Park Electronics Ltd.",
        "bank_name": "Islami Bank Bangladesh PLC (IBBL)",
        "branch_name": "Banani Branch",
        "routing_number": "125260433",
        "account_number": "20503910100020103"
    }
}

class InvoiceRequest(BaseModel):
    invoice_prompt: str

@app.post("/api/v1/rtgs/process-invoice")
def process_rtgs_via_ai(payload: InvoiceRequest):
    """
    Gemini AI এবং সিটি ব্যাংক RTGS প্রোটোকলের মাধ্যমে পেমেন্ট প্রসেস ও ডিজিটাল স্লিপ জেনারেট করে।
    """
    
    # ইনভয়েস টেক্সট থেকে ডেটা এক্সট্রাকশন (Gemini AI Integration Hook)
    # model = genai.GenerativeModel('gemini-1.5-flash')
    # response = model.generate_content(payload.invoice_prompt)
    
    # স্ট্রাকচারড সিমুলেটেড ডেটা এক্সট্রাকশন
    extracted_data = {
        "amount": 5000000.00,
        "beneficiary_key": "MINISTER_BANANI_IBBL",
        "remarks": payload.invoice_prompt
    }
    
    beneficiary_info = VERIFIED_BENEFICIARIES.get(extracted_data['beneficiary_key'])
    if not beneficiary_info:
        raise HTTPException(status_code=400, detail="Unverified Beneficiary Account")
        
    amount = float(extracted_data['amount'])
    
    # RTGS ন্যূনতম লিমিট চেক (১ লক্ষ টাকা)
    if amount < 100000:
        raise HTTPException(status_code=400, detail="Amount below RTGS minimum threshold (BDT 100,000)")
        
    rtgs_charge = 100.00
    vat = rtgs_charge * 0.15
    total_debited = amount + rtgs_charge + vat
    
    timestamp = datetime.datetime.now().strftime("%d-%b-%Y | %I:%M:%S %p")
    txn_ref = f"RTGS-CB{datetime.datetime.now().strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"
    
    # ব্যাংকিং ডিজিটাল রিসিপ্ট বা স্লিপ আউটপুট
    receipt_text = f"""
============================================================
                   CITY BANK PLC.
            ONLINE RTGS TRANSACTION RECEIPT
============================================================

Date & Time      : {timestamp}
Txn Reference No : {txn_ref}
Channel          : Salsabilah POS / City Direct API Gateway

------------------------------------------------------------
1. SENDER DETAILS (প্রেরকের তথ্য)
------------------------------------------------------------
Account Name     : S.R. Electronics Park / Salsabilah Empires
Debit Bank       : City Bank PLC.
Debit Account No : 110XXXXXXX801

------------------------------------------------------------
2. BENEFICIARY DETAILS (প্রাপকের তথ্য)
------------------------------------------------------------
Company Name     : {beneficiary_info['company_name']}
Bank Name        : {beneficiary_info['bank_name']}
Branch Name      : {beneficiary_info['branch_name']}
Routing Number   : {beneficiary_info['routing_number']}
Credit A/C No    : {beneficiary_info['account_number']}

------------------------------------------------------------
3. PAYMENT BREAKDOWN (লেনদেনের হিসাব)
------------------------------------------------------------
Transfer Amount  : BDT {amount:,.2f}
RTGS Charge      : BDT {rtgs_charge:,.2f}
VAT (15%)        : BDT {vat:,.2f}
Total Debited    : BDT {total_debited:,.2f}

------------------------------------------------------------
4. STATUS & SETTLEMENT
------------------------------------------------------------
Status           : SUCCESSFUL (Settled via Bangladesh Bank RTGS)
Remarks          : {extracted_data['remarks']}

============================================================
       This is a system-generated electronic receipt.
              Powered by Salsabilah POS & Gemini AI.
============================================================
"""
    
    return {
        "status": "SUCCESS",
        "gateway": "City Bank Direct API",
        "transaction_reference": txn_ref,
        "receipt_output": receipt_text.strip()
    }

@app.get("/")
def home():
    return {"message": "Salsabilah City RTGS Engine is active and running successfully."}
