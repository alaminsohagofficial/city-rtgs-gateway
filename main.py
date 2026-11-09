from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from payment import RTGSPaymentProcessor

app = FastAPI(title="City RTGS & Payment Gateway", version="1.0.0")
payment_processor = RTGSPaymentProcessor()

class PaymentRequest(BaseModel):
    account_number: str = Field(..., min_length=1, description="Recipient bank account number")
    routing_number: str = Field(..., min_length=1, description="Bank routing number")
    amount: float = Field(..., gt=0, description="Payment amount, must be greater than 0")

class PaymentResponse(BaseModel):
    status: str
    transaction_id: str | None = None
    message: str | None = None

@app.post("/api/v1/pay", response_model=PaymentResponse, status_code=200)
def make_rtgs_payment(req: PaymentRequest):
    # Use model_dump() for Pydantic v2
    result = payment_processor.process_payment(req.model_dump())
    
    if result.get("status") != "success":
        raise HTTPException(
            status_code=400, 
            detail=result.get("message", "Payment processing failed")
        )
        
    return result
