from models.house import House
from scrapers.base_scraper import BaseScraper


class FakeScraper(BaseScraper):

    def search(self):

        return [

            House(
                portal="Fake Portal",
                title="Piso junto al Palacio de Congresos",
                price=329000,
                size=97,
                bedrooms=3,
                bathrooms=2,
                has_pool=True,
                url="https://fakeportal.es/1"
            ),

            House(
                portal="Fake Portal",
                title="Ático con piscina en Zaidín",
                price=315000,
                size=91,
                bedrooms=3,
                bathrooms=2,
                has_pool=True,
                url="https://fakeportal.es/2"
            )

        ]