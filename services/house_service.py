from database.database import get_session
from models.house import House


class HouseService:

    def __init__(self):
        self.session = get_session()

    def house_exists(self, url):

        return self.session.query(House).filter_by(url=url).first() is not None

    def save_house(self, house):

        if self.house_exists(house.url):
            return False

        self.session.add(house)
        self.session.commit()

        return True

    def get_all(self):

        return self.session.query(House).all()
    
    def save_houses(self, houses):

        new_houses = []

        for house in houses:

            if self.save_house(house):
                new_houses.append(house)

        return new_houses