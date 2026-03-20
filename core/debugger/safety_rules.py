from core.models.issue import Issue


class SafetyRules:
    def rapid_in_material(self, segment, line_number):
        if segment.move_type == "G00" and segment.end.z < 0:
            return Issue(
                line_number=line_number,
                message="Rapid move inside material",
                severity="ERROR",
                issue_type="safety"
            )

    def excessive_depth(self, segment, line_number, max_depth=5):
        if segment.end.z < -max_depth:
            return Issue(
                line_number=line_number,
                message=f"Excessive depth: {segment.end.z}",
                severity="WARNING",
                issue_type="safety"
            )