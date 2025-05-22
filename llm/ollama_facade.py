import json
from langchain_ollama.llms import OllamaLLM
from llm.llm_facade import LargeLanguageModelFacade

class OllamaFacade(LargeLanguageModelFacade):
    def __init__(self, model: str):
        self.llm = OllamaLLM(model=model)
    def relevance(self, question: str, search_result: str) -> float:
        prompt = """Study the following question and data then return the relevance or liklihood that the supplied data could be used to answer the question. This relevance would be in the form of a floating point number between 0.0 and 1.0 where 0.0 would mean that the data isn't useful at all, 1.0 would indicate that the data is useful with complete certainty, and 0.5 would suggest that the data would just as likely be useful as not. Output as JSON in the specified schema.

**QUESTION**
%s

**DATA**
%s

**SCHEMA**
{
  "relevance": "float"
}
""" % (question, search_result)
        rv = 0.0
        answer = None
        try:
            answer = self.llm.invoke(prompt)
            result = json.loads(answer)
            if 'relevance' in result:
                rv = float(result['relevance'])
            else:
                print(f"unexpected result format {result}")
        except:
            print(f"Error with prompt {prompt}")
            if answer:
                print(f"answer is {answer}")
        return rv

    def ask(self, question: str, search_results: list[str]) -> str:
        if len(search_results) > 0:
            prompt = """You are an expert tasked to answer the following question based exclusively on the provided data.

**QUESTION**
%s

**DATA**
%s
""" % (question, "\n\n".join(search_results))
        else:
            prompt = """You are an expert tasked to answer the following question based on your already existing knowledge of the subject.

**QUESTION**
%s
""" % (question)
        try:
            return self.llm.invoke(prompt)
        except:
            print(f"Error with prompt {prompt}")
            return "error with LLM"
