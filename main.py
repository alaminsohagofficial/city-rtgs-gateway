from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from payment import RTGSPaymentProcessor

app = FastAPI(title="City RTGS & Payment Gateway")
payment_processor = RTGSPaymentProcessor()

class PaymentRequest(BaseModel):
    account_number: str
    routing_number: str
    amount: float

@app.post("/api/v1/pay")
def make_rtgs_payment(req: PaymentRequest):
    result = payment_processor.process_payment(req.dict())
    if result["status"] != "success":
        raise HTTPException(status_code=400, detail=result)
    return result
