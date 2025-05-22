from abc import ABC, abstractmethod

class LargeLanguageModelFacade(ABC):
    @abstractmethod
    def relevance(self, question: str, search_result: str) -> float:
        pass
    @abstractmethod
    def ask(self, question: str, search_results: list[str]) -> str:
        pass
