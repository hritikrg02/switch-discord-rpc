# file:     main.py
# author:   Hritik "Ricky" Saynganthone | hritik@saynganth.one

from dotenv import load_dotenv
from pypresence import Presence
from bs4 import BeautifulSoup
from pypresence import Presence

import os
import time
import sys
import requests

load_dotenv(".env.local")

APP_ID = os.getenv("APP_ID")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}  # fake user agent


# search dekudeals for the query
def find_first_item_url(query: str):
    resp = requests.get(
        "https://www.dekudeals.com/search",
        params={"q": query},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    first_result = soup.select_one(".col.d-block")
    link_tag = first_result.select_one("a.main-link")

    return "https://www.dekudeals.com" + link_tag["href"]


# given the product page for an item, get the title and image
def scrape_item_page(item_url: str):
    resp = requests.get(item_url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one('meta[property="og:title"]')
    image_tag = soup.select_one("img.shadow-img-large")

    title = (
        title_tag["content"].split(" | Deku Deals")[0].strip()
    )  # strip off " | Deku Deals" suffix
    image_url = image_tag["src"]

    return title, image_url


def search_deku(query: str):
    item_url = find_first_item_url(query)
    page_data = scrape_item_page(item_url)

    title, image_url = page_data
    return title, image_url, item_url


def main():
    query = " ".join(sys.argv[1:])
    result = search_deku(query)

    title, image_url, item_url = result
    print(f"found: {title}")
    print(f"image: {image_url}")
    print(f"page:  {item_url}")

    rpc = Presence(APP_ID)
    rpc.connect()

    rpc.update(
        details=f"{title}",
        large_image=image_url,
        large_text=title,
        start=time.time(),
    )

    print("rpc set")

    try:
        while True:
            time.sleep(15)

    except KeyboardInterrupt:
        rpc.clear()
        rpc.close()


if __name__ == "__main__":
    main()
