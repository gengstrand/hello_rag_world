from abc import ABC, abstractmethod

class SearchFacade(ABC):
    @abstractmethod
    def add_pages(self) -> str:
        pass
    @abstractmethod
    def search(self, query: str, top_results: int, simularity: float) -> list[str]:
        pass
