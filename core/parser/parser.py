from core.models.command import Command

class Parser:
    def __init__(self):
        pass

    def parse_line(self, tokens, line_number, raw_line):
        #it takes value from tokens and stores it in command object
        data = {}

        for token in tokens:
            key = token[0]  #alphabet e.g 'G' or 'M' etc.
            value = token[1:]  #value of e.g G_code 

            if key in ['G', 'M']:
                data[f"{key.lower()}_code"] = f"{key}{value}"
            elif key in ['X', 'Y', 'Z', 'F', 'S']:
                data[key.lower()] = float(value)
            elif key == 'T':
                data['tool'] = int(value)

        return Command(       
            #command() combines all data in single object in good manner
            line_number=line_number,
            raw_line=raw_line,
            g_code=data.get('g_code'),
            #Here .get() is used to assign None if data["g_code"] is not found 
            m_code=data.get('m_code'),
            x=data.get('x'),
            y=data.get('y'),
            z=data.get('z'),
            f=data.get('f'),
            s=data.get('s'),
            tool=data.get('tool')
        )

    def parse(self, token_lines): 
        #token_lines is list of tuple (tokens,rawline)
        #It is created in main.py by combining tokens(output of tokenize()) & raw line in tuple
        commands = []

        i = 1   #i is current line number

        for item in token_lines:
            tokens = item[0]
            raw_line = item[1]

            if tokens == []:   # if empty line comes
                i += 1
                continue

            cmd = self.parse_line(tokens, i, raw_line)
            commands.append(cmd)

            i += 1

        return commands #this is list of every line's command object