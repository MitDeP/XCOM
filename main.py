import sys

from logger import log
from units import humans
from battling import Battle, BattleSeries
from aliens import first_battles

def main():

    version = 'old'
    
    if version == 'old':


        b1 = BattleSeries(humans, first_battles)
        b1.run()
        
        
                





if __name__ == "__main__":
    main()