# market_intelligence_engine.py
import os
import json
import time
import random
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import requests

# CONFIG: High-value keywords for market research
KEYWORDS = [
    "smart health ring", "sleep tracker ring", "heart rate monitor ring", 
    "circular ring health", "wearable fitness tracker"
]
CHECKPOINT_FILE = "data/market_research_checkpoint.json"

def load_checkpoint():
    """Loads progress from a JSON checkpoint to allow for persistent research runs."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_checkpoint(data):
    """Saves research progress incrementally."""
    os.makedirs("data", exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def enrich_data_ai(title):
    """
    Uses a Large Language Model (local or cloud) to normalize product 
    metadata and extract brand/feature signals from messy titles.
    """
    try:
        # Example using local Ollama (Llama 3.1)
        prompt = f"Extract 'brand' and 'key_feature' from this product title: '{title}'. Return JSON."
        payload = {
            "model": "llama3.1",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": "json"
        }
        # In a portfolio environment, this would be a modular AI client call.
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=5)
        if response.status_code == 200:
            return json.loads(response.json()['message']['content'])
    except:
        pass
    return {"brand": title.split(' ')[0], "feature": "Wearable"}

def scrape_market_segment(kw):
    """
    Automated browser instance for deep market segment extraction.
    Utilizes Playwright for dynamic content loading and anti-bot navigation.
    """
    print(f"[*] Starting research for segment: {kw}")
    seen_urls = {r["url"] for r in load_checkpoint()}
    
    with sync_playwright() as p:
        # Note: In production, this would use rotating residential proxies.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        # Optimize performance by blocking non-essential assets
        page.route("**/*.{png,jpg,jpeg,css}", lambda route: route.abort())

        for page_num in range(1, 10):
            url = f"https://www.amazon.co.uk/s?k={kw.replace(' ', '+')}&page={page_num}"
            print(f"  [>] Processing page {page_num}...")
            
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                
                # Verify content loading (detect blocks/captchas)
                if "Robot" in page.title():
                    print("  [!] Anti-bot block detected. Rotating strategy...")
                    break

                page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=15000)
                
                # Human-mimicry: dynamic scroll to trigger lazy-loaded elements
                page.evaluate("window.scrollBy(0, 1000)")
                time.sleep(random.uniform(1, 3))
                
                soup = BeautifulSoup(page.content(), 'html.parser')
                items = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                batch_results = []
                for item in items:
                    try:
                        link_tag = item.find('a', {'class': 'a-link-normal'}, href=True)
                        if not link_tag: continue
                        
                        prod_url = "https://www.amazon.co.uk" + link_tag['href'].split('?')[0]
                        if prod_url in seen_urls: continue
                        
                        name = item.find('h2').get_text(strip=True)
                        price_tag = item.find('span', {'class': 'a-price-whole'})
                        rating_tag = item.find('span', {'class': 'a-icon-alt'})
                        
                        # AI Enrichment for clean metadata
                        ai_data = enrich_data_ai(name)
                        
                        data = {
                            "product_name": name,
                            "manufacturer": ai_data.get('brand', 'Unknown'),
                            "price": f"£{price_tag.text.strip()}" if price_tag else "N/A",
                            "average_review": rating_tag.text if rating_tag else "N/A",
                            "feature": ai_data.get('feature', 'Wearable'),
                            "url": prod_url,
                            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        batch_results.append(data)
                        seen_urls.add(prod_url)
                    except:
                        continue
                
                # Checkpoint persistence
                all_data = load_checkpoint()
                all_data.extend(batch_results)
                save_checkpoint(all_data)
                
                time.sleep(random.uniform(5, 10)) # Respectful crawl delay
                
            except Exception as e:
                print(f"  [!] Exception encountered: {e}")
                break
                
        browser.close()

def run_market_audit():
    """Main execution loop for market intelligence gathering."""
    print("Market Intelligence Audit: Initializing...")
    for kw in KEYWORDS:
        scrape_market_segment(kw)

    # Final Report Generation
    all_data = load_checkpoint()
    if all_data:
        df = pd.DataFrame(all_data)
        df.drop_duplicates(subset=['url'], inplace=True)
        report_path = f"reports/market_intelligence_{datetime.now().strftime('%Y%m%d')}.xlsx"
        os.makedirs("reports", exist_ok=True)
        df.to_excel(report_path, index=False)
        print(f"
[+] Success: Market report generated with {len(df)} unique records.")

if __name__ == "__main__":
    run_market_audit()
