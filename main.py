from database.database import create_database
from services.house_tracker import HouseTracker


def main():

    create_database()      # ← crea la BD y las tablas si no existen

    app = HouseTracker()
    app.run()


if __name__ == "__main__":
    main()