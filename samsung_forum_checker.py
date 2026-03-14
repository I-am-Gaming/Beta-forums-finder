import requests
import time
import random
from datetime import datetime
import pytz
import os
import re

# Telegram Bot CONFIG
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

country_names = {
    "UK": "UK🇬🇧",
    "DE": "Germany🇩🇪",
    "PL": "Poland🇵🇱",
    "KR": "Korea🇰🇷",
    "IN": "India🇮🇳",
    "US": "US🇺🇸"
}

regions = {
    "eu": {
        "base_url": "https://eu.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}",
        "country_codes": ["uk", "de", "pl"]
    },
    "kr": {
        "base_url": "https://r1.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}",
        "country_codes": ["kr"]
    },
    "in": {
        "base_url": "https://r2.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}",
        "country_codes": ["in"]
    },
    "us": {
        "base_url": "https://us.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}",
        "country_codes": ["us"]
    }
}

device_info = {
    "S26 series": {"series": "S26-S26-S26-Ultra", "series_code": "stwentysix"},
    "S25 series": {"series": "S25-S25-S25-Ultra", "series_code": "stwentyfive"},
    "S24 series": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23 series": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "A57 series": {"series": "Galaxy-A57-5G", "series_code": "afiftyseven"},
    "A56": {"series": "Galaxy-A56-5G", "series_code": "afiftysix"},
    "A55": {"series": "Galaxy-A55-5G", "series_code": "afiftyfive"},
    "A54": {"series": "Galaxy-A54-5G", "series_code": "afiftyfour"},
    "A37": {"series": "Galaxy-A37-5G", "series_code": "athirtyseven"},
    "A36": {"series": "Galaxy-A36-5G", "series_code": "athirtysix"},
    "A35": {"series": "Galaxy-A35-5G", "series_code": "athirtyfive"},
    "ZFold7": {"series": "Z-Fold7", "series_code": "zfoldseven"},
    "ZFlip7": {"series": "Z-Flip7", "series_code": "zflipseven"},
    "ZFold6": {"series": "Z-Fold6", "series_code": "zfoldsix"},
    "ZFlip6": {"series": "Z-Flip6", "series_code": "zflipsix"},
    "ZFold5": {"series": "Z-Fold5", "series_code": "zfoldfive"},
    "ZFlip5": {"series": "Z-Flip5", "series_code": "zflipfive"}
}

def send_telegram_msg(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception:
        pass

def get_previous_states():
    """Returns a dictionary of {device-region: status} from README.md"""
    states = {}
    if os.path.exists("README.md"):
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(r"\| (.*?) \| (.*?) \| (.*?) \|", content)
                for device, region, status in matches:
                    if "Device" in device: continue 
                    key = f"{device.strip()}-{region.strip()}"
                    if "[Live]" in status:
                        clean_status = "Live"
                    elif "Not Available" in status:
                        clean_status = "Not Available"
                    else:
                        clean_status = "Unknown"
                    states[key] = clean_status
        except Exception:
            pass
    return states

def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    })
    return session

def check_forum(session, url):
    try:
        response = session.get(url, timeout=30, allow_redirects=True)
        final_url = response.url
        page_source = response.text

        if "account.samsung.com" in final_url:
            return "May be live but can't access"

        not_found_indicators = [
            "The core node you are trying to access was not found",
            "Der Kernknoten, auf den Sie zugreifen möchten, wurde nicht gefunden",
            "core-node-not-found"
        ]
        
        if any(indicator in page_source for indicator in not_found_indicators):
            return "Not Available"

        if "No new messages" in page_source or "message-subject" in page_source or response.ok:
            return "Live"
        
        return "Not Available"
    except Exception:
        return "Error"

def run():
    previous_states = get_previous_states()
    session = get_session()
    
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
    
    markdown_lines = [
        "# Samsung Beta Forums Monitor\n",
        f"**Last Checked:** {current_time_ist} IST\n",
        "| Device | Region | Status |",
        "|--------|--------|--------|"
    ]

    for reg_name, config in regions.items():
        for code in config["country_codes"]:
            for device, info in device_info.items():
                url = config["base_url"].format(
                    series=info["series"],
                    country_code=code,
                    series_code=info["series_code"]
                )
                
                status = check_forum(session, url)
                region_upper = code.upper()
                state_key = f"{device}-{region_upper}"
                country = country_names.get(region_upper, region_upper)
                
                # --- TELEGRAM TRIGGER LOGIC ---
                if state_key in previous_states:
                    old_status = previous_states[state_key]
                    
                    if status == "Live" and old_status == "Not Available":
                        send_telegram_msg(f"🚀 *{device} Beta Forum* now live in *{country}*!")
                    
                    elif status == "Not Available" and old_status == "Live":
                        send_telegram_msg(f"🔴 *{device} Beta Forum* removed from *{country}*")

                # --- BUILD MARKDOWN ---
                if status == "Live":
                    markdown_lines.append(f"| {device} | {region_upper} | [Live]({url}) |")
                elif status == "May be live but can't access":
                    markdown_lines.append(f"| {device} | {region_upper} | [Restricted Access]({url}) |")
                else:
                    markdown_lines.append(f"| {device} | {region_upper} | Not Available |")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))
    
    print(f"\nUpdate complete at {current_time_ist} IST.")

if __name__ == "__main__":
    run()
