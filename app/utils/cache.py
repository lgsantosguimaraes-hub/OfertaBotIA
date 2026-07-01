import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "sent_products.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def is_product_sent(item_id: str, hours: int = 24) -> bool:
    cache = load_cache()
    if item_id in cache:
        sent_time = datetime.fromisoformat(cache[item_id])
        if datetime.now() - sent_time < timedelta(hours=hours):
            return True
    return False

def mark_product_sent(item_id: str):
    cache = load_cache()
    cache[item_id] = datetime.now().isoformat()
    save_cache(cache)