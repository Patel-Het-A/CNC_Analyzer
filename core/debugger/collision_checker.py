from core.models.issue import Issue


class CollisionChecker:
    def check(self, segment, line_number):
        if segment.end.z < -50:  
            return Issue(
                line_number=line_number,
                message="Possible collision (too deep)",
                severity="ERROR",
                issue_type="collision"
            )