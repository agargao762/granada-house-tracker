from config import load_config
from database.database import create_database
from models.house import House
from scrapers.fake_scraper import FakeScraper
from services.house_service import HouseService


def main():
    print("=" * 50)
    print("HOUSE TRACKER")
    print("=" * 50)

    # Crear la base de datos si no existe
    create_database()

    # Crear el servicio de acceso a la base de datos
    service = HouseService()

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
    # Mostrar viviendas guardadas
    # --------------------------------------------------

    print("\nViviendas guardadas:\n")

    houses = service.get_all()

    for house in houses:
        print("-" * 40)
        print(f"Portal      : {house.portal}")
        print(f"Título      : {house.title}")
        print(f"Precio      : {house.price} €")
        print(f"Superficie  : {house.size} m²")
        print(f"Dormitorios : {house.bedrooms}")
        print(f"Baños       : {house.bathrooms}")
        print(f"Piscina     : {'Sí' if house.has_pool else 'No'}")

    # --------------------------------------------------
    # Consultar el Fake Portal
    # --------------------------------------------------

    print("\nConsultando Fake Portal...\n")

    scraper = FakeScraper()

    results = scraper.search()

    print(f"Se han encontrado {len(results)} viviendas.")

    new_houses = service.save_houses(results)

    print(f"Nuevas viviendas guardadas: {len(new_houses)}\n")

    if len(new_houses) == 0:
        print("No hay viviendas nuevas.")
    else:
        for house in new_houses:
            print("-" * 40)
            print(f"Portal      : {house.portal}")
            print(f"Título      : {house.title}")
            print(f"Precio      : {house.price} €")
            print(f"Superficie  : {house.size} m²")


if __name__ == "__main__":
    main()