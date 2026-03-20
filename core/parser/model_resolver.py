class ModalResolver:
    #handles cases where G_code=None in line & updates with previous line value
    def __init__(self):
        self.last_g_code = None

    def resolve(self, commands):
        resolved_commands = []

        for cmd in commands: 
          
            if cmd.g_code: # when G_code!=None 
                self.last_g_code = cmd.g_code
            else:
                
                cmd.g_code = self.last_g_code

            resolved_commands.append(cmd)

        return resolved_commands