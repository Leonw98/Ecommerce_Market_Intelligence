# market_intelligence_engine.py
import os
import json
import time
import random
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# CONFIG: Broadening the scope for "Massive" dataset
KEYWORDS = [
    "smart health ring", "sleep tracker ring", "fitness tracker watch",
    "GPS sports watch", "ECG smartwatch", "biometric wearable",
    "Oura ring competitors", "Garmin fenix", "Apple Watch Ultra",
    "Samsung Galaxy Watch", "Fitbit Sense", "Whoop strap alternative",
    "smart jewelry", "biohacking wearable"
]

CHECKPOINT_FILE = "data/market_research_checkpoint.json"

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except: return []
    return []

def save_checkpoint(data):
    os.makedirs("data", exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def enrich_data_ai(title):
    """
    Advanced brand extraction. Avoids 'Unknown' and 'Smart'.
    Uses title heuristics if AI fails.
    """
    # 1. Manual Map for known high-value players
    brand_map = {
        "oura": "Oura", "garmin": "Garmin", "fitbit": "Fitbit", "apple": "Apple",
        "samsung": "Samsung", "whoop": "Whoop", "amazfit": "Amazfit", "huawei": "Huawei",
        "findtime": "Findtime", "wellue": "Wellue", "ringconn": "RingConn", "ultrahuman": "Ultrahuman"
    }
    
    clean_title = title.lower()
    detected_brand = ""
    for key, val in brand_map.items():
        if key in clean_title:
            detected_brand = val
            break

    # 2. AI Extraction with descriptive fallback instructions
    try:
        prompt = f"Identify the BRAND or MANUFACTURER from: '{title}'. If no brand is visible, provide the most descriptive name for this product (e.g. 'WellnessRing'). Return ONLY JSON: {{'brand': '...', 'category': '...'}}"
        payload = {"model": "llama3.1", "messages": [{"role": "user", "content": prompt}], "stream": False, "format": "json"}
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=4)
        
        if response.status_code == 200:
            ai_data = json.loads(response.json()['message']['content'])
            brand = ai_data.get('brand', detected_brand)
            if isinstance(brand, list): brand = brand[0]
            
            # Clean generic results
            bad_words = ["unknown", "smart", "health", "ring", "watch", "wearable"]
            if str(brand).lower() in bad_words or not brand:
                brand = detected_brand

            cat = ai_data.get('category', 'Wearable')
            return {"brand": str(brand) if brand else "Generic Wearable", "category": str(cat)}
    except: pass

    # 3. Final Heuristic Fallback (First significant word)
    if not detected_brand:
        words = [w for w in title.split() if w.lower() not in ["smart", "health", "ring", "watch", "the", "for"]]
        detected_brand = words[0] if words else "Generic"

    return {"brand": detected_brand, "category": "Wearable"}

def run_self_audit(record):
    """
    Real-time data integrity check.
    Sets 'is_high_signal' to True if key fields are valid.
    """
    has_brand = record['brand'] != "Unknown" and record['brand'] != "Smart"
    has_price = record['price'] != "£N/A"
    has_rating = record['rating'] != "N/A"
    
    record['is_high_signal'] = all([has_brand, has_price, has_rating])
    return record

def scrape_market_segment(kw, target_pages=20):
    print(f"[*] Starting DEEP research for: {kw}")
    existing_data = load_checkpoint()
    seen_urls = {r["url"] for r in existing_data}
    
    with sync_playwright() as p:
        # Optimized for headless persistence
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        page.route("**/*.{png,jpg,jpeg,css}", lambda route: route.abort())

        for page_num in range(1, target_pages + 1):
            # NO BUDGET FILTER: Broad wearables search
            url = f"https://www.amazon.co.uk/s?k={kw.replace(' ', '+')}&page={page_num}"
            print(f"  [>] Page {page_num} of {target_pages}...")
            
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                if "Robot" in page.title():
                    print("  [!] Blocked. Waiting 60s...")
                    time.sleep(60)
                    continue

                page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=20000)
                page.evaluate("window.scrollBy(0, 2000)")
                time.sleep(random.uniform(2, 4))
                
                soup = BeautifulSoup(page.content(), 'html.parser')
                items = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                new_items = []
                for item in items:
                    try:
                        # 1. Basic Links & ID
                        link_tag = item.find('a', {'class': 'a-link-normal'}, href=True)
                        if not link_tag: continue
                        prod_url = "https://www.amazon.co.uk" + link_tag['href'].split('?')[0]
                        if prod_url in seen_urls: continue
                        
                        asin = item.get('data-asin', "N/A")
                        
                        # 2. Advanced Extraction Logic
                        name = item.find('h2').get_text(strip=True)
                        price_whole = item.find('span', {'class': 'a-price-whole'})
                        rating = item.find('span', {'class': 'a-icon-alt'})
                        reviews_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'})
                        
                        # Best Seller / Amazon Choice Badges
                        badge = "None"
                        if "Best Seller" in item.get_text(): badge = "Best Seller"
                        elif "Amazon's Choice" in item.get_text(): badge = "Amazon's Choice"
                        
                        # Prime Status
                        is_prime = "Yes" if item.find('i', {'aria-label': 'Prime'}) else "No"

                        # AI Enrichment
                        ai = enrich_data_ai(name)
                        
                        data = {
                            "asin": asin,
                            "product_name": name,
                            "brand": ai.get('brand', 'Unknown'),
                            "category": ai.get('category', 'Wearable'),
                            "price": f"£{price_whole.text.strip()}" if price_whole else "N/A",
                            "rating": rating.text.split(' ')[0] if rating else "N/A",
                            "total_reviews": reviews_count.text.replace('(', '').replace(')', '').strip() if reviews_count else "0",
                            "badge": badge,
                            "is_prime": is_prime,
                            "url": prod_url,
                            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Apply Self-Audit
                        data = run_self_audit(data)
                        
                        new_items.append(data)
                        seen_urls.add(prod_url)
                    except: continue
                
                # Incremental Save
                existing_data.extend(new_items)
                save_checkpoint(existing_data)
                print(f"    [+] Saved {len(new_items)} new items. Total: {len(existing_data)}")
                
                time.sleep(random.uniform(5, 12)) 
                
            except Exception as e:
                print(f"  [!] Error: {e}")
                break
                
        browser.close()

def run_market_audit():
    print(f"--- STARTING MASSIVE WEARABLE RESEARCH RUN: {datetime.now()} ---")
    for kw in KEYWORDS:
        scrape_market_segment(kw)
    
    # Final Export to Excel
    all_data = load_checkpoint()
    if all_data:
        df = pd.DataFrame(all_data)
        df.drop_duplicates(subset=['url'], inplace=True)
        report_path = f"reports/massive_wearable_market_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        os.makedirs("reports", exist_ok=True)
        df.to_excel(report_path, index=False)
        print(f"\n[FINISH] Massive report generated: {len(df)} records.")

if __name__ == "__main__":
    run_audit_start_time = time.time()
    run_market_audit()
    print(f"Total Run Time: {(time.time() - run_audit_start_time)/60:.2f} minutes")
