import requests
import time
import random

# Configuration preserved from your source files
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

series_info = {
    "S26": {"series": "S26-S26-S26-Ultra", "series_code": "stwentyfive"},
    "S25": {"series": "S25-S25-S25-Ultra", "series_code": "stwentyfive"},
    "S24": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "S22": {"series": "S22-S22-S22-Ultra", "series_code": "stwentytwo"},
    "A57": {"series": "Galaxy-A57-5G", "series_code": "afiftyseven"},
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
        # [span_2](start_span)30-second timeout to allow for slow loading[span_2](end_span)
        response = session.get(url, timeout=30, allow_redirects=True)
        final_url = response.url
        page_source = response.text

        # 1. Check for Samsung Account redirection (Restricted/Login required)
        if "account.samsung.com" in final_url:
            return "May be live but can't access"

        # 2. [span_3](start_span)Check for "Not Found" indicators in English and German[span_3](end_span)
        not_found_indicators = [
            "The core node you are trying to access was not found",
            "Der Kernknoten, auf den Sie zugreifen möchten, wurde nicht gefunden",
            "core-node-not-found"
        ]
        
        if any(indicator in page_source for indicator in not_found_indicators):
            return "Not Available"

        # 3. Check for Live indicators (including empty forums)
        if "No new messages" in page_source or "message-subject" in page_source or response.ok:
            return "Live"
        
        return "Not Available"

    except Exception:
        return "Error"

def run():
    session = get_session()
    markdown_lines = [
        "# Samsung Beta Forums Monitor\n",
        f"Last Checked: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        "| Device | Region | Status |",
        "|--------|--------|--------|"
    ]

    for reg_name, config in regions.items():
        for code in config["country_codes"]:
            for device, info in series_info.items():
                url = config["base_url"].format(
                    series=info["series"],
                    country_code=code,
                    series_code=info["series_code"]
                )
                
                status = check_forum(session, url)
                print(f"Checking {device:6} ({code.upper()}): {status}")
                
                # [span_4](start_span)Update Markdown table logic[span_4](end_span)
                if status == "Live":
                    markdown_lines.append(f"| {device} | {code.upper()} | [Live]({url}) |")
                elif status == "May be live but can't access":
                    markdown_lines.append(f"| {device} | {code.upper()} | [Restricted Access]({url}) |")
                else:
                    markdown_lines.append(f"| {device} | {code.upper()} | Not Available |")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))
    
    print("\nREADME.md updated.")

if __name__ == "__main__":
    run()
