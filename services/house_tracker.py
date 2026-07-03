import asyncio


from config import load_config

from services.house_service import HouseService
from services.filter_service import FilterService
from services.scraper_manager import ScraperManager
from services.telegram_service import TelegramService
from app_config import APP_NAME, APP_ICON


class HouseTracker:

    def __init__(self):

        self.config = load_config()

        self.service = HouseService()

        self.filter_service = FilterService()

        self.manager = ScraperManager()

        self.telegram = TelegramService()

    def print_search(self, search):
            
        print("=" * 50)
        print(f"{APP_ICON} {APP_NAME}")
        print("=" * 50)

        print(f"Ciudad      : {search['city']}")
        print(f"Precio máx. : {search['max_price']} €")
        print(f"Superficie  : {search['min_size']} m²")
        print(f"Habitaciones: {search['bedrooms']}")
        print(f"Baños       : {search['bathrooms']}")
        print(f"Piscina     : {search['pool']}")

    def process_search(self, search):

        self.print_search(search)

        print("\nConsultando portales...\n")

        results = self.manager.search_all(search)
        
        print(f"📥 Anuncios encontrados: {len(results)}")

        filtered = []

        for house in results:

            if self.filter_service.matches(house, search):
                filtered.append(house)

        print(f"🎯 Cumplen filtros: {len(filtered)}")

        new_houses, updated_houses = self.service.save_houses(filtered)
        
        print(f"🆕 Nuevas viviendas: {len(new_houses)}")

        print(f"💰 Cambios de precio: {len(updated_houses)}")



        if not new_houses and not updated_houses:
            print("No hay novedades.")
            return

        print("\nNuevas viviendas:\n")

        for house in new_houses:

            print("-" * 40)
            print(f"Portal : {house.portal}")
            print(f"Título : {house.title}")
            print(f"Precio : {house.price:.0f} €")
            print(f"m²     : {house.size:.0f}")
            print(f"URL    : {house.url}")

        if updated_houses:

            print("\nCambios de precio:\n")

            for _, house, old_price in updated_houses:

                print("-" * 40)
                print(f"Título : {house.title}")
                print(f"Antes  : {old_price:.0f} €")
                print(f"Ahora  : {house.price:.0f} €")

        if self.telegram.enabled():

            asyncio.run(
                self.telegram.send_houses(
                    search,
                    new_houses
                )
            )

        else:
            print("Telegram deshabilitado.")


    def run(self):

        print("=" * 50)
        print(f"{APP_ICON} {APP_NAME}")
        print("=" * 50)

        houses = self.service.get_all()

        print(f"\nBase de datos: {len(houses)} viviendas")

        for search in self.config["searches"]:
            
            self.process_search(search)