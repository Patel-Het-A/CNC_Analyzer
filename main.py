from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator
from core.debugger.debugger import Debugger
from core.optimizer.optimizer import Optimizer

lines = [
    "G21",              # mm
    "G90",              # absolute mode

    # Safe start
    "G00 X0 Y0 Z10",

    # Cutting start
    "G01 Z-2 F300",

    # Normal cutting
    "G01 X20 Y0",
    "G01 X20 Y20",
    "G01 X0 Y20",
    "G01 X0 Y0",

    # Sharp corner (for smoothing)
    "G01 X5 Y0",
    "G01 X5 Y5",

    # Excessive depth (debug)
    "G01 Z-10",

    # Rapid inside material (should be fixed)
    "G00 X50 Y50",

    # Safe move
    "G00 Z15",

    # Large jump (anomaly)
    "G00 X200 Y200",

    # Redundant move
    "G00 X200 Y200",

    # Air cutting (should convert to rapid)
    "G01 X210 Y210",

    # Another cut
    "G01 Z-3",
    "G01 X250 Y250",

    "M30"
]

tokenizer = Tokenizer()
token_lines = [(tokenizer.tokenize(line), line) for line in lines]

parser = Parser()
commands = parser.parse(token_lines)

resolver = ModalResolver()
commands = resolver.resolve(commands)

print("\n--- commands ---\n")
for cmd in commands:
    print(cmd)

simulator = Simulator()
toolpath = simulator.run(commands)

print("\n--- TOOLPATH ---\n")
for seg in toolpath:
    print(seg)

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