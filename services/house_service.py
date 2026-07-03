from database.database import get_session
from models.house import House


class HouseService:

    def __init__(self):
        self.session = get_session()

    def get_by_url(self, url):

        return (
            self.session
            .query(House)
            .filter(House.url == url)
            .first()
        )    

    def update_price(self, house, new_price):

        house.price = new_price

        self.session.commit()

    def house_exists(self, url):

        return self.session.query(House).filter_by(url=url).first() is not None

    def save_house(self, house):

        existing = self.get_by_url(house.url)

        if existing is None:

            self.session.add(house)
            self.session.commit()

            return "new"

        if existing.price != house.price:

            old_price = existing.price

            self.update_price(existing, house.price)

            return (
                "price_changed",
                existing,
                old_price
            )

        return "existing"
    
    def get_all(self):

        return self.session.query(House).all()
    
    def save_houses(self, houses):

        new_houses = []

        updated_houses = []

        for house in houses:

            result = self.save_house(house)

            if result == "new":

                new_houses.append(house)

            elif isinstance(result, tuple):

                updated_houses.append(result)

        return new_houses, updated_houses