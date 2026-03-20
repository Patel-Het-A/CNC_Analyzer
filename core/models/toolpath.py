class ToolpathPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point(X={self.x}, Y={self.y}, Z={self.z})"


class ToolpathSegment:
    def __init__(self, start: ToolpathPoint, end: ToolpathPoint, move_type: str, feed=None):
        self.start = start
        self.end = end
        self.move_type = move_type  # G00 or G01
        self.feed = feed

        # For debugger later
        self.is_cutting = end.z < 0

    def __repr__(self):
        return (
            f"Segment({self.move_type}, "
            f"{self.start} -> {self.end}, "
            f"Cutting={self.is_cutting})"
        )