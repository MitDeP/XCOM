"""File for battle/fight relate data"""
import random
from sre_parse import State
from typing import List
from enum import Enum, auto
from xml.dom.NodeFilter import NodeFilter

from logger import log
from units import Unit, XCOMSoldier as Soldier, UnitState


class BattleState(Enum):
    NullState       =   auto()
    HumanTurn       =   auto()
    AlienTurn       =   auto()
    HumansWin       =   auto()
    HumansLose      =   auto()

class Battle:


    def __init__(self, humans:list, aliens:list):
        self.humans:List[Soldier]   =   humans
        self.killed_humans:list     =   []
        self.bleeding_out:list      =   []
        self.stabilized:list        =   []
        self.aliens:List[Unit]      =   aliens
        self.battlestate:Enum       =   BattleState.NullState
        self.__survived:list          =   []
        
    def fight(self) -> None:
        self.__fight()

        if any(self.humans):
            log.log(f"Humans win")
            if log._debug:
                for human in self.humans:
                    log.debug(f"\t{human}")
            self.battlestate = BattleState.HumansWin

        elif any(self.aliens):
            log.log(f"Humans lose")
            self.battlestate = BattleState.HumansLose




        

    def __fight(self) -> None:
        """
        Main function for battling
        """

        log.trace(f"Starting fight")

        round:int   =   0
        random.shuffle(self.humans)
        random.shuffle(self.aliens)

        while self.two_sides_remain:
            round += 1
            log.log(f"\n##########\nRound {round}\n##########\n")

            #Buffer list for survivors
            self.__survived.clear()

            #Iterate over all humans
            self.battlestate = BattleState.HumanTurn
            for human in self.humans:
                log.trace(f"It is now {human}'s turn")
                if human.use_ordinance():
                    #TODO: move this code too
                    human.available_ordinance -= 1
                    log.log(f"{human} throws an explosive!")

                    number = 1
                    #TODO: Move this code
                    if len(self.aliens) > 1:
                        rand = sum([random.randint(1,2) for _ in range(2)])
                        number = min(rand, len(self.aliens))

                    targets = random.sample(self.aliens, number)
                    for target in targets:
                        human.attack_with_explosives(target)

                        if not target.alive:
                            self.aliens.remove(target)

                else:

                    target = random.choice(self.aliens)
                    human.attack(target)

                    if not target.alive:
                        self.aliens.remove(target)        
                log.trace(f"Checking state for {human}")
                #finally, put human in proper list
                if human.state == UnitState.Alive:
                    log.debug(f"{human} survived to the next round")
                    self.__survived.append(human)
                elif human.state == UnitState.Dying:
                    log.debug(f"{human} is put into bleeding out")
                    self.bleeding_out.append(human)
                elif human.state == UnitState.Stabilized:
                    log.debug(f"{human} has been put in stabilized")
                    self.stabilized.append(human)
                elif human.state == UnitState.Dead:
                    log.debug(f"{human} has been moved into dead")
                    self.killed_humans.append(human)
                else:
                    log.warning(f"Invalid/unknown state for {human} - {human.state!r}")
                    self.__survived.append(human)

                log.log("", notify=True)

                if not any(self.aliens): return

                

            #Finally, put the humans back in place.
            self.humans = self.__survived.copy()

            #Check if we can quit early
            if not self.two_sides_remain:
                log.debug(f"Only one side remains")
                return

            log.wait()

            log.log("\n=============\nAlien's Turn\n=============\n")
            
            self.__survived.clear()
            self.battlestate.AlienTurn
            for alien in self.aliens:
                #TODO: put alien combat code here
                if alien.use_ordinance():
                    #TODO: move this code too
                    alien.available_ordinance -= 1
                    log.log(f"{alien} throws an explosive!")

                    number = 1
                    #TODO: Move this code
                    if len(self.aliens) > 1:
                        rand = sum([random.randint(1,2) for _ in range(2)])
                        number = min(rand, len(self.humans))

                    targets = random.sample(self.humans, number)
                    for target in targets:
                        human.attack_with_explosives(target)

                        if target.is_bleeding_out:
                            self.humans.remove(target)
                            self.bleeding_out.append(target)

                        elif not target.alive:
                            self.humans.remove(target)
                            self.killed_humans.append(target)



                else:

                    target = random.choice(self.humans)
                    alien.attack(target)

                    if target.is_bleeding_out:
                            self.humans.remove(target)
                            self.bleeding_out.append(target)

                    elif not target.alive:
                        self.humans.remove(target)
                        self.killed_humans.append(target)

                if alien.state  ==  UnitState.Alive:
                    log.debug(f"{alien} has survived to next round")
                    self.__survived.append(alien)

                elif alien.state == UnitState.Dead:
                    log.debug(f"{alien} is dead. Nothing to do")
                    #Currently don't need to track dead aliens. Let them go away
                
                else:
                    log.warning(f"Invalid/Unknown state for {alien} - {alien.state!r}")
                    self.__survived.append(alien)

                log.log("",notify=True)

                if not self.two_sides_remain: return

            self.aliens = self.__survived.copy()
            self.__survived.clear()


            #Again, see if we can leave early.

            #TODO Process status effects

            for dying in self.bleeding_out:

                dying.bleedout_timer -= 1

            



            

            

    
    @property
    def two_sides_remain(self) -> bool:
        """Function for testing if two sides are still fighting"""
        return any(self.humans) and any(self.aliens)


    @property
    def humans_win(self) -> bool:
        """TODO"""

        if self.battlestate == BattleState.NullState:
            log.warning(f"Request for winner occurred before battle occured, or battle did not conclude properly")


        return self.battlestate != BattleState.HumansLose 

class BattleSeries:


    def __init__(self, humans:list, alien_list):

        self.humans = humans
        self.battle_list = alien_list
        self.last_battle = None
        self.humans_heal_between_battles:bool       =   True
        self.humans_level_between_battles:bool      =   True
        self.humans_kia:list =   []



    def run(self):
        """TODO"""

        for battle_no, enemy_list in enumerate(self.battle_list, start=1):
            bat = Battle(self.humans, enemy_list)
            self.last_battle = bat
            log.log(f"Battle {battle_no}", notify=True)
            bat.fight()

            self.humans_kia += bat.killed_humans
            self.humans = bat.humans

            if not bat.humans_win:
                log.log(f"\nHumanity has been defeated!\n", notify=True)
                return
            else:
                log.log(f"\nThe humans are victorious!\n", notify=True)

            if self.process_between_battles:
                for human in self.humans:

                    if self.humans_heal_between_battles:
                        human.rest()

                    if self.humans_level_between_battles:
                        human.check_for_level_up()


    @property
    def process_between_battles(self) -> bool:
        return self.humans_heal_between_battles \
        or self.humans_level_between_battles
