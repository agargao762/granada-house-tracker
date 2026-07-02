import asyncio

from config import load_config

from services.house_service import HouseService
from services.filter_service import FilterService
from services.scraper_manager import ScraperManager
from services.telegram_service import TelegramService


class HouseTracker:

    def __init__(self):

        self.config = load_config()

        self.service = HouseService()

        self.filter_service = FilterService()

        self.manager = ScraperManager()

        self.telegram = TelegramService()

    def run(self):

        print("=" * 50)
        print("HOUSE TRACKER")
        print("=" * 50)

        search = self.config["searches"][0]

        print("\nBúsquedas configuradas:\n")

        print(f"Nombre      : {search['name']}")
        print(f"Ciudad      : {search['city']}")
        print(f"Precio máx. : {search['max_price']} €")
        print(f"Superficie  : {search['min_size']} m²")
        print(f"Habitaciones: {search['bedrooms']}")
        print(f"Baños       : {search['bathrooms']}")
        print(f"Piscina     : {search['pool']}")

        print("-" * 40)

        houses = self.service.get_all()

        print(f"\nBase de datos: {len(houses)} viviendas")

        print("\nConsultando portales...\n")

        results = self.manager.search_all()

        print(f"📥 Anuncios encontrados: {len(results)}")

        filtered = []

        for house in results:

            if self.filter_service.matches(house, search):
                filtered.append(house)

        print(f"🎯 Cumplen filtros: {len(filtered)}")

        new_houses = self.service.save_houses(filtered)

        print(f"🆕 Nuevas viviendas: {len(new_houses)}")

        if len(new_houses) == 0:
            print("No hay viviendas nuevas.")
            
        
            return

        print("\nNuevas viviendas:\n")

        for house in new_houses:

            print("-" * 40)
            print(f"Portal : {house.portal}")
            print(f"Título : {house.title}")
            print(f"Precio : {house.price:.0f} €")
            print(f"m²     : {house.size:.0f}")
            print(f"URL    : {house.url}")

        if self.telegram.enabled():

            for house in filtered[:1]:
                asyncio.run(
                    self.telegram.send_house(house)
                )

        else:

            print("Telegram deshabilitado.")