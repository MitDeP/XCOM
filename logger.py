"""File for homemode logger"""



class Logger:

    def __init__(self):
        self._trace:bool        =   False
        self._debug:bool        =   True
        self._warning:bool      =   True
        self.buffer:bool        =   False

    def log(self, msg:str, notify:bool = False):
        if notify:
            input(msg)
        else:
            print(msg)


    def trace(self, msg:str):

        if self._trace: self.log(f"TRACE:\t{msg}")

    def debug(self, msg:str):

        if self._debug:  self.log(f"DEBUG:\t{msg}")

    def wait(self):
        if self.buffer:
            input()

    def warning(self, msg:str):

        if self._warning: self.log(f"WARNING:\t{msg}")



log = Logger()