from core.models.issue import Issue
from pipeline.config import Config

Z_safe=Config.SAFE_Z
max_depth=Config.MAX_DEPTH


class SafetyRules:
    def rapid_in_material(self, segment, line_number):
        if segment.move_type == "G00" and segment.end.z < Z_safe:
            if segment.end.z<0:
                return Issue(
                    line_number=line_number,
                    message="Rapid move inside material",
                    severity="ERROR",
                    issue_type="safety"
                )
            else:
                return Issue(
                    line_number=line_number,
                    message="Rapid move below safe height",
                    severity="WARNING",
                    issue_type="safety"
                )


    def excessive_depth(self, segment, line_number):
        if segment.end.z < -max_depth:
            return Issue(
                line_number=line_number,
                message=f"Excessive depth: {segment.end.z}",
                severity="WARNING",
                issue_type="safety"
            )
        
    
    def missing_feed(self, segment, line_number):
        if segment.move_type == "G01" and segment.feed is None:
            return Issue(
                line_number=line_number,
                message="Missing feed rate for cutting",
                severity="WARNING",
                issue_type="process"
            )
        
    def missing_retract(self, segment, prev_segment, line_number):
        if prev_segment and prev_segment.end.z < 0:
            if segment.move_type == "G00" and segment.start.z < Z_safe:
                return Issue(
                    line_number=line_number,
                    message="No safe retract before rapid move",
                    severity="WARNING",
                    issue_type="safety"
                )
            
        