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
            if "core-node-not-found" in response.text:
                return "Not Found"
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("div.message-subject")
            return "Live" if posts else "Live - No Posts"
        return f"Error {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

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

# Write to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Samsung Beta Forum Status\n\n")
    for r in results:
        label = f"{r['series']} ({r['country']})"
        if "Live" in r["status"]:
            f.write(f"- **{label}** → [Live]({r['url']})\n")
        else:
            f.write(f"- **{label}** → Not available\n")

print("README.md updated with live forum status.")