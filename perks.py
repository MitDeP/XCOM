"""File for all the soldier perks"""

from enum import Enum, auto, IntFlag, unique

#C + P for now
class Perk(IntFlag):

    NONE     = 0

    #Increase hit bonus by 1 each
    MarksmanI   =   auto() #Level 1
    MarksmanII  =   auto() #Level 2
    MarksmanIII =   auto() #Level 4
    MarksmanIV  =   auto() #Level 6
    MarksmanV   =   auto() #Level 9

    Marksman    =   MarksmanI | MarksmanII | MarksmanIII | MarksmanIV | MarksmanV

    #Increases Damage bonus by 1 each
    DeadshotI   =   auto() #Level 1
    DeadshotII  =   auto() #Level 2
    DeadshotIII =   auto() #Level 4
    DeadshotIV  =   auto() #Level 6
    DeadshotV   =   auto() #Level 9

    Deadshot    =   DeadshotI | DeadshotII | DeadshotIII | DeadshotIV | DeadshotV

    #Increase hit die
    ToughnessI  =   auto()  #d6 -> d8   , level 1
    ToughnessII =   auto()  #d8 -> d10  , level 3
    ToughnessIII=   auto()  #d10 -> d12 , level 5

    Toughness   =   ToughnessI | ToughnessII | ToughnessIII

    #Increases crit chance by 1 each
    LethalityI  =   auto()  #level 2
    LethalityII =   auto()  #level 5
    LethalityIII=   auto()  #level 8

    Lethality   =   LethalityI | LethalityII | LethalityIII

    #Increases base hp recovery by 1 each
    RecoveryI   =   auto()  #level 1
    RecoveryII  =   auto()  #level 2
    RecoveryIII =   auto()  #level 4
    RecoveryIV  =   auto()  #level 6
    RecoveryV   =   auto()  #level 8

    Recovery    =   RecoveryI | RecoveryII | RecoveryIII | RecoveryIV | RecoveryV


    #Increases armor score by 1 each
    PlatingI    =   auto()  #level 1
    PlatingII   =   auto()  #level 2
    PlatingIII  =   auto()  #level 4
    PlatingIV   =   auto()  #level 6
    PlatingV    =   auto()  #level 8

    Plating     =   PlatingI | PlatingII | PlatingIII | PlatingIV | PlatingV

    #Increases evasion by 1 each
    EvasiveI    =   auto()  #level 1
    EvasiveII   =   auto()  #level 3
    EvasiveIII  =   auto()  #level 5

    Evasive     =   EvasiveI | EvasiveII | EvasiveIII

    #Increases damage dice
    ArsenalI    =   auto()  #2d4, Shogtun               #level 1
    ArsenalII   =   auto()  #1d10, Sniper Rifle         #level 1
    ArsenalIII  =   auto()  #2d6, Laser Rifle           #level 3
    ArsenalIV   =   auto()  #2d8, Shrapnel Launcher     #level 3
    ArsenalV    =   auto()  #3d6, Laser Cannon          #level 5
    ArsenalVI   =   auto()  #6d4, Plasma Rifle          #level 5
    ArsenalVII  =   auto()  #5d6, Rocket Launcher       #level 8
    ArsenalVIII =   auto()  #4d8, Plasma Cannon         #level 10

    Arsenal     =   ArsenalI | ArsenalII | ArsenalIII | ArsenalIV | ArsenalV | ArsenalVI | ArsenalVII | ArsenalVIII


    #Increases Shields by 1 each
    ShieldingI  =   auto()  #level 5
    ShieldingII =   auto()  #level 5
    ShieldingIII=   auto()  #level 6
    ShieldingIV =   auto()  #level 6
    ShieldingV  =   auto()  #level 7

    Shielding   =   ShieldingI | ShieldingII | ShieldingIII | ShieldingIV | ShieldingV

    #Increases Shield Recharge by one each
    CapacitorI  =   auto()  #level 6
    CapacitorII =   auto()  #level 6
    CapacitorIII=   auto()  #level 7
    CapacitorIV =   auto()  #level 7
    CapacitorV  =   auto()  #level 8

    Capacitor   =   CapacitorI | CapacitorII | CapacitorIII | CapacitorIV | CapacitorV


    #Increases armor class by 2 each
    ArmorerI    =   auto()  #Advanced Kevlar (12)       #level 1
    ArmorerII   =   auto()  #Carbon nanothreads (14)    #level 3
    ArmorerIII  =   auto()  #Plasteel plate (16)        #level 5
    ArmorerIV   =   auto()  #Alien Alloy (18)           #level 8
    ArmorerV    =   auto()  #Void-Eater Metal (20)      #level 10

    Armorer     =   ArmorerI | ArmorerII | ArmorerIII | ArmorerIV | ArmorerV


    #Unit stabilizes and survives if round ends before they bleed out
    DieHardI    =   auto()  #   level 3
    DieHardII   =   auto()  #   level 5
    DieHardIII  =   auto()  #   level 7

    DieHard     =   DieHardI | DieHardII | DieHardIII


    #Unit has resistance to critical hit damage
    CritResistI =   auto()  #   level 3
    CritResistII=   auto()  #   level 5
    CritResistIII=  auto()  #   level 7

    CritResist  =   CritResistI | CritResistII | CritResistIII


    #Unit has ability to use grenades against groups of enemies
    OrdinanceI  =    auto()  #   level 2, frag grenade
    OrdinaceII =    auto()  #   level 5, plasma grenade
    OrdinanceIII=   auto()  #   level 8, plastic explosive
    
    Ordinance   =   OrdinanceI | OrdinaceII | OrdinanceIII

    #Unit has ability to immediately attack back upon being hit
    VengeanceI  =   auto()  #   level 3
    VengeanceII =   auto()  #   level 5
    VengeanceIII=   auto()  #   level 8
    VengeanceIV =   auto()  #   level 10
    
    Vengeance   =   VengeanceI | VengeanceII | VengeanceIII | VengeanceIV


    #Unit has extra explosives
    BlastmasterI    =   auto()  # level 3
    BlastmasterII   =   auto()  # level 6
    BlastmasterIII  =   auto()  # level 9

    Blastmaster     =   BlastmasterI | BlastmasterII | BlastmasterIII


class CharacterClass(Enum):

    Soldier         =   auto()
    Leader          =   auto()
    Psychic         =   auto()
    Sniper          =   auto()
    Heavy           =   auto()
    Medic           =   auto()
    Cyborg          =   auto()
    Demoman         =   auto()
    Juggarnaut      =   auto()


    soldier_default=    Soldier


class LeaderPerks(IntFlag):
    pass

class PsychicPerks(IntFlag):
    pass

class SniperPerks(IntFlag):
    pass

class HeavyPerks(IntFlag):
    pass

class MedicPerks(IntFlag):
    StabilizeI      =   auto()      #Automatic
    """Chance to stabilize 1 bleeding out person on the battlefield"""
    StabilizeII     =   auto()      #Level 9
    """Chance to stabilize up to 2 bleeding out people on the battlefield"""
    StabilizeIII    =   auto()      #Level 14
    """Chance to stabilize up to 3 bleeding out people on the battlefield"""

    

class CyborgPerks(IntFlag):
    Lazarus         =   auto()      #Automatic
    """Unkillable - always stabilizes."""

class DemomanPerks(IntFlag):
    pass

class JuggarnautoPerks(IntFlag):
    IntimidatingI   =   auto()      #Automatic
    """+4 Agro, making this character more likely to get targeted (total +8)"""
    ImtimidatingII  =   auto()      #Level 10
    """+4 Agro, making this character more likely to get targeted (total +12)"""
    ImtimidatingIII =   auto()      #Level 15
    """+4 Agro, making this character more likely to get targeted (total +16)"""
    BulletSpongeI   =   auto()      #Automatic
    """Immediate +30 hp"""
    BulletSpongeII  =   auto()      #Level 8
    """Immediate +30 hp"""
    BulletSpongeIII =   auto()      #Level 12
    """Immediate +30 hp"""