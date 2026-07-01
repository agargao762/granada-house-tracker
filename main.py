from config import load_config
from database.database import create_database, get_session
from models.house import House
from scrapers.fake_scraper import FakeScraper

def main():
    print("=" * 50)
    print("HOUSE TRACKER")
    print("=" * 50)

    # Crear la base de datos si no existe
    create_database()

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

    # Abrimos la base de datos
    session = get_session()

    # Creamos una vivienda de prueba
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

    # Comprobamos si ya existe una vivienda con esa URL
    existing_house = session.query(House).filter_by(url=house.url).first()

    if existing_house:
        print("\nℹ️ La vivienda ya existe en la base de datos.")
    else:
        session.add(house)
        session.commit()
        print("\n✅ Vivienda de prueba guardada en la base de datos.")

        print("\nViviendas guardadas:\n")

    houses = session.query(House).all()

    for house in houses:
        print("-" * 40)
        print(f"Portal      : {house.portal}")
        print(f"Título      : {house.title}")
        print(f"Precio      : {house.price} €")
        print(f"Superficie  : {house.size} m²")
        print(f"Dormitorios : {house.bedrooms}")
        print(f"Baños       : {house.bathrooms}")
        print(f"Piscina     : {'Sí' if house.has_pool else 'No'}")

        print("\nConsultando Fake Portal...\n")

    scraper = FakeScraper()

    results = scraper.search()

    print(f"Se han encontrado {len(results)} viviendas.\n")

    for house in results:
        print("-" * 40)
        print(f"Portal      : {house.portal}")
        print(f"Título      : {house.title}")
        print(f"Precio      : {house.price} €")
        print(f"Superficie  : {house.size} m²")


if __name__ == "__main__":
    main()