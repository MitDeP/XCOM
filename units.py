import random
from enum import Enum, auto, IntFlag, unique
import math
from re import S

from items import Weapon, wep_assault_rifle, wep_shotgun, wep_laser_cannon, wep_laser_rifle, wep_plasma_cannon, wep_plasma_rifle, wep_rocket_launcher, wep_shrapnel_gun, wep_sniper, wep_void_gun
from logger import log
from perks import Perk

@unique
class UnitState(Enum):
    Alive       =   auto()
    Stabilized  =   auto()
    Dying       =   auto()
    Dead        =   auto()


@unique
class KillMethod(Enum):
    Normal      =   auto()
    Retaliation =   auto()
    Explosive   =   auto()



class Unit:

    """Base Unit Class"""

    number_dice_for_attack:int  =   3
    """Number of dice used to roll for an attack roll"""
    attack_dice_type:int        =   6
    """Kind of dice used to roll (e.g., 6 would be a d6)"""
    crit_level_table:list       =   [
        10,          #  10/1000  ( 1.0%)
        50,          #  50/1000  ( 5.0%)
        100,         # 100/1000  (10.0%)
        145,         # 145/1000  (14.5%)
        180,         # 180/1000  (18.0%)
        200,         # 200/1000  (20.0%)
        210,         # 210/1000  (21.0%)
        215,         # 215/1000  (21.5%)
        220,         # 220/1000  (22.0%)
        225,         # 225/1000  (22.5%)
        228,         # 228/1000  (22.8%)
        230,         # 230/1000  (23.0%)
    ]

    standard_crit_multiplier:float = 2.5


    def __init__(self, name:str, max_hit_points:int=1, armor_class:int=10, attack_bonus:int=0, weapon:Weapon=None, armor:int=0, will:int=0, max_shields:int=0,
    shield_regen:int = 0, evasion:int = 0, crit_level:int = 0, crit_resist:int = 0, number_explosives:int = 0, ordinance_level:int = 0, agro:int = 4,
    cost:int = 10_000, proficiency:int=0, retaliation_chance:int = 0, hit_die_type:int = 0, num_hit_dice:int = 0, damage_bonus:int = 0, custom_weapon:tuple = None):
        self.name:str               =   name
        self.max_hit_points:int     =   max_hit_points
        self.cur_hit_points:int     =   max_hit_points
        self.armor_class:int        =   armor_class
        self.attack_bonus:int       =   attack_bonus
        self.damage_bonus:int       =   damage_bonus
        self.weapon:Weapon          =   weapon
        self.armor:int              =   armor
        self.will:int               =   will                                #Unused in old engine
        self.max_shields:int        =   max_shields
        self.cur_shields:int        =   max_shields
        self.shield_regen:int       =   shield_regen
        self.evasion:int            =   evasion
        self.crit_level:int         =   crit_level
        self.crit_chance:int        =   Unit.crit_level_table[crit_level]
        self.crit_resist:int        =   crit_resist
        self.max_ordinance:int      =   number_explosives
        self.available_ordinance:int=   number_explosives
        self.ordinance_level:int    =   ordinance_level
        self.agro:int               =   agro                                #Unused in old engine
        self.cost:int               =   cost                                #TODO move to own alien class
        self.proficiency:int        =   proficiency
        self.retaliation_chance:int =   retaliation_chance
        self.hit_die_type:int       =   hit_die_type
        self.num_hit_dice:int       =   num_hit_dice
        self.id                     =   None                #Aliens only

        self.state:UnitState        =   UnitState.Alive


        if custom_weapon and not weapon:
            self.weapon = Weapon("Custom Weapon", custom_weapon[0], custom_weapon[1], custom_weapon[2])


        #Stat Tracking
        self.damage_taken:int       =   0
        self.damage_dealt:int       =   0
        self.kills:int              =   0
        self.shots_taken:int        =   0
        self.shots_hit:int          =   0

    @classmethod
    def from_dictionary(cls, dictionary:dict, id:int=None):
        alien = cls(**dictionary)

        if id: alien.id = id

        return alien

    def damage_callback(self, inflictor) -> None:
        """Function called whenever the unit is damaged"""

        self.update_state()

    def use_ordinance(self) -> bool:
        return random.randint(1, 20) <= self.ordinance_level+self.available_ordinance*2 and self.available_ordinance >= 1

    def hit_callback(self) -> None:
        self.shots_hit += 1

    def kill_callback(self, kill_method:Enum = KillMethod.Normal) -> None:
        self.kills += 1

    def damage(self, inflictor, amount:int, is_crit:bool):
        log.debug(f"{self} is getting damage by {inflictor} for {amount} raw damage")

        damage_dealt:int    = amount

        if is_crit:
            crit_mult:float = Unit.standard_crit_multiplier

            #get the bigger number, so if somehow the crit would do *less* damage
            #   than the normal attack, normal damage is done instead
            crit_mult -= max(0.25*self.crit_resist, 1.0)

            if crit_mult > 1.0:
                #Don't anounce crit for no bonus
                log.log(f"{inflictor} scores a critical hit for {crit_mult}x damage!")

                damage_dealt = math.ceil(damage_dealt*crit_mult)

        #No evading a critical hit
        evades = random.randint(1,12) <= self.evasion and not is_crit

        if evades:
            log.log(f"{self} is merely skimmed by the attack!")
            damage_dealt = math.ceil(damage_dealt/2.0)

        #add the amount of raw damage done to inflictor's record
        inflictor.damage_dealt += damage_dealt

        if self.cur_shields:
            self.cur_shields -= amount
            
            #check if shields broke, take absoulte value of them to figure
            #   out how much damage was done
            if self.cur_shields <= 0:
                damage_dealt = abs(self.cur_shields)
                self.cur_shields = 0
                log.log(f"{self}'s shields were broken!")
            else:
                print(f"The attack weakened {self}'s shields ({self.cur_shields}/{self.max_shields})")
                damage_dealt = 0



        if damage_dealt:

            #Armor is applied last since any damage at this point will do
            #    a minimum of 1 damage
            if self.armor:
                print(f"{self}'s armor blocks {self.armor} damage")
                damage_dealt -= self.armor
                if damage_dealt <= 0:
                    damage_dealt = 1

            
            self.cur_hit_points -= damage_dealt
            self.damage_taken += damage_dealt

            log.log(f"{inflictor} attacked {self} for {damage_dealt} damage ({self.cur_hit_points}/{self.max_hit_points})")
            self.damage_callback(inflictor)
            #TODO: Have damage callback check for retaliation

            if self.conscious:

                retaliate  = random.randint(1,12) <= self.retaliation_chance and inflictor.alive

                if retaliate:
                    log.log(f"{self} retaliates against {inflictor}!")
                    self.attack(inflictor)

    def update_state(self):
        """Function for udpdating this unit's state"""
        previous_state = self.state
        if self.cur_hit_points < 1:
            self.state = UnitState.Dead

        if previous_state != self.state:
            log.debug(f"{self}'s state updated: {previous_state.name} ==> {self.state.name}") 
                
    def between_turn_update(self):
        """Function for processing each unit between turns"""
        

        #NOTE: old engine has it's own function. May want to change so this
        #   one does too, later
        if any(self.shield_regen):
            self.cur_shields += self.shield_regen
            if self.cur_shields >= self.max_shields:
                self.cur_shields = self.max_shields
                log.log(f"{self}'s shields recharge to full! ({self.cur_shields}/{self.max_shields})")
            else:
                log.log(f"{self}'s shields recharge by {self.shield_regen} ({self.cur_shields}/{self.max_shields})")

    def attack(self, target):
        """Function for making a standard attack against another target"""

        log.log(f"{self} attacks {target}")

        attack_roll = self.roll_to_attack()

        log.debug(f"{self}'s {attack_roll} vs {target}'s {target.armor_class}")

        if attack_roll >= target.armor_class:
            self.shots_hit += 1
            damage_amount:int = self.weapon.roll_damage(self.proficiency + self.damage_bonus)

            is_crit:bool    = random.randint(1, 1000) <= self.crit_chance

            target.damage(self, damage_amount, is_crit)

            if not target.conscious:

                if not target.alive:
                    log.log(f"{self} kills {target}")
                    self.kill_callback(kill_method=KillMethod.Normal)

                else:
                    log.log(f"{self} knocks {target} unconscious") 

        else:
            log.log(f"{self} misses {target}")

    def attack_with_explosives(self, target):

        damage_amount:int = self.roll_explosives_damage()

        target.damage(self, damage_amount, False)

        if target.is_bleeding_out:
            self.kill_callback(kill_method=KillMethod.Explosive)
            log.log(f"{self} knocks {target} unconscious")

        elif not target.alive:
            self.kill_callback(kill_method=KillMethod.Explosive)
            log.log(f"{self} kills {target} with a explosive")

    def refresh(self):
        """Function for resetting a unit's hit points to max, 
        as well as shields and their available ordinance"""

        self.cur_hit_points = self.max_hit_points
        self.cur_shields    = self.max_shields
        self.available_ordinance=self.max_ordinance

    def roll_explosives_damage(self):
        #TODO improve, document

        die, num = 1, 1

        if self.ordinance_level == 1:
            die, num = 6, 2

        elif self.ordinance_level == 2:
            die, num = 6, 3

        elif self.ordinance_level == 3:
            die, num = 6, 4

        return sum([random.randint(1, die) for _ in range(num)])

    def heal(self, amount:int):
        """Function for healing damage to a unit"""
        if self.cur_hit_points == self.max_hit_points: return

        self.cur_hit_points += amount
        if self.cur_hit_points >= self.max_hit_points:
            self.cur_hit_points = self.max_hit_points
            log.log(f"{self} recovered {amount} and is back up to full hit points ({self.max_hit_points}/{self.max_hit_points})")
        else:
            log.log(f"{self} has recovered {amount} hit points ({self.cur_hit_points}/{self.max_hit_points})")
        
    def roll_to_attack(self) -> int:
        """Rolls for an attack."""
        return sum([random.randint(1, Unit.attack_dice_type) for _ in range(Unit.number_dice_for_attack)]) + self.attack_bonus + self.proficiency

    @property
    def conscious(self) -> bool:
        """Property if unit is conscious. Will return false if unit is
        dead, bleeding out, or stabilized"""
        return self.state == UnitState.Alive

    
    @property
    def is_bleeding_out(self) -> bool:
        return self.state == UnitState.Dying


    @property
    def alive(self) -> bool:
        """Returns if the Unit is alive"""
        return self.state != UnitState.Dead


    @property
    def accuracy(self) -> float:
        return round((self.shots_hit/self.shots_taken)*100,2)



    def __str__(self) -> str:
        name = f"{self.name}"

        if self.id:
            name += f" {self.id}"

        return name


class XCOMSoldier(Unit):

    """Class for an xcom soldier"""

    base_exp_requirement:int        =   1
    base_exp_increment:int          =   4
    exp_level_mult:float            =   1.25
    max_level:int                   =   20
    proficiency_bonus_table:list    =   [3, 6, 9, 12, 15, 18]


    #exp rates
    exp_get_hit:int     =   1
    exp_wound:int       =   2
    exp_kill:int        =   4
    exp_kill_explosive:int= 1
    perks_per_level:int =   2

    def __init__(self, name:str):

        super(XCOMSoldier, self).__init__(name, max_hit_points=6, armor_class=10, weapon = wep_assault_rifle, num_hit_dice=1, hit_die_type=4)
        self.perk_flags:Perk            =       Perk.NONE
        self.bleedout_timer:int         =       0
        self.max_bleedout:int           =       0
        self.recovery_bonus:int         =   0
        self.exp:int                    =       0
        self.level:int                  =       1
        self.next_level_requirement:int =       XCOMSoldier.base_exp_requirement


    def update_state(self):
        """overriden state update function specifically for soldiers"""
        previous_state = self.state
        if self.cur_hit_points < 1 and self.max_bleedout and self.bleedout_timer > 0:
            self.bleedout_timer = self.max_bleedout
            self.state = UnitState.Dying

        elif self.cur_hit_points < 1:
            self.state = UnitState.Dead

        if previous_state != self.state:
            log.debug(f"{self}'s state updated: {previous_state.name} ==> {self.state.name}")

    def rest(self) -> None:
        """TODO"""

        self.cur_shields = self.max_shields
        self.available_ordinance = self.max_ordinance
        
        hp_restore = sum([random.randint(1,self.hit_die_type) for _ in range(self.num_hit_dice)]) + self.recovery_bonus
        self.heal(hp_restore)

    def hit_callback(self) -> None:
        self.exp += XCOMSoldier.exp_wound
        return super().hit_callback()

    def kill_callback(self, kill_method:Enum) -> None:

        if kill_method == KillMethod.Normal:
            self.exp += XCOMSoldier.exp_kill

        elif kill_method == KillMethod.Explosive:
            self.exp += XCOMSoldier.exp_kill_explosive

        else:
            log.warning(f"Invalid/Unhandled killmethod for Soldier - {kill_method!r}")

        return super().kill_callback()

    def damage_callback(self, inflictor) -> None:
        """Partially overriden damage callback for soldiers, since
        Aliens don't go unconsious"""

        self.exp += XCOMSoldier.exp_get_hit

        self.update_state()

    def check_for_level_up(self) -> None:

        if self.level >= XCOMSoldier.max_level: return

        #log.log(f"{self} gained {exp} exp ({self.exp})")
        #self.exp += exp

        while self.exp >= self.next_level_requirement:
            self.level += 1
            log.log(f"{self} leveled up to level {self.level}")

            if self.level in XCOMSoldier.proficiency_bonus_table:
                log.log(f"{self}'s proficiency has risen")
                self.proficiency += 1

            self.level_up_bonus()
        
            if self.level == XCOMSoldier.max_level:
                log.log(f"{self} has reached the maximum level!")
                self.next_level_requirement = math.inf
                
            else:
                self.next_level_requirement = math.ceil(self.next_level_requirement*XCOMSoldier.exp_level_mult) + XCOMSoldier.base_exp_increment

    def level_up_bonus(self):
        hp_increase = sum([random.randint(1, self.hit_die_type) for _ in range(self.num_hit_dice)])
        log.log(f"{self}'s maximum hit points increased by {hp_increase} to {self.max_hit_points + hp_increase}")
        self.max_hit_points += hp_increase
        self.cur_hit_points += hp_increase

        for _ in range(XCOMSoldier.perks_per_level):
            self.gain_new_perk()

    def gain_new_perk(self):
        possible = self.get_available_perks()

        if not any(possible):
            log.debug(f"No perks to choose from")
        else:
            choice = random.choice(possible)

        log.log(f"{self} has chosen {choice.name} as a new perk")

        if choice & Perk.Marksman:
            print(f"{self} hits the range and has improved their overall accuracy")
            self.attack_bonus += 1
            print(f"{self}'s attack bonus has increased to +{self.attack_bonus}")

        elif choice & Perk.Deadshot:
            print(f"{self} has become more efficient with their weapon, and can now use it better.")
            self.damage_bonus += 1
            print(f"{self}'s damage bonus has increased to +{self.damage_bonus}")

        elif choice & Perk.Toughness:
            
            if choice == Perk.ToughnessI:
                print(f"{self} has become a lot tougher, and is able to wear more damage before going down")
                self.num_hit_dice = 2
                print(f"{self}'s hit die is now a 2d4")
            
            elif choice == Perk.ToughnessII:
                print(f"{self} has endured enough pain, and is now heavily resisant to it")
                self.num_hit_dice = 3
                print(f"{self}'s hit die is now a 3d4")

            elif choice == Perk.ToughnessIII:
                print(f"{self} is so tough they are practically a walking tank!")
                self.num_hit_dice = 4
                print(f"{self}'s hit die is now a 4d4")

        elif choice & Perk.Lethality:
            print(f"Overall, {self} has become much more dangerous than a typical human")
            self.crit_level += 1
            self.crit_chance = Unit.crit_level_table[self.crit_level]
            print(f"{self}'s crititcal hit chance is now at +{round(self.crit_chance/1000,2)}%")

        elif choice & Perk.Recovery:
            print(f"{self} has become used to pain, and can now get back in the battlefield faster")
            self.recovery_bonus += 2
            print(f"{self}'s recovery bonus is now +{self.recovery_bonus}")

        elif choice & Perk.Plating:
            print(f"{self} has customized their armor to be even thicker and more hardy")
            self.armor += 1
            print(f"{self}'s armor bonus is now at {self.armor}")

        elif choice & Perk.Evasive:
            print(f"{self} has developed faster reflexes and is now more likely to graze incoming shots")
            self.evasion += 1
            print(f"{self}'s evasion bonus has increased to +{self.evasion}")

        elif choice & Perk.Shielding:
            print(f"{self} has gotten their armor upgraded to use more high-tech energy shielding")
            self.improve_shielding(1)
            print(f"{self}'s energy shields are now at +{self.max_shields}")

        elif choice & Perk.Capacitor:
            print(f"{self} has upgraded their shields to recharge on the battlefield")
            self.shield_regen += 1
            print(f"{self}'s shield regeneration has improved to +{self.shield_regen}")

        elif choice & Perk.Arsenal:
            
            if choice == Perk.ArsenalI:
                print(f"{self} ditches the standard issue assault rifle for a nice shotgun")
                self.weapon = wep_shotgun
                
            elif choice == Perk.ArsenalII:
                print(f"{self} decides to stay away from aliens, instead shooting them from afar with a sniper rifle")
                self.weapon = wep_sniper
            
            elif choice == Perk.ArsenalIII:
                print(f"{self} convinces the engineers to let them field test their new laser rifle")
                self.weapon = wep_laser_rifle

            elif choice == Perk.ArsenalIV:
                print(f"{self} gets a hold of a mean looking weapon capable of shooting a fistful of flaming hot shrapnel")
                self.weapon = wep_shrapnel_gun

            elif choice == Perk.ArsenalV:
                print(f"{self} 'borrows' one of the experimental weapons known as a laser cannon")
                self.weapon = wep_laser_cannon

            elif choice == Perk.ArsenalVI:
                print(f"{self} is chosen to field a new and prototype plasma rifle")
                self.weapon = wep_plasma_rifle

            elif choice == Perk.ArsenalVII:
                print(f"{self} decides they need something for bigger enemies... A shoulder-mounted rocket launcher should do.")
                self.weapon = wep_rocket_launcher

            elif choice == Perk.ArsenalVIII:
                print(f"{self} is rewarded for their hard work by the engineers. They are given a massive plasma cannon")
                self.weapon = wep_plasma_cannon

        elif choice & Perk.Armorer:
            
            if choice == Perk.ArmorerI:
                print(f"{self} ditches the standard issue vest for a set of advanced kevlar armor")
                self.armor_class = 12

            elif choice == Perk.ArmorerII:
                print(f"{self} manages to get their hands on experimental armor made of carbon nanothreds")
                self.armor_class = 14

            elif choice == Perk.ArmorerIII:
                print(f"{self} pulls some strings and gets a hold of an impossibly rare set of plasteel plate armor")
                self.armor_class = 15

            elif choice == Perk.ArmorerIV:
                print(f"{self} is chosen to try out an experimental set of armor made from the alien alloys")
                self.armor_class = 16

            elif choice == Perk.ArmorerV:
                print(f"{self} is one of the few lucky ones to get a hold of armor made of void-eater metal, a material made from collapsed stars")
                self.armor_class = 17
            
            print(f"{self}'s AC is now {self.armor_class}")

        elif choice & Perk.DieHard:

            print(f"{self} devlops a shocking resolve to live... No matter what.")
            if not (self.perk_flags & Perk.DieHardI):
                self.max_bleedout += 3
            else:
                self.max_bleedout += 2
            print(f"{self}'s bleedout timer has been increased to {self.max_bleedout}")

        elif choice & Perk.CritResist:
            print(f"{self} has studied tactics diligently to make sure they are prepared for when the enemy finds their weakness")
            self.crit_resist += 1
            print(f"{self}'s crit resistance level has increased to {self.crit_resist}")

        elif choice & Perk.Ordinance:

            if choice & Perk.OrdinanceI:
                print(f"{self} manages to get their hands on some frag grenades for next time they deploy")
                self.max_ordinance = 1 
                self.available_ordinance = 1
                self.ordinance_level += 1
            
            elif choice & Perk.OrdinaceII:
                print(f"{self} gets a hold of a crate of experimental plasma grenades... Just in case.")
                self.ordinance_level += 1

            elif choice & Perk.OrdinanceIII:
                print(f"Somehow, {self} acquired plastic explosives... Better watch out.")
                self.ordinance_level += 1

        elif choice & Perk.Blastmaster:

            print(f"{self} sacrifices some sandwich space for an extra explosive")
            self.max_ordinance += 1
            print(f"{self} now carries {self.max_ordinance} explosives")

        elif choice & Perk.Vengeance:

            print(f"{self} has had enough of getting shot. No more will they take it lying down")
            self.retaliation += 1
            print(f"{self}'s retaliation level has increased to {self.retaliation}")

        else:
            print(f"?????????????????????????????????")

        self.perk_flags |= choice

        log.wait(newlines = 1)

    def get_available_perks(self):
        new = []


        if self.level >= 15:
            if not(self.perk_flags & Perk.ArsenalVIII) and self.perk_flags & Perk.ArsenalVII:
                new.append(Perk.ArsenalVIII)

        if self.level >= 14:
            if not(self.perk_flags & Perk.ArmorerV) and self.perk_flags & Perk.ArmorerIV:
                new.append(Perk.ArmorerV)

            if not(self.perk_flags & Perk.CapacitorV) and self.perk_flags & (Perk.CapacitorIV | Perk.ShieldingV):
                new.append(Perk.CapacitorV)

        if self.level >= 13:
            if not(self.perk_flags & Perk.DeadshotV) and self.perk_flags & Perk.DeadshotIV:
                new.append(Perk.DeadshotV)

            if not(self.perk_flags & Perk.VengeanceIV) and self.perk_flags & Perk.VengeanceIII:
                new.append(Perk.VengeanceIV)

            if not(self.perk_flags & Perk.ShieldingV) and self.perk_flags & Perk.ShieldingIV:
                new.append(Perk.ShieldingV)

        if self.level >= 12:
            if not(self.perk_flags & Perk.ArsenalVII) and self.perk_flags & Perk.ArsenalVI:
                new.append(Perk.ArsenalVII)

            if not(self.perk_flags & Perk.LethalityIII) and self.perk_flags & Perk.LethalityII:
                new.append(Perk.LethalityIII)

            if not(self.perk_flags & Perk.DieHardIII) and self.perk_flags & Perk.DieHardII:
                new.append(Perk.DieHardIII)


        if self.level >= 11:
            if not(self.perk_flags & Perk.BlastmasterIII) and self.perk_flags & Perk.BlastmasterII:
                new.append(Perk.BlastmasterIII)

            if not(self.perk_flags & Perk.RecoveryV) and self.perk_flags & Perk.RecoveryIV:
                new.append(Perk.RecoveryV)

            if not(self.perk_flags & Perk.ArmorerIV) and self.perk_flags & Perk.ArmorerIII:
                new.append(Perk.ArmorerIV)

            if not(self.perk_flags & Perk.VengeanceIII) and self.perk_flags & Perk.VengeanceII:
                new.append(Perk.VengeanceIII)

            if not(self.perk_flags & Perk.CapacitorIV) and self.perk_flags & (Perk.CapacitorIII | Perk.ShieldingIV):
                new.append(Perk.CapacitorIV)

        if self.level >= 10:


            if not(self.perk_flags & Perk.PlatingV) and self.perk_flags & Perk.PlatingIV:
                new.append(Perk.PlatingV)

            if not(self.perk_flags & Perk.ArsenalVI) and self.perk_flags & Perk.ArsenalV:
                new.append(Perk.ArsenalVI)

            if not(self.perk_flags & Perk.OrdinanceIII) and self.perk_flags & Perk.OrdinaceII:
                new.append(Perk.OrdinanceIII)

            if not(self.perk_flags & Perk.DeadshotIV) and self.perk_flags & Perk.DeadshotIII:
                new.append(Perk.DeadshotIV)

            if not(self.perk_flags & Perk.ShieldingIV) and self.perk_flags & Perk.ShieldingIII:
                new.append(Perk.ShieldingIV)

            if not(self.perk_flags & Perk.EvasiveIII) and self.perk_flags & Perk.EvasiveII:
                new.append(Perk.EvasiveIII)

        if self.level >= 9:

            if not(self.perk_flags & Perk.MarksmanV) and self.perk_flags & Perk.MarksmanIV:
                new.append(Perk.MarksmanV)

            if not(self.perk_flags & Perk.BlastmasterII) and self.perk_flags & Perk.BlastmasterI:
                new.append(Perk.BlastmasterII)

            if not(self.perk_flags & Perk.CritResistIII) and self.perk_flags & Perk.CritResistII:
                new.append(Perk.CritResistIII)

            if not(self.perk_flags & Perk.CapacitorIII) and self.perk_flags & (Perk.CapacitorII | Perk.ShieldingIII):
                new.append(Perk.CapacitorIII)

        if self.level >= 8:

            if not(self.perk_flags & Perk.PlatingIV) and self.perk_flags & Perk.PlatingIII:
                new.append(Perk.PlatingIV)

            if not(self.perk_flags & Perk.ArsenalV) and self.perk_flags & Perk.ArsenalIV:
                new.append(Perk.ArsenalV)

            if not(self.perk_flags & Perk.RecoveryIV) and self.perk_flags & Perk.RecoveryIII:
                new.append(Perk.RecoveryIV)

            if not(self.perk_flags & Perk.MarksmanIV) and self.perk_flags & Perk.MarksmanIII:
                new.append(Perk.MarksmanIV)

            if not(self.perk_flags & Perk.ArmorerIII) and self.perk_flags & Perk.ArmorerII:
                new.append(Perk.ArmorerIII)

            if not(self.perk_flags & Perk.VengeanceII) and self.perk_flags & Perk.VengeanceI:
                new.append(Perk.VengeanceII)

            if not(self.perk_flags & Perk.ShieldingIII) and self.perk_flags & Perk.ShieldingII:
                new.append(Perk.ShieldingIII)

            if not(self.perk_flags & Perk.CapacitorII) and self.perk_flags & (Perk.CapacitorI | Perk.ShieldingII):
                new.append(Perk.CapacitorII)


        if self.level >= 7:

            if not(self.perk_flags & Perk.DeadshotIII) and self.perk_flags & Perk.DeadshotII:
                new.append(Perk.DeadshotIII)

            if not(self.perk_flags & Perk.ToughnessIII) and self.perk_flags & Perk.ToughnessII:
                new.append(Perk.ToughnessIII)

            if not(self.perk_flags & Perk.LethalityII) and self.perk_flags & Perk.LethalityI:
                new.append(Perk.LethalityII)

            if not(self.perk_flags & Perk.DieHardII) and self.perk_flags & Perk.DieHardI:
                new.append(Perk.DieHardII)

            if not(self.perk_flags & Perk.CritResistII) and self.perk_flags & Perk.CritResistI:
                new.append(Perk.CritResistII)

            if not(self.perk_flags & Perk.ShieldingII) and self.perk_flags & Perk.ShieldingI:
                new.append(Perk.ShieldingII)

            if not(self.perk_flags & Perk.EvasiveII) and self.perk_flags & Perk.EvasiveI:
                new.append(Perk.EvasiveII)

        if self.level >= 6:

            if not(self.perk_flags & Perk.CapacitorI) and self.perk_flags & Perk.ShieldingI:
                new.append(Perk.CapacitorI)

            if not(self.perk_flags & Perk.PlatingIII) and self.perk_flags & Perk.PlatingII:
                new.append(Perk.PlatingIII)

            if not(self.perk_flags & Perk.ArsenalIV) and self.perk_flags & Perk.ArsenalIII:
                new.append(Perk.ArsenalIV)

            if not(self.perk_flags & Perk.OrdinaceII) and self.perk_flags & Perk.OrdinanceI:
                new.append(Perk.OrdinaceII)

            if not(self.perk_flags & Perk.BlastmasterI) and self.perk_flags & Perk.OrdinanceI:
                new.append(Perk.BlastmasterI)

            if not(self.perk_flags & Perk.RecoveryIII) and self.perk_flags & Perk.RecoveryII:
                new.append(Perk.RecoveryIII)

        if self.level >= 5:

            if not(self.perk_flags & Perk.ShieldingI):
                new.append(Perk.ShieldingI)

            if not(self.perk_flags & Perk.DeadshotII) and self.perk_flags & Perk.DeadshotI:
                new.append(Perk.DeadshotII)

            if not(self.perk_flags & Perk.MarksmanIII) and self.perk_flags & Perk.MarksmanII:
                new.append(Perk.MarksmanIII)

            if not(self.perk_flags & Perk.ArmorerII) and self.perk_flags & Perk.ArmorerI:
                new.append(Perk.ArmorerII)

            if not(self.perk_flags & Perk.CritResistI):
                new.append(Perk.CritResistI)
            
        if self.level >= 4:


            if not(self.perk_flags & Perk.PlatingII) and self.perk_flags & Perk.PlatingI:
                new.append(Perk.PlatingII)

            if not(self.perk_flags & Perk.ArsenalIII) and self.perk_flags & Perk.ArsenalII:
                new.append(Perk.ArsenalIII)

            if not(self.perk_flags & Perk.RecoveryII) and self.perk_flags & Perk.RecoveryI:
                new.append(Perk.RecoveryII)

            if not(self.perk_flags & Perk.ToughnessII) and self.perk_flags & Perk.ToughnessI:
                new.append(Perk.ToughnessII)

            if not(self.perk_flags & Perk.VengeanceI):
                new.append(Perk.VengeanceI)

        if self.level >= 3:

            if not(self.perk_flags & Perk.DieHardI):
                new.append(Perk.DieHardI)

            if not(self.perk_flags & Perk.OrdinanceI):
                new.append(Perk.OrdinanceI)

            if not(self.perk_flags & Perk.ArsenalII) and self.perk_flags & Perk.ArsenalI:
                new.append(Perk.ArsenalII)

            if not(self.perk_flags & Perk.MarksmanII) and self.perk_flags & Perk.MarksmanI:
                new.append(Perk.MarksmanII)

            if not(self.perk_flags & Perk.LethalityI):
                new.append(Perk.LethalityI)

            if not(self.perk_flags & Perk.EvasiveI):
                new.append(Perk.EvasiveI)

        if self.level >= 2:

            if not(self.perk_flags & Perk.PlatingI):
                new.append(Perk.PlatingI)
            
            if not(self.perk_flags & Perk.DeadshotI):
                new.append(Perk.DeadshotI)
            
        if self.level >= 1:

            if not(self.perk_flags & Perk.MarksmanI):
                new.append(Perk.MarksmanI)

            if not(self.perk_flags & Perk.ToughnessI):
                new.append(Perk.ToughnessI)

            if not(self.perk_flags & Perk.RecoveryI):
                new.append(Perk.RecoveryI)

            if not(self.perk_flags & Perk.ArsenalI):
                new.append(Perk.ArsenalI)

            if not(self.perk_flags & Perk.ArmorerI):
                new.append(Perk.ArmorerI)


        return new

    def show_stats(self) -> None:
        """TODO"""
        log.log(f"{self}")
        log.log(f"Level: {self.level}")
        log.log(f"EXP: {self.exp}/{self.next_level_requirement}")
        log.log(f"------------")
        log.log(f"Max HP      :       {self.max_hit_points}")
        log.log(f"AC          :       {self.armor_class}")
        log.log(f"Attack Bonus:       {self.attack_bonus}")
        log.log(f"Damage Bonus:       {self.damage_bonus}")
        log.log(f"Weapon      :       {self.weapon.num_dice}d{self.weapon.dice_sides}")
        log.log(f"Hit Die     :       {self.num_hit_dice}d{self.hit_die_type}")
        log.log(f"Crit Chance :       {self.crit_chance}%")
        log.log(f"Crit Resist :       {self.crit_resist}")
        log.log(f"Recovery    :       {self.recovery_bonus}")
        log.log(f"Evasion     :       {self.evasion}")
        log.log(f"Armor       :       {self.armor}")
        log.log(f"Ordinance   :       {self.ordinance_level}")
        log.log(f"Explosives  :       {self.max_ordinance}")
        log.log(f"Shielding   :       {self.max_shields} with {self.shield_regen} regen")
        log.log(f"Bleedout    :       {self.max_bleedout}")
        log.log(f"Retaliation :       {self.retaliation_chance}")
        log.log(f"-----------------")
        log.log(f"Kills       :       {self.kills}")
        log.log(f"Damage Dealt:       {self.damage_dealt}")
        log.log(f"Damage Taken:       {self.damage_taken}")
        if self.shots_taken == 0:
            print(f"Accuracy    :       -/-")
        else:
            print(f"Accuracy    :       {round(self.shots_hit/self.shots_taken, 3)*100}%")


humans = [
    XCOMSoldier("Mitchell"),
    XCOMSoldier("Stephen"),
    XCOMSoldier("Preston"),
    XCOMSoldier("Colton"),
    XCOMSoldier("Emma"),
    XCOMSoldier("Roz"),
    XCOMSoldier("Ben"),
    XCOMSoldier("Matteo"),
    XCOMSoldier("Allyson"),
    XCOMSoldier("Caitlin"),
    XCOMSoldier("Levi"),
    XCOMSoldier("Allyson"),
]
