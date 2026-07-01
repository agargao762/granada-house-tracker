from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Clase base para todos los scrapers."""

    @abstractmethod
    def search(self):
        """
        Debe devolver una lista de viviendas.
        """
        pass