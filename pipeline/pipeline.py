from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator
from core.debugger.debugger import Debugger
from core.optimizer.optimizer import Optimizer
from core.visualizer.visualizer import Visualizer
from core.ai.ai_engine import AIEngine

from pipeline.config import Config

import copy


class CNCPipeline:
    def __init__(self, api_key=None):
        self.config = Config()

        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.resolver = ModalResolver()
        self.simulator = Simulator()
        self.debugger = Debugger()
        self.optimizer = Optimizer()
        self.visualizer = Visualizer()

        self.ai = AIEngine(api_key) if api_key and self.config.ENABLE_AI else None

    def run(self, gcode_lines):
        # -------- TOKENIZE --------
        token_lines = [(self.tokenizer.tokenize(line), line) for line in gcode_lines]

        # -------- PARSE --------
        commands = self.parser.parse(token_lines)
        commands = self.resolver.resolve(commands)

        # -------- SIMULATE --------
        toolpath = self.simulator.run(commands)
        original_toolpath = copy.deepcopy(toolpath)

        # -------- DEBUG --------
        issues = []
        if self.config.ENABLE_DEBUGGING:
            issues = self.debugger.run(toolpath)

        # -------- OPTIMIZE --------
        optimized_toolpath = toolpath
        if self.config.ENABLE_OPTIMIZATION:
            optimized_toolpath = self.optimizer.run(toolpath)

        # -------- METRICS --------
        original_distance = self.visualizer.total_distance(original_toolpath)
        optimized_distance = self.visualizer.total_distance(optimized_toolpath)

        # -------- AI --------
        ai_result = None
        if self.ai:
            ai_result = self.ai.run(gcode_lines, issues)

        return {
            "commands": commands,
            "toolpath": original_toolpath,
            "optimized_toolpath": optimized_toolpath,
            "issues": issues,
            "metrics": {
                "original_distance": original_distance,
                "optimized_distance": optimized_distance
            },
            "ai": ai_result
        }