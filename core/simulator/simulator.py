from core.models.machine_state import MachineState
from core.simulator.motion_engine import MotionEngine
from core.simulator.toolpath_generator import ToolpathGenerator
from core.simulator.state_tracker import StateTracker

# motion engine derives toolpath for only one line
# simulator derives toolpath for every lines using motion engine

class Simulator:
    def __init__(self):
        self.state = MachineState()
        self.state_tracker = StateTracker(self.state)
        self.motion_engine = MotionEngine(self.state)
        self.toolpath_generator = ToolpathGenerator()

    def run(self, commands):
        for cmd in commands:
            self.execute_command(cmd)

        return self.toolpath_generator.get_toolpath()

    def execute_command(self, cmd):
        
        self.state_tracker.update(cmd)

        if cmd.g_code in ["G00", "G01"]:
            segment = self.motion_engine.execute_motion(cmd)
            self.toolpath_generator.add_segment(segment)