from scrapers.pisos_scraper import PisosScraper

class ScraperManager:

    def __init__(self):

        self.scrapers = [
            PisosScraper()
        ]

    def search_all(self, search):

        houses = []

        for scraper in self.scrapers:

            houses.extend(scraper.search(search))

        return houses