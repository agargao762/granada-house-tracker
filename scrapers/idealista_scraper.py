from scrapers.base_scraper import BaseScraper
from scrapers.http_scraper import HttpScraper


class IdealistaScraper(BaseScraper):

    def __init__(self):

        self.http = HttpScraper()

    def search(self):

        print("Consultando Idealista...")

        url = (
            "https://www.idealista.com/"
        )

        html = self.http.get(url)

        print(f"Página descargada ({len(html)} caracteres).")

        return []