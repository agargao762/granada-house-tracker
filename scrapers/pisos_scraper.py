from re import search

from bs4 import BeautifulSoup

from models.house import House
from scrapers.base_scraper import BaseScraper
from scrapers.http_scraper import HttpScraper


class PisosScraper(BaseScraper):

    def __init__(self):
        self.http = HttpScraper()

    def build_url(self, search):

        city = search["city"].lower().replace(" ", "-")

        return f"https://www.pisos.com/venta/pisos-{city}/"

    def search(self, search):

        print("Consultando Pisos.com...")

        url = self.build_url(search)
        print(f"URL: {url}")                        #Temporal

        html = self.http.get(url)

        soup = BeautifulSoup(html, "lxml")

        ads = soup.select("div.ad-preview")

        print(f"Anuncios encontrados: {len(ads)}")

        houses = []

        for ad in ads:

            title = ad.select_one(".ad-preview__title")
            price = ad.select_one(".ad-preview__price")
            subtitle = ad.select_one(".ad-preview__subtitle")

            if not title or not price:
                continue

            chars = ad.select(".ad-preview__char")

            bedrooms = 0
            bathrooms = 0
            size = 0

            for char in chars:

                text = char.get_text(strip=True).lower()

                if "hab" in text:
                    try:
                        bedrooms = int(text.split()[0])
                    except ValueError:
                        pass

                elif "baño" in text:
                    try:
                        bathrooms = int(text.split()[0])
                    except ValueError:
                        pass

                elif "m²" in text:
                    try:
                        size = float(text.split()[0].replace(",", "."))
                    except ValueError:
                        pass

            href = title.get("href", "")

            house = House(
                portal="Pisos.com",
                title=title.get_text(strip=True),
                price=float(
                    price.get_text(strip=True)
                    .replace(".", "")
                    .replace("€", "")
                    .strip()
                ),
                size=size,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                has_pool=False,
                url="https://www.pisos.com" + href
            )

            houses.append(house)

        return houses