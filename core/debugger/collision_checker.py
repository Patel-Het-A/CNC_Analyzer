from core.models.issue import Issue
from pipeline.config import Config

COLLISION_DEPTH=Config.COLLISION_DEPTH

class CollisionChecker:
    def check(self, segment, line_number):
        if segment.end.z < -COLLISION_DEPTH:  
            return Issue(
                line_number=line_number,
                message="Possible collision (too deep)",
                severity="ERROR",
                issue_type="collision"
            )