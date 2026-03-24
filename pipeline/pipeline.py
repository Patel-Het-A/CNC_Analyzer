from core.parser.tokenizer import Tokenizer
from core.parser.parser import Parser
from core.parser.modal_resolver import ModalResolver
from core.simulator.simulator import Simulator
from core.debugger.debugger import Debugger
from core.optimizer.optimizer import Optimizer
from core.visualizer.visualizer import Visualizer
from core.ai.ai_engine import AIEngine

from pipeline.config import Config
from utils.metrics import Metrics

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
        self.metrics = Metrics()

        self.ai = AIEngine(api_key) if api_key and self.config.ENABLE_AI else None

    def run(self, gcode_lines):
        
        token_lines = [(self.tokenizer.tokenize(line), line) for line in gcode_lines]

        commands = self.parser.parse(token_lines)
        commands = self.resolver.resolve(commands)

        toolpath = self.simulator.run(commands)
        original_toolpath = copy.deepcopy(toolpath)

        issues = []
        if self.config.ENABLE_DEBUGGING:
            issues = self.debugger.run(toolpath)

        optimized_toolpath = toolpath
        if self.config.ENABLE_OPTIMIZATION:
            optimized_toolpath = self.optimizer.run(toolpath)

        original_metrics = self.metrics.calculate(original_toolpath)
        optimized_metrics = self.metrics.calculate(optimized_toolpath)
        improvement=((original_metrics["total"]-optimized_metrics["total"])/original_metrics["total"])*100
        improvement=round(improvement,2)
        ai_result = None
        if self.ai:
            ai_result = self.ai.run(gcode_lines, issues)

        return {
            "commands": commands,
            "toolpath": original_toolpath,
            "optimized_toolpath": optimized_toolpath,
            "issues": issues,
            "metrics": {
                "original": original_metrics,
                "optimized": optimized_metrics,
                "improvemnt":improvement
            },
            "ai": ai_result
        }