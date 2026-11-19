import os
import json
import time
from datetime import datetime, timedelta
import requests

API_KEY = "579b464db66ec23bdd0000017410a5eb1b9242687e2edc925b16d7ff"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
CACHE_FILE = "mandi_cache.json"

# Flexible keyword mapping between API commodity names and your app's crop keys
COMMODITY_ALIASES = {
    "rice": ["paddy", "dhan", "rice"],
    "wheat": ["wheat", "gehun"],
    "cotton": ["cotton", "kapas"],
    "maize": ["maize", "makka"],
    "chickpea": ["gram", "chana", "bengal gram"],
    "pigeonpeas": ["arhar", "tur", "red gram"],
    "blackgram": ["black gram", "urd", "urad"],
    "mungbean": ["green gram", "moong"],
    "mothbeans": ["moth"],
    "lentil": ["masur", "lentil"],
    "kidneybeans": ["rajgir", "rajma"],
    "banana": ["banana", "kela"],
    "grapes": ["grapes", "angoor"],
    "apple": ["apple", "seb"],
    "mango": ["mango", "aam"],
    "orange": ["orange", "santra"],
    "papaya": ["papaya", "papita"],
    "pomegranate": ["pomegranate", "anar"],
    "watermelon": ["water melon", "tarbooz"],
    "muskmelon": ["kharbuja", "musk melon"],
    "jute": ["jute", "patson"],
    "coffee": ["coffee"],
    "coconut": ["coconut", "nariyal", "copra"],
    "sugarcane": ["sugarcane", "ganna"]
}

def update_cache_from_agmarknet():
    if not os.path.exists(CACHE_FILE):
        print(f"[-] Error: {CACHE_FILE} not found. Ensure the template cache exists.")
        return False

    with open(CACHE_FILE, "r") as f:
        cache_data = json.load(f)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Connecting to Agmarknet Data Gateway...")

    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 200,  # Increased from 50 to 200 to capture pulses and cereals
        "filters[state]": "Uttar Pradesh"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    max_retries = 3
    success = False

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Attempt {attempt}/{max_retries}] Fetching latest UP Mandi auctions...")
            res = requests.get(url, params=params, headers=headers, timeout=25)

            if res.status_code == 200:
                data = res.json()
                records = data.get('records', [])
                print(f"[+] Successfully received {len(records)} active auction records from Agmarknet.")

                if not records:
                    print("[-] Note: Gateway returned 0 records for Uttar Pradesh today. Preserving verified cache.")
                    break

                updated_count = 0
                today_str = datetime.now().strftime("%d %b %Y")

                for r in records:
                    comm_api = str(r.get('commodity', '')).lower()

                    try:
                        modal = float(r.get('modal_price', 0))
                        min_p = float(r.get('min_price', modal * 0.92))
                        max_p = float(r.get('max_price', modal * 1.08))
                        arrivals = float(r.get('arrival', r.get('arrivals_in_qtl', 120)))
                    except (ValueError, TypeError):
                        continue

                    if modal > 0:
                        # Match commodity against our aliases
                        for crop_key, aliases in COMMODITY_ALIASES.items():
                            if any(alias in comm_api for alias in aliases):
                                if crop_key in cache_data.get('commodities', {}):
                                    crop_entry = cache_data['commodities'][crop_key]
                                    crop_entry['current_price'] = modal
                                    crop_entry['min_price'] = min_p
                                    crop_entry['max_price'] = max_p

                                    # Append or update today's history entry
                                    history = crop_entry.get('history', [])
                                    if history and history[-1].get("date") == today_str:
                                        history[-1]["price"] = modal
                                        history[-1]["arrival"] = arrivals
                                    else:
                                        history.append({"date": today_str, "price": modal, "arrival": arrivals})
                                        if len(history) > 7:
                                            history.pop(0)
                                    crop_entry['history'] = history

                                    updated_count += 1
                                    print(f"  -> Updated {crop_key.capitalize()} ({comm_api.title()}): Modal = Rs {modal:.2f}/Q")

                cache_data['updated_at'] = today_str
                with open(CACHE_FILE, "w") as f:
                    json.dump(cache_data, f, indent=2)

                print(f"[+] Sync Complete: {updated_count} agricultural commodities updated in {CACHE_FILE}.")
                success = True
                break

            elif res.status_code == 429:
                print("[-] Rate limited by government gateway (HTTP 429). Backing off...")
                time.sleep(3)
            else:
                print(f"[-] Gateway returned HTTP status {res.status_code}. Retrying...")
                time.sleep(2)

        except requests.exceptions.Timeout:
            print(f"[-] Attempt {attempt} timed out.")
            if attempt < max_retries:
                time.sleep(2)
        except Exception as e:
            print(f"[-] Connection error: {e}")
            if attempt < max_retries:
                time.sleep(2)

    if not success:
        print("[*] Gateway unreachable or no new transactions. Verified APMC baseline retained in cache.")
    return success

if __name__ == "__main__":
    update_cache_from_agmarknet()