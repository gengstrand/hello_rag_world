import json
import logging
from langchain_ollama.llms import OllamaLLM
from llm.llm_facade import LargeLanguageModelFacade
from llm.term_stats import TermStats

class OllamaFacade(LargeLanguageModelFacade):
    def __init__(self, logger: logging.Logger, model: str):
        self.llm = OllamaLLM(model=model)
        self.logger = logger
        self.question_stats = {}

    def relevance(self, question: str, search_result: str) -> float:
        if question not in self.question_stats:
            self.question_stats[question] = TermStats(question)
        rv = self.question_stats[question].similarity(search_result)
        if rv > 0.2:
            return rv
        prompt = """Study the following question and data then return the relevance or likelihood that the supplied data could be used to answer the question. This relevance would be in the form of a floating point number between 0.0 and 1.0 where 0.0 would mean that the data isn't useful at all, 1.0 would indicate that the data is useful with complete certainty, and 0.5 would suggest that the data would just as likely be useful as not. Output as JSON in the specified schema. The response MUST be a valid JSON object and NOTHING else.

**QUESTION**
%s

**DATA**
%s

**SCHEMA**
{
  "relevance": "float"
}
""" % (question, search_result)
        answer = None
        try:
            answer = self.llm.invoke(prompt)
            if not answer:
                self.logger.warning(f"empty response for prompt {prompt}")
                return 0.0
            if answer.startswith('```json'):
                answer = answer[8:-3].strip()
            elif answer.startswith('```'):
                answer = answer[3:-3].strip()
            if not answer.endswith('}'):
                self.logger.warning(f"unexpected response {answer}")
                return 0.0
            result = json.loads(answer)
            if 'relevance' in result:
                rv = float(result['relevance'])
            else:
                self.logger.warning(f"unexpected result format {result}")
        except:
            self.logger.error(f"Error with prompt {prompt}")
            if answer:
                self.logger.error(f"answer is {answer}")
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
            self.logger.error(f"Error with prompt {prompt}")
            return "error with LLM"
