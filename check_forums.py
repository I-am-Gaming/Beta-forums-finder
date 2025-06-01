import requests
import os

# Base URL templates
eu_base_url_template = "https://eu.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"
kr_base_url_template = "https://r1.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"
in_base_url_template = "https://r2.community.samsung.com/t5/{series}/ct-p/{country_code}-bp-{series_code}"

# Device series and codes
devices = {
    "s24": "stwentyfour",
    "s23": "stwentythree",
    "s22": "stwentytwo"
}

# Country codes
eu_countries = ["uk", "de", "pl"]
kr_countries = ["kr"]
in_countries = ["in"]

def build_urls():
    urls = []

    for series, code in devices.items():
        series_path = f"{series}-{series}-{series}-ultra"
        
        for country in eu_countries:
            urls.append(eu_base_url_template.format(series=series_path, country_code=country, series_code=code))
        
        for country in kr_countries:
            urls.append(kr_base_url_template.format(series=series_path, country_code=country, series_code=code))
        
        for country in in_countries:
            urls.append(in_base_url_template.format(series=series_path, country_code=country, series_code=code))
    
    return urls

def check_forum(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return "not_found", f"HTTP {r.status_code}"
        
        text = r.text.lower()

        if "core node not found" in text:
            return "not_found", "Core node not found"
        
        if "there are no posts" in text or "no posts" in text:
            return "live_empty", "Live but no posts"
        
        return "live_posts", "Live with posts"
    
    except Exception as e:
        return "not_found", f"Error: {e}"

def main():
    # Load previously active forums
    prev_active = set()
    if os.path.exists("active_forums.txt"):
        with open("active_forums.txt", "r", encoding="utf-8") as f:
            prev_active = set(line.strip() for line in f if line.strip())

    urls = build_urls()
    current_active = set()
    new_active = set()

    live_with_posts = []
    live_no_posts = []
    not_found = []

    for url in urls:
        status_code, status_msg = check_forum(url)
        
        if status_code == "live_posts":
            current_active.add(url)
            live_with_posts.append(url)
            if url not in prev_active:
                new_active.add(url)
        elif status_code == "live_empty":
            live_no_posts.append(url)
        else:
            not_found.append((url, status_msg))
    
    # Save current active URLs (only live with posts)
    with open("active_forums.txt", "w", encoding="utf-8") as f:
        for url in sorted(current_active):
            f.write(url + "\n")

    # Console report
    print(f"\n✅ Live with posts ({len(live_with_posts)}):")
    for url in live_with_posts:
        print(f"  - {url}")
    
    print(f"\n⚠️ Live but no posts ({len(live_no_posts)}):")
    for url in live_no_posts:
        print(f"  - {url}")
    
    print(f"\n❌ Not found or error ({len(not_found)}):")
    for url, reason in not_found:
        print(f"  - {url} ({reason})")

    if new_active:
        print(f"\n🆕 Newly active forums ({len(new_active)}):")
        for url in new_active:
            print(f"  - {url}")
    
    if not current_active:
        print("\n📁 No active forums found, but 'active_forums.txt' created as empty.")
    else:
        print(f"\n📁 'active_forums.txt' updated with {len(current_active)} active forums.")

if __name__ == "__main__":
    main()