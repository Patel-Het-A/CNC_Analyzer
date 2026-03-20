import re

class Tokenizer:
    def __init__(self):
        pass

    def remove_comments(self, line: str):
       
        line = re.sub(r"\(.*?\)", "", line)
        line = re.sub(r";.*", "", line)
        return line.strip()

    def tokenize(self, line: str):
        line = line.upper()
        line = self.remove_comments(line)

        if not line:
            return []

        
        tokens = re.findall(r"[A-Z][-\d\.]+", line)

        return tokens