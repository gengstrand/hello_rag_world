import logging
from llm.llm_facade import LargeLanguageModelFacade 
from llm.term_stats import TermStats

class MockedLargeLanguageModel(LargeLanguageModelFacade):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.question_stats = {}

    def relevance(self, question: str, context: str) -> float:
        if question not in self.question_stats:
            self.question_stats[question] = TermStats(question)
        self.logger.info(f"term stats for context matches {self.question_stats[question].similarity(context)}")
        return sum(1 for word in question.split(' ') if word in context) / len(question.split(' '))
    
    def ask(self, question: str, context: list[str]) -> str:
        rv = [doc for doc in context for word in question.split(' ') if word in doc]
        return '\n'.join(rv) if len(rv) > 0 else "I don't know"