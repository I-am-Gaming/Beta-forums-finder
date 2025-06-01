import requests
import os

# Your base URL templates
eu_base_url_template = "https://eu.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"
kr_base_url_template = "https://r1.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"
in_base_url_template = "https://r2.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"

# Device series and their codes
devices = {
    "s24": "stwentyfour",
    "s23": "stwentythree",
    "s22": "stwentytwo"
}

# Countries for EU
eu_countries = ["uk", "de", "pl"]

# Korea country code (use 'kr' for example)
kr_countries = ["kr"]

# India country code
in_countries = ["in"]

# Build all URLs
def build_urls():
    urls = []

    # EU forums
    for series, code in devices.items():
        for country in eu_countries:
            series_path = f"{series}-{series}-{series}-ultra"
            url = eu_base_url_template.format(series=series_path, country_code=country, series_code=code)
            urls.append(url)

    # Korea forums
    for series, code in devices.items():
        for country in kr_countries:
            series_path = f"{series}-{series}-{series}-ultra"
            url = kr_base_url_template.format(series=series_path, country_code=country, series_code=code)
            urls.append(url)

    # India forums
    for series, code in devices.items():
        for country in in_countries:
            series_path = f"{series}-{series}-{series}-ultra"
            url = in_base_url_template.format(series=series_path, country_code=country, series_code=code)
            urls.append(url)

    return urls

def check_forum(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        text = r.text.lower()
        if "core node not found" in text:
            return False, "Core node not found"
        # Detect if no posts message exists
        if "there are no posts" in text or "no posts" in text:
            return False, "No posts"
        return True, "Active with posts"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    prev_active = set()
    if os.path.exists("active_forums.txt"):
        with open("active_forums.txt", "r", encoding="utf-8") as f:
            prev_active = set(line.strip() for line in f if line.strip())

    urls = build_urls()
    current_active = set()
    new_active = set()

    for url in urls:
        is_active, status = check_forum(url)
        print(f"{url} -> {status}")
        if is_active:
            current_active.add(url)
            if url not in prev_active:
                new_active.add(url)

    # Save updated active URLs
    with open("active_forums.txt", "w", encoding="utf-8") as f:
        for url in sorted(current_active):
            f.write(url + "\n")

    print(f"\nNewly active forums since last run: {len(new_active)}")
    for new_url in new_active:
        print(f" - {new_url}")

if __name__ == "__main__":
    main()