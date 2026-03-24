def explain_gcode(gcode):
    return f"""

Explain this gcode in one line each for every line of gcode.
note that more than one line should not be printed for one line of gcode.
dont print input line.
output format-"line number - Explaination of gcode in one line."


{gcode}
"""

def suggest_optimization(issues):
    return f"""
This are identified issues in input G-Code.
Write suggestions for solving this issues in only one line for each issue object.Note that only one line should be printed and don't print issue object that I am providing you.

Format of output-"line number of faulty line -"ISSUE IN CAPITAL LETTERS" your suggestion response in one line."


{issues}
"""