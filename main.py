from units import XCOMSoldier as Soldier, Unit, humans
from items import wep_assault_rifle, wep_plasma_rifle, wep_shotgun
from battling import Battle

def main():
    
    aliens = [Unit("Prax", 20, 12, 1, wep_plasma_rifle, 1), Unit("Prax", 20, 12, 1, wep_plasma_rifle, 1), Unit("Prax", 20, 12, 1, wep_plasma_rifle, 1), Unit("Prax", 20, 12, 1, wep_plasma_rifle, 1)]
    aliens2= [Unit("Allopew", 6, 10, 0, wep_shotgun, 1), Unit("Allopew", 6, 10, 0, wep_shotgun, 1), Unit("Allopew", 6, 10, 0, wep_shotgun, 1), Unit("Allopew", 6, 10, 0, wep_shotgun, 1)]

    b = Battle(humans=humans,aliens=aliens2)
    b.fight()
    dead = b.killed_humans
    for d in dead:
        print(f"{d} has died")

    for h in b.humans:
        h.award_exp(0)
    print("Fight over")





if __name__ == "__main__":
    main()