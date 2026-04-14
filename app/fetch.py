import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "MyFeedBot/1.0 (personal use)"
}

def fetch(site):
    url = site["url"]

    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            break
        except requests.exceptions.RequestException:
            if i == 2:
                print(f"Failed: {url}")
                return None
            time.sleep(5)

    print(f"{url} -> {res.status_code}")

    if res.status_code == 404:
        print("Page not found")
        return None

    if res.status_code != 200:
        return None

    html = res.text

    if site["mode"] == "full":
        return html

    elif site["mode"] == "selector":
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.select_one(site["selector"])
        return tag.text.strip() if tag else ""

    return None