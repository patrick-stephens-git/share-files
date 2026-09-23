# coding: utf-8
import logging
import webbrowser
from urllib.parse import quote_plus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

query = 'test'

# {query} is swapped for the URL-encoded query in each template
url_list = ['https://www.amazon.com/s?k={query}','https://www.walmart.com/search?q={query}']

chrome_path = 'open -a /Applications/Google\\ Chrome.app %s'


def build_urls(url_templates: list[str], search_query: str) -> list[str]:
    # Encoded so multi-word queries and special characters don't break the URL
    encoded_query = quote_plus(search_query)
    # str.replace rather than str.format so any other braces in a URL don't raise a KeyError
    return [template.replace('{query}', encoded_query) for template in url_templates]


def open_urls(urls: list[str]) -> None:
    browser = webbrowser.get(chrome_path)
    for url in urls:
        logger.info("Opening %s", url)
        browser.open_new(url)


def main() -> None:
    open_urls(build_urls(url_list, query))


if __name__ == "__main__":
    main()
