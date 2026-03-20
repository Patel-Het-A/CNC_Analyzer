from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator

lines = [
    "G21",
    "G90",
    "G00 X0 Y0 Z5",
    "G01 Z-2 F100",
    "X20 Y0",
    "X20 Y20",
    "X0 Y20",
    "X0 Y0",
    "G00 Z5",
    "M30"
]

tokenizer = Tokenizer()
token_lines = []

for line in lines:
    tokens = tokenizer.tokenize(line)
    token_lines.append((tokens, line))

parser = Parser()
commands = parser.parse(token_lines)

resolver = ModalResolver()
commands = resolver.resolve(commands)

simulator = Simulator()
toolpath = simulator.run(commands)

print("\n--- TOOLPATH OUTPUT ---\n")
for segment in toolpath:
    print(segment)