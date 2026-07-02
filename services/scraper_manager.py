from scrapers.pisos_scraper import PisosScraper

class ScraperManager:

    def __init__(self):

        self.scrapers = [
            PisosScraper()
        ]

    def search_all(self):

        houses = []

        for scraper in self.scrapers:

            try:
                results = scraper.search()
                houses.extend(results)

            except Exception as e:
                print(f"⚠️ Error en {scraper.__class__.__name__}: {e}")

        return houses