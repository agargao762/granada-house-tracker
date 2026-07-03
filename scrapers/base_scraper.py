from abc import ABC, abstractmethod


class BaseScraper:

    def search(self, search):
        raise NotImplementedError