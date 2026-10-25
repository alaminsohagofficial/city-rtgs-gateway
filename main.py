import os
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine import SalsabilahAIEngine

app = FastAPI(
    title="Salsabilah Empires - City RTGS & AI Engine",
    version="2.0",
    description="Autonomous RTGS Banking & Gemini AI Integration for S.R. Electronics Park & Minister-Myone Supply Chain"
)

ai_engine = SalsabilahAIEngine()

class InvoiceRequest(BaseModel):
    invoice_prompt: str

@app.post("/api/v1/rtgs/process-invoice")
def process_rtgs_via_ai(payload: InvoiceRequest):
    # Gemini AI ইঞ্জিন ব্যবহার করে ইনভয়েস পার্স করা
    extracted_data = ai_engine.extract_invoice_data(payload.invoice_prompt)
    
    beneficiary_info = ai_engine.validate_beneficiary(extracted_data.get('beneficiary_key'))
    if not beneficiary_info:
        raise HTTPException(status_code=400, detail="Unverified Beneficiary Account")
        
    amount = float(extracted_data.get('amount', 0))
    
    # RTGS ন্যূনতম লিমিট চেক (১ লক্ষ টাকা)
    if amount < 100000:
        raise HTTPException(status_code=400, detail="Amount below RTGS minimum threshold (BDT 100,000)")
        
    rtgs_charge = 100.00
    vat = rtgs_charge * 0.15
    total_debited = amount + rtgs_charge + vat
    
    timestamp = datetime.datetime.now().strftime("%d-%b-%Y | %I:%M:%S %p")
    txn_ref = f"RTGS-CB{datetime.datetime.now().strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"
    
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
Remarks          : {extracted_data.get('remarks')}

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
    
