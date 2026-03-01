# Ecommerce Market Intelligence & Pricing Engine

A high-volume extraction engine designed for Amazon-scale market research and competitor price tracking.

## 🧱 The Problem
E-commerce sites like Amazon use dynamic layouts and aggressive anti-bot protections. High-volume research (1,000+ records) requires robust error handling, proxy rotation, and data normalization.

## 🚀 The Solution
This engine utilizes a **High-Volume Crawl** lifecycle to extract structured data from 2,500+ products:
1.  **Dynamic Selectors:** Custom CSS/XPath logic to handle Amazon's ever-changing DOM structure.
2.  **Checkpointing:** Built-in state management allows the engine to resume 1,000+ record jobs instantly if interrupted.
3.  **Data Normalization:** Automated cleaning of pricing, review counts, and manufacturer metadata for direct Excel export.

## 📊 High-Volume Output (2,000+ Records)
The engine generates a full competitive landscape, including AI-driven brand categorization:

| Product Name | Brand (AI Identified) | Price | Review Score | Feature Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Oura Ring 4** | Oura | £349 | 4.8 | Sleep / Wellness |
| **Ultrahuman Air** | Ultrahuman | £329 | 4.4 | Metabolism / Recovery |
| **Circular Ring Slim** | Circular | £259 | 4.1 | Vitals / Vibration |

## 🛠️ Tech Stack
- **Automation:** Playwright / Scrapy (Python)
- **Data Ops:** JSON Checkpointing, Pandas (Clean/Merge)
- **Performance:** Optimized for unattended high-volume research.

## 📦 Key Deliverables
- **`market_researcher.py`**: High-volume crawler with checkpointing and error handling.
- **`samples/Smart_Wearables_Market_Intelligence.xlsx`**: A full market report of 2,000+ wearable products (Oura, Ultrahuman, Samsung, etc.).

---
*Developed for e-commerce trend analysis and competitive pricing.*
