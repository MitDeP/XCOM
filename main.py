import sys

from logger import log
from units import humans
from battling import Battle, BattleSeries
from aliens import all_battles

def main():

    version = 'old'
    
    if version == 'old':

        for battle in all_battles:
            bs = BattleSeries(humans, battle)
            bs.run()

            if bs.humans_defeated:
                print("Game over")
                return
            
        print("You win!")





        
        
                





if __name__ == "__main__":
    main()