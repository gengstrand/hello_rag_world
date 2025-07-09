from abc import ABC, abstractmethod
from typing import Generator

class IndexerFacade(ABC):
    @abstractmethod
    def documents(self) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def title(self) -> str:
        pass

    @abstractmethod
    def collection_name(self) -> str:
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        pass