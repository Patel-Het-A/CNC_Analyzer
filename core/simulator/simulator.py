from core.models.machine_state import MachineState
from core.simulator.motion_engine import MotionEngine
from core.simulator.toolpath_generator import ToolpathGenerator
from core.simulator.state_tracker import StateTracker

class Simulator:
    def __init__(self):
        self.toolpath_generator = ToolpathGenerator()

    def run(self, commands):
        # reset everything on every run so repeated API calls don't accumulate state
        state = MachineState()
        self.state_tracker = StateTracker(state)
        self.motion_engine = MotionEngine(state)
        self.toolpath_generator.reset()

        for cmd in commands:
            self.execute_command(cmd)

        return self.toolpath_generator.get_toolpath()

    def execute_command(self, cmd):
        self.state_tracker.update(cmd)

        if cmd.g_code in ["G00", "G01"]:
            segment = self.motion_engine.execute_motion(cmd)
            self.toolpath_generator.add_segment(segment)