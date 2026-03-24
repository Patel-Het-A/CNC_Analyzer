class SuggestionEngine:
    def __init__(self, llm):
        self.llm = llm

    def suggest(self, summary):
        from .prompt_templates import suggest_optimization
        prompt = suggest_optimization(summary)
        return self.llm.generate(prompt)