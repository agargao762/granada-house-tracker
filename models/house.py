from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True)
    portal = Column(String)
    title = Column(String)
    price = Column(Float)
    size = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    has_pool = Column(Boolean)
    url = Column(String, unique=True)

    def __repr__(self):
        return (
            f"<House("
            f"portal='{self.portal}', "
            f"price={self.price}, "
            f"size={self.size})>"
        )