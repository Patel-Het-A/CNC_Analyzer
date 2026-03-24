from .llm_client import LLMClient
from .explaination import ExplanationEngine
from .suggestion import SuggestionEngine
from .strategy_analyzer import StrategyAnalyzer

class AIEngine:

    def __init__(self, api_key):
        llm = LLMClient(api_key)

        self.explainer = ExplanationEngine(llm)
        self.suggester = SuggestionEngine(llm)
        # self.analyzer = StrategyAnalyzer()

    def run(self, gcode, issues):
        explanation = self.explainer.explain(gcode)
        # strategy = self.analyzer.analyze(toolpath)
        suggestion = self.suggester.suggest(issues)

        return {
            "explanation": explanation,
            # "strategy": strategy,
            "suggestion": suggestion
        }