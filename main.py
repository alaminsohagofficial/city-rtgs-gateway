import json
import sys
from ai_engine import extract_and_audit_invoice
from payment import calculate_rtgs_settlement, dispatch_rtgs_payment, validate_rtgs_details


def run_rtgs_pipeline() -> None:
    sample_invoice = {
        "reference_id": "INV-RTGS-001",
        "beneficiary_name": "S.R. Electronics Park",
        "routing_number": "080270011",
        "account_number": "1234567890",
        "amount": 250000.00,
        "currency": "BDT",
    }

    try:
        audit_result = extract_and_audit_invoice(sample_invoice)
        routing_ok = validate_rtgs_details(
            str(audit_result.get("routing_number", sample_invoice["routing_number"])),
            str(audit_result.get("account_number", sample_invoice["account_number"])),
        )
        if not routing_ok:
            raise ValueError("Invalid RTGS routing or account number.")

        settlement = calculate_rtgs_settlement(float(sample_invoice["amount"]))
        final_payload = {
            "audit": audit_result,
            "settlement": settlement,
        }
        dispatch_result = dispatch_rtgs_payment(final_payload)

        output = {
            "status": "COMPLETED",
            "settlement": settlement,
            "dispatch": dispatch_result,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except Exception as exc:
        print(f"RTGS Pipeline Failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_rtgs_pipeline()
