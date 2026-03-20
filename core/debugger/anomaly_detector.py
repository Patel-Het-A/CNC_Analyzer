from core.models.issue import Issue
import math


class AnomalyDetector:
    def large_jump(self, segment, line_number, threshold=100):
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