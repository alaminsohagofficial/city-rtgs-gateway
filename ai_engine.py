import json
from typing import Any
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import config


def extract_and_audit_invoice(invoice_data: dict[str, Any]) -> dict[str, Any]:
    if not config.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=config.gemini_api_key)
    prompt = f"""
You are the AI financial auditor for Salsabilah City RTGS & AI Engine
(Salsabilah Empires & S.R. Electronics Park).
Analyze the following invoice/payment payload and return a structured JSON object
with keys: reference_id, beneficiary_name, routing_number, account_number,
base_amount, is_valid, and audit_notes.

Input data:
{json.dumps(invoice_data, indent=2, ensure_ascii=False)}
"""

    try:
        response = client.models.generate_content(
            model=config.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        if not response.text:
            raise RuntimeError("Empty response from Gemini API.")
        return json.loads(response.text)
    except APIError as exc:
        raise RuntimeError(f"Gemini API error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from Gemini API: {exc}") from exc
