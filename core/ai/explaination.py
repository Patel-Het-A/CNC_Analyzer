class ExplanationEngine:
    def __init__(self, llm):
        self.llm = llm


    def explain_gcode(self,gcode):
        
        return f"""

        Explain this gcode in one line each for every line of gcode.
        note that more than one line should not be printed for one line of gcode.
        dont print input line.
        output format-"line number-Explaination of gcode in one line."

        {gcode}
        """

    def explain(self, gcode):
        prompt = self.explain_gcode(gcode)


        return self.llm.generate(prompt)