class StateTracker:
    def __init__(self, state):
        self.state = state

    def update(self, cmd):
    
        if cmd.g_code == "G90":
            self.state.absolute_mode = True
        elif cmd.g_code == "G91":
            self.state.absolute_mode = False

        if cmd.f:
            self.state.feed_rate = cmd.f

        if cmd.m_code == "M03":
            self.state.spindle_on = True
            if cmd.s:
                self.state.spindle_speed = cmd.s

        elif cmd.m_code == "M05":
            self.state.spindle_on = False
        
        elif cmd.m_code == "M30":
            pass      # program end