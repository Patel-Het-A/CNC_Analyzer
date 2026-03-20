class Command:
    def __init__(
        self,
        line_number: int,
        raw_line: str,
        g_code: str = None,
        m_code: str = None,
        x: float = None,
        y: float = None,
        z: float = None,
        f: float = None,
        s: float = None,
        tool: int = None,
        comment: str = None
    ):
        self.line_number = line_number
        self.raw_line = raw_line

        # Codes
        self.g_code = g_code
        self.m_code = m_code

        # Coordinates
        self.x = x
        self.y = y
        self.z = z

        # Parameters
        self.f = f  # feed rate
        self.s = s  # spindle speed
        self.tool = tool

        # Meta
        self.comment = comment

    def __repr__(self):     
        # modifies the way of printing object
        return (
            f"Command(line={self.line_number}, "
            f"G={self.g_code}, M={self.m_code}, "
            f"X={self.x}, Y={self.y}, Z={self.z}, "
            f"F={self.f}, S={self.s}, T={self.tool})"
        )