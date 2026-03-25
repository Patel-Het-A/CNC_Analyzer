from core.debugger.safety_rules import SafetyRules
from core.debugger.collision_checker import CollisionChecker
from core.debugger.anomaly_detector import AnomalyDetector

class Debugger:
    def __init__(self):
        self.issues = []
        self.safety = SafetyRules()
        self.collision = CollisionChecker()
        self.anomaly = AnomalyDetector()

    def run(self, toolpath):
        self.issues = []  # reset on every run

        for i in range(len(toolpath)):
            segment = toolpath[i]
            prev_segment = toolpath[i - 1] if i > 0 else None
            self.apply_rules(segment, segment.line_number, prev_segment)

        return self.issues

    def apply_rules(self, segment, line_number, prev_segment):
        checks = [
            self.safety.rapid_in_material(segment, line_number),
            self.safety.excessive_depth(segment, line_number),
            self.collision.check(segment, line_number),
            self.anomaly.large_jump(segment, line_number),
            self.safety.missing_feed(segment, line_number),
            self.safety.missing_retract(segment, prev_segment, line_number)
        ]

        for issue in checks:
            if issue:
                self.issues.append(issue)