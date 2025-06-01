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

# Store results
results = []

def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("div.message-subject")  # Post titles
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

# Write to file (always created)
with open("active_forums.txt", "w", encoding="utf-8") as f:
    if results:
        for r in results:
            f.write(f"[{r['region']}/{r['country']}/{r['series']}] {r['url']} --> {r['status']}\n")
    else:
        f.write("No forums found.\n")

print("Forum check completed.")