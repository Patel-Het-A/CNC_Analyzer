class ToolpathGenerator:
    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def get_toolpath(self):
        return self.segments

    def reset(self):
        self.segments = []