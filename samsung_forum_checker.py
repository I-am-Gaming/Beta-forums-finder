import requests
from bs4 import BeautifulSoup

# Country & series setup
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
    "S24": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "S22": {"series": "S22-S22-S22-Ultra", "series_code": "stwentytwo"}
}

results = []

def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("div.message-subject")
            if posts:
                return "Live"
            else:
                return "Live (No Posts)"
        elif "core-node-not-found" in response.text:
            return "Not available"
        else:
            return "Error"
    except Exception:
        return "Error"

for region, config in regions.items():
    for code in config["country_codes"]:
        for key, info in series_info.items():
            url = config["base_url"].format(
                series=info["series"],
                country_code=code,
                series_code=info["series_code"]
            )
            status = check_forum(url)
            results.append({
                "series": key,
                "region": region.upper(),
                "country": code.upper(),
                "url": url,
                "status": status
            })

# Write summary to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Samsung Beta Forums Status\n\n")
    for r in results:
        if r["status"] == "Live":
            line = f"{r['series']}({r['country']}) ----> [Live]({r['url']})\n"
        elif r["status"] == "Live (No Posts)":
            # You can decide whether to hyperlink or not here; example below with hyperlink and "No Posts"
            line = f"{r['series']}({r['country']}) ----> [Live (No Posts)]({r['url']})\n"
        else:
            line = f"{r['series']}({r['country']}) ----> Not available\n"
        f.write(line)

print("README.md updated with forum status.")