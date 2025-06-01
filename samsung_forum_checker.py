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

# Loop through all combinations and collect results
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

# Filter only live forums (has posts or no posts)
live_forums = [r for r in results if r['status'].startswith("Live")]

# Sort live forums by region, country, then series
live_forums.sort(key=lambda x: (x['region'], x['country'], x['series']))

# Write live forums to file
with open("active_forums.txt", "w", encoding="utf-8") as f:
    if live_forums:
        for r in live_forums:
            f.write(f"[{r['region']}/{r['country']}/{r['series']}] {r['url']} --> {r['status']}\n")
    else:
        f.write("No live forums found.\n")

print("Live forum check completed.")