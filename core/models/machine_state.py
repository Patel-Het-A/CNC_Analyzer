class MachineState:
    def __init__(self):
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        
        self.absolute_mode = True  
        self.units = "mm"           

        
        self.feed_rate = None
        self.spindle_on = False
        self.spindle_speed = None

        
        self.current_tool = None

    def update_position(self, x=None, y=None, z=None):
        if self.absolute_mode:
            if x is not None:
                self.x = x
            if y is not None:
                self.y = y
            if z is not None:
                self.z = z
        else:
            if x is not None:
                self.x += x
            if y is not None:
                self.y += y
            if z is not None:
                self.z += z

    def __repr__(self):
        return (
            f"MachineState(X={self.x}, Y={self.y}, Z={self.z}, "
            f"Mode={'G90' if self.absolute_mode else 'G91'}, "
            f"Units={self.units}, Spindle={'ON' if self.spindle_on else 'OFF'})"
        )