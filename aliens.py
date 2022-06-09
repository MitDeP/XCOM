from asyncio import shield
from enum import Enum, IntFlag, auto
from typing import final

from webob import second

from units import Unit as Alien
from items import wep_allopew_rifle

import alien_data

difficulty = alien_data.Difficulty.Normal


class AllopewPirate(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.allopew_pirate_dict[difficulty]

        super(AllopewPirate, self).__init__("Allopew Pirate", **data_dict, id=id)

class AllopewRaider(Alien):

    def __init__(self, id=None):
        data_dict = alien_data.allopew_raider_dict[difficulty]

        super(AllopewRaider, self).__init__("Allopew Raider", **data_dict,id = id)

class AllopewBuckaneer(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.allopew_buckaneer_dict[difficulty]

        super(AllopewBuckaneer, self).__init__("Allopew Buckaneer", **data_dict, id=id)

class AllopewRobber(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.allopew_robber_dict[difficulty]

        super(AllopewRobber, self).__init__("Allopew Robber", **data_dict,id = id)

class AllopewWarlord(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.allopew_warlord_dict[difficulty]

        super(AllopewWarlord, self).__init__("Allopew Warlord", **data_dict, id=id)

class AllopewCaptain(Alien):

    def __init__(self, id=None):
        data_dict = alien_data.allopew_captain_dict[difficulty]

        super(AllopewCaptain, self).__init__("Allopew Captain", **data_dict, id=id)


class AllopewKing(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.allopew_king_dict[difficulty]

        super(AllopewKing, self).__init__("Allopew King", **data_dict, id=id)


class PraxSoldier(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prax_soldier_dict[difficulty]

        super(PraxSoldier, self).__init__("Prax Soldier", **data_dict, id = id)

class PraxLieutenant(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prax_lieutenant_dict[difficulty]

        super(PraxLieutenant, self).__init__("Prax Lieutenant", **data_dict, id = id)

class PraxCaptain(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prax_captain_dict[difficulty]

        super(PraxCaptain, self).__init__("Prax Captain", **data_dict, id = id)


class PraxCommando(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prax_commando_dict[difficulty]

        super(PraxCommando, self).__init__("Prax Commando", **data_dict, id=id)


class PraxSpecops(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prax_specops_dict[difficulty]

        super(PraxSpecops, self).__init__("Prax Specops", **data_dict, id=id)

class Prex(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.prex_oppressor_dict[difficulty]

        super(Prex, self).__init__("Prex Oppressor", **data_dict, id=id)

class BethnekiDrone(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_drone_dict[difficulty]

        super(BethnekiDrone, self).__init__("Bethneki Drone", **data_dict, id=id)

class BethnekiRobot(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_robot_dict[difficulty]

        super(BethnekiRobot, self).__init__("Bethneki Robot", **data_dict, id=id)

class BethnekiScout(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_scout_dict[difficulty]

        super(BethnekiScout, self).__init__("Bethneki Scout", **data_dict, id=id)

class BethnekiResearcher(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_researcher_dict[difficulty]

        super(BethnekiResearcher, self).__init__("Bethneki Researcher", **data_dict, id=id)

class BethnekiGuerrilla(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_guerrilla_dict[difficulty]

        super(BethnekiGuerrilla, self).__init__("Bethneki Guerrilla", **data_dict, id=id)

class BethnekiAssassin(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_assassin_dict[difficulty]

        super(BethnekiAssassin, self).__init__("Bethneki Assassin", **data_dict, id=id)

class BethnekiMech(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.bethneki_mech_dict[difficulty]

        super(BethnekiMech, self).__init__("Bethneki Mech", **data_dict, id=id)

class UltranusTrooper(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.ultranus_trooper_dict[difficulty]

        super(UltranusTrooper, self).__init__("Ultranus Trooper", **data_dict, id=id)

class UltranusStormtrooper(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.ultranus_stormtrooper_dict[difficulty]

        super(UltranusStormtrooper, self).__init__("Ultranus Stormtrooper", **data_dict, id=id)

class UltranusTank(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.ultranus_tank_dict[difficulty]

        super(UltranusTank, self).__init__("Ultranus Tank", **data_dict, id=id)

class VoidThrall(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.void_thrall_dict[difficulty]

        super(VoidThrall, self).__init__("Void Thrall", **data_dict, id=id)

class VoidEater(Alien):

    def __init__(self, id=None):

        data_dict = alien_data.void_eater_dict[difficulty]

        super(VoidEater, self).__init__("Void Eater", **data_dict, id=id)



def alien_factory(request_dictionary) -> list:
    """TODO"""

    aliens = []

    for alien_cls, number in request_dictionary.items():

       #alien_info_dict = alien_dict.get(alien_type)
    

        for i in range(number):
            aliens.append(alien_cls(id=i+1))
            #aliens.append(Alien.from_dictionary(alien_info_dict, id=i+1))

    return aliens


def setup_battles(battle_list:list) -> list:
    """TODO"""

    battles:list = []

    for battle_dict in battle_list:
        battles.append(alien_factory(battle_dict))

    return battles




allopew_battles = [
    {AllopewPirate : 4},

    {AllopewPirate : 4,
    AllopewRaider : 2},

    {AllopewPirate : 4,
    AllopewRaider : 1,
    AllopewBuckaneer : 1},

    {AllopewPirate : 8,
    AllopewRaider : 2,
    AllopewBuckaneer : 2},

    {AllopewPirate : 5,
    AllopewRaider : 2,
    AllopewBuckaneer : 2,
    AllopewWarlord : 1},

    {AllopewPirate : 5,
    AllopewRaider : 1,
    AllopewBuckaneer : 2,
    AllopewRobber : 1},

    {AllopewPirate : 6,
    AllopewRaider : 3,
    AllopewBuckaneer : 3,
    AllopewWarlord : 2, 
    AllopewKing : 1},

    {AllopewRaider : 12,
    AllopewRaider : 5},


]

prax_battles = [
    {PraxSoldier : 3},
    
    {PraxSoldier : 4, 
    PraxLieutenant : 1},

    {PraxSoldier : 6,
    PraxLieutenant : 1},

    {PraxSoldier : 4,
    PraxCaptain : 1},

    {PraxSpecops : 2},

    {PraxSoldier : 6,
    PraxLieutenant : 2},

    {PraxSoldier : 4,
    PraxCaptain : 1},

    {PraxSoldier : 6,
    PraxCommando : 1},

    {PraxSoldier : 4,
    PraxSpecops : 2},

    {PraxSoldier : 4,
    PraxLieutenant : 2,
    PraxCaptain : 1,
    Prex : 1},

    {PraxSoldier : 6},

    {PraxLieutenant : 2,
    PraxCaptain  : 1},

    {PraxCommando : 2}

]

bethneki_battles = [
    {BethnekiScout : 3,
    BethnekiRobot : 2},

    {BethnekiScout : 3,
    BethnekiRobot : 2,
    BethnekiResearcher : 1,
    BethnekiDrone : 1},

    {BethnekiScout : 3,
    BethnekiRobot : 1,
    BethnekiResearcher : 3,
    BethnekiDrone : 1},

    {BethnekiDrone : 10,
    BethnekiRobot : 4},

    {BethnekiResearcher : 3,
    BethnekiDrone : 1},

    {BethnekiResearcher : 1,
    BethnekiDrone : 3,
    BethnekiGuerrilla : 2},

    {BethnekiDrone : 3,
    BethnekiGuerrilla : 3,
    BethnekiAssassin : 1},

    {BethnekiGuerrilla : 4,
    BethnekiDrone : 4,
    BethnekiAssassin : 2},

    {BethnekiGuerrilla : 3,
    BethnekiAssassin : 1,
    BethnekiDrone : 6,
    BethnekiMech : 1},
]

ultranus_battles = [
    {UltranusTrooper : 3},
    
    {UltranusTrooper : 5},

    {UltranusTrooper : 2,
    UltranusStormtrooper : 1},

    {UltranusTrooper : 6},

    {UltranusTrooper : 2, 
    UltranusStormtrooper : 2},

    {UltranusStormtrooper : 4,
    UltranusStormtrooper : 1},

    {UltranusTrooper : 2,
    UltranusTank : 1}
]


void_battles = [
    {VoidEater : 1}
]

first_battles = setup_battles(allopew_battles)

second_battles = setup_battles(prax_battles)

third_battles = setup_battles(bethneki_battles)

fourth_battles = setup_battles(ultranus_battles)

final_battles = setup_battles(void_battles)


all_battles = [first_battles, second_battles, third_battles, fourth_battles, final_battles]