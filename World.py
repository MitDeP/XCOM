"""Class for state of world"""

class World:


    def __init__(self):

        self.cur_day    =   1
        self.cur_month  =   1
        self.cur_year   =   2022


    def increment_time(self):

        self.cur_day += 1
        
        #NOTE: Just 30 days for all months for now
        if self.cur_day >= 31:
            self.cur_day = 1
            self.cur_month += 1

            if self.cur_month >= 13:
                self.cur_month = 1
                self.cur_year += 1
