class FilterService:

    def matches(self, house, search):

        if house.price > search["max_price"]:
            return False

        if house.size < search["min_size"]:
            return False

        if house.bedrooms < search["bedrooms"]:
            return False

        if house.bathrooms < search["bathrooms"]:
            return False

        if search["pool"] and not house.has_pool:
            return False

        return True