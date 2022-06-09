"""File for homemode logger"""



class Logger:

    def __init__(self):
        self._trace:bool        =   False
        self._debug:bool        =   False
        self._warning:bool      =   True
        self.buffer:bool        =   True
        self.no_notify:bool     =   False

    def log(self, msg:str, notify:bool = False):
        if notify and not self.no_notify:
            input(msg)
        else:
            print(msg)


    def trace(self, msg:str):

        if self._trace: self.log(f"TRACE:\t{msg}")

    def debug(self, msg:str):

        if self._debug:  self.log(f"DEBUG:\t{msg}")

    def wait(self, newlines:int=0):
        str = "\n"*newlines
        if self.buffer:
            input(str)

    def warning(self, msg:str):

        if self._warning: self.log(f"WARNING:\t{msg}")



log = Logger()