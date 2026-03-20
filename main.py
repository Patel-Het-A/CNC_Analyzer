from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator
from core.debugger.debugger import Debugger

lines = [
    "G21",
    "G90",
    "G00 X0 Y0 Z5",
    "G01 Z-10 F100",   
    "G00 X50 Y50",    
    "G01 X200 Y200",   
    "M30"
]

tokenizer = Tokenizer()
token_lines = [(tokenizer.tokenize(line), line) for line in lines]

parser = Parser()
commands = parser.parse(token_lines)

resolver = ModalResolver()
commands = resolver.resolve(commands)

simulator = Simulator()
toolpath = simulator.run(commands)

debugger = Debugger()
issues = debugger.run(toolpath)

print("\n--- commands ---\n")
for cmd in commands:
    print(cmd)

print("\n--- TOOLPATH ---\n")
for seg in toolpath:
    print(seg)

print("\n--- ISSUES ---\n")
for issue in issues:
    print(issue)