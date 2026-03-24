from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator
from core.debugger.debugger import Debugger
from core.optimizer.optimizer import Optimizer
from core.visualizer.visualizer import Visualizer
import copy



lines = [
    "G21",
"G90",
"G00 Z10",

"G00 X0 Y20",
"G01 Z-2 F300",
"G01 X10 Y20",
"G01 X10 Y0",
"G01 X5 Y0",
"G01 X5 Y5",
"G00 Z10",

"G00 X15 Y20",
"G01 Z-2",
"G01 X25 Y20",
"G01 X15 Y20",
"G01 X15 Y0",
"G01 X25 Y0",
"G00 Z10",

"G00 X15 Y10",
"G01 Z-2",
"G01 X22 Y10",
"G00 Z10",

"G00 X30 Y20",
"G01 Z-2",
"G01 X40 Y20",
"G01 X30 Y20",
"G01 X30 Y0",
"G01 X40 Y0",
"G00 Z10",

"G00 X30 Y10",
"G01 Z-2",
"G01 X37 Y10",
"G00 Z10",

"G00 X45 Y20",
"G01 Z-2",
"G01 X60 Y20",
"G00 Z10",

"G00 X52.5 Y20",
"G01 Z-2",
"G01 X52.5 Y0",
"G00 Z10",

"M30"
]


tokenizer = Tokenizer()
token_lines = [(tokenizer.tokenize(line), line) for line in lines]

parser = Parser()
commands = parser.parse(token_lines)

resolver = ModalResolver()
commands = resolver.resolve(commands)
scale=commands[0].g_code
if not scale in ["G21","G20"]:
    scale="G21"

print("\n--- commands ---\n")
for cmd in commands:
    print(cmd)

simulator = Simulator()
toolpath = simulator.run(commands)

print("\n--- TOOLPATH ---\n")
for seg in toolpath:
    print(seg)


s=copy.deepcopy(toolpath)

debugger = Debugger()
issues = debugger.run(toolpath)


print("\n--- ISSUES ---\n")
for issue in issues:
    print(issue)

optimizer=Optimizer()
optimized_toolpath=optimizer.run(toolpath)

print("\n---OPTIMIZED TOOLPATH---\n")
for seg in optimized_toolpath:
    print(seg)

print("\n---FEED---\n")
for seg in optimized_toolpath:
    print(f"{seg} | Feed={seg.feed}")

viz = Visualizer()

distance_original=viz.total_distance(s)
distance_optimized=viz.total_distance(optimized_toolpath)
viz.show_3d(s,distance_original,optimized_toolpath,distance_optimized,scale)
