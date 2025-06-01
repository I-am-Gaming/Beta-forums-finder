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
        "base_url": "https://us.community.samsung.com/t5/{series}/ct-p/{series_code}",
        "country_codes": ["us"]  # Special case for US
    }
}

series_info = {
    "S24": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "S22": {"series": "S22-S22-S22-Ultra", "series_code": "stwentytwo"}
}

# Store results
results = []

def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("div.message-subject")
            if posts:
                return "Live - Has Posts"
            else:
                return "Live - No Posts"
        elif "core-node-not-found" in response.text:
            return "Not Found"
        else:
            return f"Error {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Loop through all regions, countries, and series
for region, config in regions.items():
    for code in config["country_codes"]:
        for key, info in series_info.items():
            if region == "us":
                url = config["base_url"].format(series=info["series"], series_code=info["series_code"])
            else:
                url = config["base_url"].format(
                    series=info["series"],
                    country_code=code,
                    series_code=info["series_code"]
                )
            status = check_forum(url)
            results.append({
                "series": key,
                "region": region.upper(),
                "country": code.lower(),
                "url": url,
                "status": status
            })

# Map countries for display
def format_label(series, country):
    country_map = {
        "us": "US", "uk": "UK", "in": "IN", "kr": "KR", "de": "DE", "pl": "PL"
    }
    return f"{series} ({country_map.get(country.lower(), country.upper())})"

# Write to README.md
with open("README.md", "w", encoding="utf-8")