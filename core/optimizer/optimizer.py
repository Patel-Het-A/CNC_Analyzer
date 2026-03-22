from core.optimizer.code_cleaner import CodeCleaner
from core.optimizer.path_optimizer import PathOptimizer


class Optimizer:
    def __init__(self):
        self.path_optimizer = PathOptimizer()

    def run(self, toolpath):

        toolpath = self.path_optimizer.optimize(toolpath)

        return toolpath