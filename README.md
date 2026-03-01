# ⌚ Ecommerce Market Intelligence & Pricing Engine
> **High-Volume extraction & AI-driven market analysis at scale.**

```text
      _..._
    .'     '.
   /  _   _  \      [ MARKET INTELLIGENCE ENGINE ]
   | (o) (o) |      Status: 200+ Records Extracted
   |    _    |      Engine: Playwright + Llama 3.1
    \  '='  /       Target: Wearable Tech (Amazon UK/US)
     '-----'
```

## 🧱 The Challenge
E-commerce research at scale faces two main hurdles: **Anti-Bot Blocking** and **Data Decay**. Manual research is impossible, and standard scrapers fail when a 4-hour job is interrupted without state management.

## 🚀 The Solution: "Scale & Resiliency" Architecture
This engine was developed as a high-performance prototype for deep-market analysis:
1.  **Stateful Checkpointing:** Utilizes a JSON-based state manager to allow research runs to resume instantly if interrupted.
2.  **AI Metadata Normalization:** Integrated local **Llama 3.1** via Ollama to transform messy product titles into clean "Brand" and "Feature" columns.
3.  **Dynamic Human Mimicry:** Uses Playwright with randomized scroll-depths and interaction delays to bypass basic bot detection.

## 💻 High-Signal Logic: AI Enrichment
This snippet demonstrates how the engine uses LLMs to "clean" the data during the crawl:

```python
def enrich_data_ai(title):
    """
    Normalizes product metadata using Local Llama 3.1.
    Transforms: 'Oura Ring Gen3 Horizon - Silver - Size 10 - Smart Ring'
    To: {'brand': 'Oura', 'feature': 'Sleep/Recovery'}
    """
    prompt = f"Extract 'brand' and 'key_feature' from: '{title}'. Return JSON."
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.1",
        "messages": [{"role": "user", "content": prompt}],
        "format": "json"
    })
    return response.json()
```

## 📊 High-Volume Output (200+ Records)
The engine generates a full competitive landscape with 0% manual entry. Below is a live sample of the first 20 records:

| product_name | manufacturer | price | average_review | feature |
|---|---|---|---|---|
| Smart Ring Charging Size 9 | Smart Ring | £39 | 4.1 / 5 | Wearable |
| Oura Ring 4 Sizing Kit | Oura | £5 | 4.4 / 5 | Sizing Tool |
| Oura Ring 4 Charging Case | Oura | £99 | 4.3 / 5 | Wearable |
| Oura Ring 4 Charging Case | Oura | £99 | 4.3 / 5 | Wearable |
| Oura Ring Gen3 Sizing Kit | Oura | £10 | 4.3 / 5 | Wearable |
| 12 Pack Rings Cover | Oura | £12 | 4.2 / 5 | Wearable |
| Oura Ring 4 Charger - Size 8 | Oura | £59 | 4.7 / 5 | Wearable |
| Oura Ring 4 Charging Case | Oura | £99 | 4.3 / 5 | Wearable |
| Oura Ring 4 Charger - Size 9 | Oura | £59 | 4.7 / 5 | Wearable |
| Ring Covers for Oura 4 | Oura | £4 | 5.0 / 5 | Wearable |
| Oura Ring 4 Charger - Size 10 | Oura | £59 | 4.7 / 5 | Charging Dock |
| Oura Gen3 Heritage Ring | Oura | £192 | 4.2 / 5 | Sleep/Health Wearable |
| Cover for Oura Ring Gen 4 | Ultrahuman | £11 | 3.8 / 5 | Anti-Scratch TPU |
| Ring Protector for Oura 4 | Oura | £16 | 2.2 / 5 | Scratch-Resistant |
| Smart Ring Sizing Kit | Oura | £6 | 4.8 / 5 | Wearable |
| 4PC Silicone Ring Cover | Oura | £8 | 4.3 / 5 | Wearable |
| 5PCS Silicone Rings Cover | Oura | £5 | 4.6 / 5 | Wearable |
| 2 Pcs Ring Protector Gym | Oura | £4 | 4.6 / 5 | Silicone Case |
| Silicone Ring Protector | Oura | £3 | 4.1 / 5 | Wearable |
| Smart Ring Charger - Size 8 | Oura | £39 | 4.0 / 5 | Wearable |

## 📦 Repository Structure
- `market_intelligence_engine.py`: The core crawler with checkpointing.
- `Smart_Wearables_Market_Intelligence.xlsx`: The "Golden Record" dataset (200+ unique products).

---
*Technical Case Study: High-Volume Data Acquisition & AI Normalization.*

## 📜 License & Technical Disclaimer
**© 2026 Leon Wilkinson. All Rights Reserved.**

This repository is a **redacted technical case study** designed to demonstrate architectural patterns and engineering strategy. 

*   **Proprietary Logic:** The full, production-grade version of this engine contains proprietary logic for residential proxy rotation, anti-fingerprinting, and advanced data validation which has been removed for security and IP protection.
*   **Usage:** Unauthorized copying, redistribution, or commercial use of this redacted source code is strictly prohibited. 
*   **Purpose:** This project serves as a portfolio piece to showcase expertise in Python, Playwright, and LLM-driven data enrichment.
