import requests

# Define base URL templates for different community domains and device series
eu_base_url_template = "https://eu.community.samsung.com/t5/{series}/{country_code}-bp-{series_code}"
kr_base_url_template = "https://r1.community.samsung.com/t5/{series}/{country_code}-bp-{series_code}"
in_base_url_template = "https://r2.community.samsung.com/t5/{series}/{country_code}-bp-{series_code}"

# Device series info: URL path and series code for the beta forums
device_series = {
    "S24": {
        "path": "S24-S24-S24-Ultra",
        "series_code": "stwentyfour"
    },
    "S23": {
        "path": "s23-s23-s23-ultra",
        "series_code": "stwentythree"
    },
    "S22": {
        "path": "s22-s22-s22-ultra",
        "series_code": "stwentytwo"
    }
}

# Countries by community domain
eu_countries = ["uk", "de", "pl"]
kr_countries = ["kr"]  # Korea
in_countries = ["in"]  # India

# Aggregate URLs
urls_to_check = []

# Build EU URLs for each device and country
for device, info in device_series.items():
    for country in eu_countries:
        url = eu_base_url_template.format(
            series=info["path"],
            country_code=country,
            series_code=info["series_code"]
        )
        urls_to_check.append(url)

# Build Korea URLs for each device and country
for device, info in device_series.items():
    for country in kr_countries:
        url = kr_base_url_template.format(
            series=info["path"],
            country_code=country,
            series_code=info["series_code"]
        )
        urls_to_check.append(url)

# Build India URLs for each device and country
for device, info in device_series.items():
    for country in in_countries:
        url = in_base_url_template.format(
            series=info["path"],
            country_code=country,
            series_code=info["series_code"]
        )
        urls_to_check.append(url)

# Function to check forum URL status
def check_forum(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Not found (HTTP {response.status_code})"
        elif "core node not found" in response.text.lower():
            return "Not found (core node message)"
        else:
            return "Active"
    except requests.RequestException as e:
        return f"Error ({str(e)})"

# Run all checks and print results
print("Samsung Beta Forums Status Report")
print("---------------------------------")
for url in urls_to_check:
    status = check_forum(url)
    print(f"{url} -> {status}")