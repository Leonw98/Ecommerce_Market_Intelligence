# 📋 Handover State: Ecommerce Market Intelligence Engine

**Project Status:** Active Crawl / Mass Data Acquisition Phase
**Last Update:** March 1, 2026

## 🛠️ Technical Configuration
- **Core Engine:** Playwright (Python) + BeautifulSoup4
- **AI Integration:** Local Llama 3.1 via Ollama (Running on `localhost:11434`)
- **Target Marketplace:** Amazon UK (Broad Wearables)
- **Checkpointing:** Incremental JSON saves at `data/market_research_checkpoint.json`

## 📊 Data Schema
Each record captures:
- `asin`: Amazon Standard Identification Number
- `product_name`: Full descriptive title
- `brand`: AI-extracted brand name
- `category`: AI-identified category (Ring, Watch, Strap, etc.)
- `price`: Cleaned GBP price
- `rating`: Numerical score (e.g. 4.4)
- `total_reviews`: Customer feedback volume
- `badge`: Presence of "Best Seller" or "Amazon Choice"
- `is_prime`: Prime delivery availability
- `url`: Direct canonical product link

## 🚀 State for Next AI (Claude/Other)
1. **Resume Capability:** The engine is stateless between keywords. If it crashes, simply re-run `market_intelligence_engine.py`. It uses the `seen_urls` set from the JSON checkpoint to avoid duplicates.
2. **Expansion Points:**
   - **Proxy Rotation:** Currently uses a single IP. For >2,000 records, Claude should implement the `NetworkManager` logic (found in other project folders) to handle 403 blocks.
   - **Deep Extraction:** The engine currently scrapes search results. Claude can be tasked to visit each `url` individually for full feature lists, manufacturer specs, and customer review sentiment.
   - **Analytics:** The raw data is ready for a Pandas-based trend analysis (e.g., "Average price per category" or "Highest rated brands with >500 reviews").

## 📂 Current Progress
- **Checkpoint File:** `C:\src\Freelance\Portfolio_Repos\Ecommerce_Market_Intelligence\data\market_research_checkpoint.json`
- **Output Folder:** `C:\src\Freelance\Portfolio_Repos\Ecommerce_Market_Intelligenceeports/`
