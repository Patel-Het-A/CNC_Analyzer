class Issue:
    def __init__(
        self,
        line_number: int,
        message: str,
        severity: str = "WARNING",   # INFO/WARNING/ERROR
        issue_type: str = None      
    ):
        self.line_number = line_number
        self.message = message
        self.severity = severity
        self.issue_type = issue_type

    def __repr__(self):
        return (
            f"Issue(line={self.line_number}, "
            f"type={self.issue_type}, "
            f"severity={self.severity}, "
            f"msg='{self.message}')"
        )