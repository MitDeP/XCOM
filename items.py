"""File for items"""
import random


class Weapon:

    def __init__(self, name:str, num_dice:int, dice_sides:int, damage_bonus:int):
        self.name:str           =       name
        self.num_dice:int       =       num_dice
        self.dice_sides:int     =       dice_sides
        self.damage_bonus:int   =       damage_bonus


    def roll_damage(self, ext_damage_bonus:int =0 ) -> int:
        return sum([random.randint(1, self.dice_sides) for _ in range(self.num_dice)]) + self.damage_bonus + ext_damage_bonus



wep_assault_rifle   =   Weapon("Assault Rifle",     1, 6, 0)
wep_shotgun         =   Weapon("Shotgun",           2, 4, 0)
wep_sniper          =   Weapon("Sniper Rifle",      1, 10,0)
wep_laser_rifle     =   Weapon("Laser Rifle",       2, 6, 0)
wep_shrapnel_gun    =   Weapon("Shrapnel Gun",      2, 8, 0)
wep_laser_cannon    =   Weapon("Laser Cannon",      3, 6, 0)
wep_plasma_rifle    =   Weapon("Plasma Rifle",      4, 6, 0)
wep_rocket_launcher =   Weapon("Rocket Launcher",   5, 6, 0)
wep_plasma_cannon   =   Weapon("Plasma Cannon",     4, 8, 0)
wep_void_gun        =   Weapon("Void Gun",          4, 10,0)