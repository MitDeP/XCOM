class Unit:

    """Base Unit Class"""


    def __init__(self, name:str):
        self.name:str           =       name




class XCOMSoldier(Unit):

    """Class for an xcom soldier"""

    def __init__(self, name:str):

        super(XCOMSoldier, self).__init__(name)
