class StrategyAnalyzer:
    def analyze(self, toolpath):
        total_moves = len(toolpath)
        cutting = sum(1 for s in toolpath if s.move_type == "G01")

        return {
            "total_moves": total_moves,
            "cutting_moves": cutting,
            "efficiency": cutting / total_moves if total_moves else 0
        }