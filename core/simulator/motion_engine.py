from core.models.toolpath import ToolpathPoint, ToolpathSegment

class MotionEngine:
    def __init__(self, state):
        self.state = state

    def execute_motion(self, cmd):
        
        start = ToolpathPoint(self.state.x, self.state.y, self.state.z)

        self.state.update_position(cmd.x, cmd.y, cmd.z)

        end = ToolpathPoint(self.state.x, self.state.y, self.state.z)

    
        segment = ToolpathSegment(
            start=start,
            end=end,
            move_type=cmd.g_code,
            feed=cmd.f or self.state.feed_rate
        )

        return segment