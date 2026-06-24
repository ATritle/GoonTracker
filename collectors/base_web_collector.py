import requests
from bs4 import BeautifulSoup


class BaseWebCollector:

    def get_page_text(self, url):

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text("\n")
