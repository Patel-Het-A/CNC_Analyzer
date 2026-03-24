def load_gcode_file(path):
    """
    Load G-code file and return list of lines
    """
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]