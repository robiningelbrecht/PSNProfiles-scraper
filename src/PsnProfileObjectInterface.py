from __future__ import annotations
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class PsnProfileObjectInterface(ABC):

    @abstractmethod
    def to_json(self) -> str:
        pass

    @abstractmethod
    def create_from_soup(soup: BeautifulSoup) -> PsnProfileObjectInterface:
        pass
