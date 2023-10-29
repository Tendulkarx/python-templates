import httpx
from selectolax.parser import HTMLParser


def get_data(store, url, selector):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        },)
    html = HTMLParser(resp.text)
    price = html.css_first(selector).text().strip()
    return {"store": store, "price": price}


def main():
    result = [
        get_data("Amazon", "https://www.amazon.co.uk/dp/B00CWY0CY6", "span.a-offscreen"),
        get_data("KEF", "https://www.amazon.co.uk/dp/B0B4W9G5MC", "span.a-offscreen"),
        get_data("Larq", "https://www.livelarq.com/shop/larq-pitcher-purevis", "span.headPrice_current")
            ]
    print(*result, sep="\n")


if __name__ == '__main__':
    main()
