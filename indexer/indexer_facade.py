from abc import ABC, abstractmethod
from typing import Generator

class IndexerFacade(ABC):
    @abstractmethod
    def documents(self) -> Generator[str, None, None]:
        pass
    def title(self) -> str:
        pass