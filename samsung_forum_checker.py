import requests
from bs4 import BeautifulSoup

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
        "base_url": "https://us.community.samsung.com/t5/{series_code}/ct-p/{series_code}",
        "country_codes": ["us"]
    }
}

series_info = {
    "S24": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "S22": {"series": "S22-S22-S22-Ultra", "series_code": "stwentytwo"}
}

def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if "core-node-not-found" in response.text.lower():
                return "Not available"
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.select("div.message-subject"):
                return f"[Live]({url})"
            return f"[Live - No Posts]({url})"
        return "Not available"
    except:
        return "Not available"

readme_lines = ["# Samsung Beta Forums Status\n\n"]

for region, config in regions.items():
    for country in config["country_codes"]:
        for model, info in series_info.items():
            if region == "us":
                url = config["base_url"].format(series_code=info["series_code"])
            else:
                url = config["base_url"].format(series=info["series"], country_code=country, series_code=info["series_code"])
            status = check_forum(url)
            readme_lines.append(f"{model} ({country.upper()}) ----> {status}\n")

with open("README.md", "w", encoding="utf-8") as f:
    f.writelines(readme_lines)