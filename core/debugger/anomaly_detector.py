from core.models.issue import Issue
from pipeline.config import Config


import math

threshold=Config.LARGE_JUMP_THRESHOLD

class AnomalyDetector:
    def large_jump(self, segment, line_number):
        dx = segment.end.x - segment.start.x
        dy = segment.end.y - segment.start.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist > threshold:
            return Issue(
                line_number=line_number,
                message="Large sudden movement detected",
                severity="WARNING",
                issue_type="anomaly"
            )