import requests
import time

headers = {
    "User-Agent": "MyFeedBot/1.0 (personal use)"
}

def fetch(url: str):
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            break
        except requests.exceptions.RequestException:
            if i == 2:
                return None
            time.sleep(5)

    if res.status_code != 200:
        return None

    return res.text