from config import load_config
from database.database import create_database
from models.house import House
from services.scraper_manager import ScraperManager
from services.house_service import HouseService
from services.filter_service import FilterService
from services.telegram_service import TelegramService


def main():
    print("=" * 50)
    print("HOUSE TRACKER")
    print("=" * 50)

    # Crear la base de datos si no existe
    create_database()

    # Crear el servicio de acceso a la base de datos
    service = HouseService()
    telegram = TelegramService()
    filter_service = FilterService()

    # Leer la configuración
    config = load_config()

    print("\nBúsquedas configuradas:\n")

    for search in config["searches"]:
        print(f"Nombre      : {search['name']}")
        print(f"Ciudad      : {search['city']}")
        print(f"Precio máx. : {search['max_price']} €")
        print(f"Superficie  : {search['min_size']} m²")
        print(f"Habitaciones: {search['bedrooms']}")
        print(f"Baños       : {search['bathrooms']}")
        print(f"Piscina     : {search['pool']}")
        print("-" * 40)

    # --------------------------------------------------
    # Vivienda de prueba (la eliminaremos más adelante)
    # --------------------------------------------------

    house = House(
        portal="Prueba",
        title="Piso de prueba",
        price=250000,
        size=95,
        bedrooms=3,
        bathrooms=2,
        has_pool=True,
        url="https://ejemplo.com/piso-prueba"
    )

    if service.save_house(house):
        print("\n✅ Vivienda de prueba guardada.")
    else:
        print("\nℹ️ La vivienda de prueba ya existía.")

    # --------------------------------------------------
    # Resumen de la base de datos
    # --------------------------------------------------

    houses = service.get_all()

    print(f"\nBase de datos: {len(houses)} viviendas")

    # --------------------------------------------------
    # Consultar el Fake Portal
    # --------------------------------------------------

    print("\nConsultando portales...\n")

    manager = ScraperManager()

    results = manager.search_all()

    print(f"📥 Anuncios encontrados: {len(results)}")

    filtered = []

    search = config["searches"][0]

    for house in results:

        if filter_service.matches(house, search):
            filtered.append(house)

    print(f"🎯 Cumplen filtros: {len(filtered)}")

    new_houses = service.save_houses(filtered)

    print(f"🆕 Nuevas viviendas: {len(new_houses)}")

    if len(new_houses) == 0:
        print("No hay viviendas nuevas.")
    else:
        print("\nNuevas viviendas:\n")

    for house in new_houses:
        print("-" * 40)
        print(f"Portal : {house.portal}")
        print(f"Título : {house.title}")
        print(f"Precio : {house.price:.0f} €")
        print(f"m²     : {house.size:.0f}")
        print(f"URL    : {house.url}")

    if telegram.enabled():
        telegram.send("House Tracker ejecutado correctamente.")
    else:
        print("Telegram deshabilitado.")


if __name__ == "__main__":
    main()