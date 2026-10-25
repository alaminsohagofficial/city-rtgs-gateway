# 🏦 Salsabilah City RTGS & AI Engine

An enterprise-grade, autonomous RTGS (Real-Time Gross Settlement) banking and Gemini AI integration backend built for **Salsabilah Empires** and **S.R. Electronics Park** to automate B2B transactions and supply chain settlements (specifically for **Minister-Myone Group**).

---

## 🚀 Key Features

* **AI-First Invoice Processing:** Uses **Google Gemini API** to automatically extract and parse payment amounts, beneficiary details, and remarks from unstructured invoices or text.
* **Automated RTGS Integration:** Connects with **City Bank PLC** and Bangladesh Bank RTGS switch architecture for instant high-value fund transfers.
* **Built-in Financial Logic:** Automatically calculates standard RTGS charges (BDT 100) and 15% VAT.
* **Risk & Verification Guardrails:** Validates beneficiary routing numbers and account details against official records (e.g., Minister Banani IBBL Branch, Routing: `125260433`) before processing.
* **Digital Receipt Generation:** Generates automated, timestamped electronic transaction receipts for digital reconciliation.

---

## 📂 Project Structure

```text
city-rtgs-gateway/
├── main.py             # FastAPI backend & RTGS API endpoints
├── ai_engine.py        # Gemini AI invoice extraction & verification logic
├── requirements.txt    # Python dependencies list
└── README.md           # Project documentation
