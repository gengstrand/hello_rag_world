from llm.llm_facade import LargeLanguageModelFacade 

class MockedLargeLanguageModel(LargeLanguageModelFacade):
    def __init__(self):
        super().__init__()

    def relevance(self, question: str, context: str) -> float:
        return sum(1 for word in question.split(' ') if word in context) / len(question.split(' '))
    
    def ask(self, question: str, context: list[str]) -> str:
        rv = [doc for doc in context for word in question.split(' ') if word in doc]
        return '\n'.join(rv) if len(rv) > 0 else "I don't know"