import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from config import settings

app = FastAPI(title="City RTGS & Payment Gateway", version="1.0.0")

class PaymentRequest(BaseModel):
    account_number: str = Field(..., min_length=1, description="Recipient bank account number")
    routing_number: str = Field(..., min_length=1, description="Bank routing number")
    amount: float = Field(..., gt=0, description="Principal payment amount, must be greater than 0")

class PaymentResponse(BaseModel):
    status: str
    transaction_id: str | None = None
    total_debited: float | None = None
    message: str | None = None

class RTGSPaymentProcessor:
    def __init__(self):
        self.base_url = settings.CITY_BANK_API_URL
        self.api_key = settings.BANK_API_KEY
        self.api_secret = settings.BANK_API_SECRET
        self.vat_rate = settings.VAT_PERCENTAGE
        self.rtgs_fee = settings.RTGS_FEE

    def calculate_charges(self, base_amount: float) -> dict:
        vat_amount = (self.rtgs_fee * self.vat_rate) / 100
        total_fee = self.rtgs_fee + vat_amount
        return {
            "principal": base_amount,
            "rtgs_fee": self.rtgs_fee,
            "vat": vat_amount,
            "total_debited": base_amount + total_fee
        }

    def process_payment(self, payload: dict) -> dict:
        # Calculate breakdown including structural fees & VAT
        breakdown = self.calculate_charges(payload["amount"])
        
        # Integration logic with City Bank RTGS API would go here (e.g., using httpx)
        # Mocking a successful gateway response structure:
        return {
            "status": "success",
            "transaction_id": "RTGS-CITY-2026-981234",
            "total_debited": breakdown["total_debited"],
            "message": "Payment processed successfully via RTGS"
        }

payment_processor = RTGSPaymentProcessor()

@app.post("/api/v1/pay", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
def make_rtgs_payment(req: PaymentRequest):
    try:
        # Pass validated model dump data to processor
        result = payment_processor.process_payment(req.model_dump())
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=result.get("message", "Payment processing failed")
            )
            
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
