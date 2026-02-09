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
    "S25": {"series": "S25-S25-S25-Ultra", "series_code": "stwentyfive"},
    "S24": {"series": "S24-S24-S24-Ultra", "series_code": "stwentyfour"},
    "S23": {"series": "S23-S23-S23-Ultra", "series_code": "stwentythree"},
    "S22": {"series": "S22-S22-S22-Ultra", "series_code": "stwentytwo"},
    "A56": {"series": "Galaxy-A56-5G", "series_code": "afiftysix"},
    "A55": {"series": "Galaxy-A55-5G", "series_code": "afiftyfive"},
    "A54": {"series": "Galaxy-A54-5G", "series_code": "afiftyfour"},
    "A36": {"series": "Galaxy-A36-5G", "series_code": "athirtysix"},
    "A35": {"series": "Galaxy-A35-5G", "series_code": "athirtyfive"},
    "ZFold7": {"series": "Z-Fold7", "series_code": "zfoldseven"},
    "ZFlip7": {"series": "Z-Flip7", "series_code": "zflipseven"},
    "ZFold6": {"series": "Z-Fold6", "series_code": "zfoldsix"},
    "ZFlip6": {"series": "Z-Flip6", "series_code": "zflipsix"},
    "ZFold5": {"series": "Z-Fold5", "series_code": "zfoldfive"},
    "ZFlip5": {"series": "Z-Flip5", "series_code": "zflipfive"}
}

# Store markdown table rows
markdown_lines = ["| Device | Region | Status |", "|--------|--------|--------|"]

def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select("div.message-subject")

            if "No new messages" in response.text:
                return "Live - Newly Created"
            elif posts:
                return "Live - Has Posts"
            else:
                return "Live"

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
            region_label = code.upper()

            if status.startswith("Live"):
                markdown_lines.append(f"| {key} | {region_label} | [{status}]({url}) |")
            else:
                markdown_lines.append(f"| {key} | {region_label} | Not Available |")

# Write to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Samsung Beta Forums Monitor\n\n")
    f.write("\n".join(markdown_lines))

print("README.md has been updated with latest forum statuses.")
