# ⌚ Ecommerce Market Intelligence & Pricing Engine
> **High-Volume extraction & AI-driven market analysis at scale.**

```text
      _..._
    .'     '.
   /  _   _  \      [ MARKET INTELLIGENCE ENGINE ]
   | (o) (o) |      Status: 2,240 Records Extracted
   |    _    |      Engine: Playwright + Llama 3.1
    \  '='  /       Target: Wearable Tech (Amazon UK/US)
     '-----'
```

## 🧱 The Challenge
E-commerce research at scale (1,000+ records) faces two main hurdles: **Anti-Bot Blocking** and **Data Decay**. Manual research is impossible, and standard scrapers fail when a 4-hour job is interrupted without state management.

## 🚀 The Solution: "Scale & Resiliency" Architecture
This engine was developed as a high-performance prototype for deep-market analysis:
1.  **Stateful Checkpointing:** Utilizes a JSON-based state manager to allow 1,000+ record research runs to resume instantly if interrupted.
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

## 📊 High-Volume Output (2,000+ Records)
The engine produces a full competitive landscape with 0% manual entry:

| Product Name | Brand (AI) | Price | Review Score | Feature Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Oura Ring 4** | Oura | £349 | 4.8 | Sleep / Wellness |
| **Ultrahuman Air** | Ultrahuman | £329 | 4.4 | Metabolism / Recovery |
| **Circular Ring Slim** | Circular | £259 | 4.1 | Vitals / Vibration |

## 📦 Repository Structure
- `market_intelligence_engine.py`: The core crawler with checkpointing.
- `Smart_Wearables_Market_Intelligence.xlsx`: The "Golden Record" dataset (200+ unique products).

---
*Technical Case Study: High-Volume Data Acquisition & AI Normalization.*
