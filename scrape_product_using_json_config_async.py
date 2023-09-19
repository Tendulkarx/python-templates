# Example JSON data for stores and selectors
# Customize this JSON structure to match your needs
# [
#     {
#         "name": "rab",
#         "url": "https://rab.equipment/",
#         "title_selector": "span.base",
#         "price_selector": "span.price"
#     },
#     {
#         "name": "blackdiamond",
#         "url": "https://www.blackdiamondequipment.com",
#         "title_selector": "h1.product-title",
#         "price_selector": "h2.product-price"
#     }
# ]

import httpx
import json
from selectolax.parser import HTMLParser
from rich import print
from dataclasses import dataclass
import asyncio

# Define data classes for Store and Item (customize as needed)
@dataclass
class Store:
    name: str
    url: str
    title_selector: str
    price_selector: str

@dataclass
class Item:
    store: Store
    title: str
    price: str

# Load store data from a JSON file (customize the JSON structure)
def load_stores(filename="stores.json"):
    with open(filename, "r") as f:
        data = json.load(f)
        return [Store(**item) for item in data]

# Asynchronously load a web page and parse it
async def load_page(client, url):
    resp = await client.get(url)
    return HTMLParser(resp.text)

# Parse HTML to extract title and price
def parse(store, html):
    return Item(
        store=store,
        title=html.css_first(store.title_selector).text(strip=True),
        price=html.css_first(store.price_selector).text(strip=True),
    )

# Determine the appropriate store for a given URL
def store_selector(stores, url):
    for store in stores:
        if store.url in url:
            return store

# Main asynchronous function to fetch and process data
async def main():
    # Load store data (customize the JSON filename and structure)
    stores = load_stores("stores.json")

    # Define HTTP headers (customize as needed)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }

    # Create an HTTP client session
    async with httpx.AsyncClient(headers=headers) as client:
        urls = [
            "https://example.com/product1",
            "https://example.com/product2",
        ]

        # Asynchronously fetch HTML content for multiple URLs
        tasks = [load_page(client, url) for url in urls]
        parsed_items = await asyncio.gather(*tasks)

        # Process and print parsed items
        for url, parsed_item in zip(urls, parsed_items):
            store = store_selector(stores, url)
            if store:
                print(parse(store, parsed_item))
            else:
                print(f"No matching store found for URL: {url}")

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
