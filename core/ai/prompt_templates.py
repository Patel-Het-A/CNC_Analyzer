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


Note for incremental mode 'G91' you dont need to move to specified coordinates instead specified X,Y,Z values tells that you need to move that much amount of steps in specified direction so calculate coordinates of tool after increment and show that with your explanation.

if issues is empty then return No critical issues are found.

Format of output-"line number of faulty line -"ISSUE IN CAPITAL LETTERS" your suggestion response in one line."


{issues}
"""