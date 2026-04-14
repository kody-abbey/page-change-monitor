from bs4 import BeautifulSoup

def parse(site, html: str):
    if site["mode"] == "full":
        return html

    elif site["mode"] == "selector":
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.select_one(site["selector"])
        return tag.text.strip() if tag else ""

    return ""