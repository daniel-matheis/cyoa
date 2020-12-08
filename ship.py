""" DOC STRING for SHIP -  """
from random import *
from time import *

class Character:
    """ Character Class """
    def __init__(self):
        self.name = None
        self.location = None
        self.hp = 10
        self.credits = 0
        self.rank = None
        self.ship_assignment = None
#         self.command_skill = 0.0
#         self.science_skill = 0.0
#         self.security_skill = 0.0
        """
        instead of seperate gun-/pistol-skill just specialties, f.e.:
        sniper-rifles +2, protocol -1, piloting +1
        """
#         self.diplomacy_skill = 0.0
        
    def __repr__(self):
        return f"{self.name}"
        
# ''' Location Class '''
# class Location:
#     def __init__(self, name):
#         self.name = name
#         self.characters_present = []

class Dock:
    """ Dock Class """
    def __init__(self, name):
        self.name = name
        self.location = None
        self.torpedo_bay = []
        self.torpedos = []

    def __repr__(self):
        return self.name

class Ship:
    """ Ship Class """  # bsp "Battle Cruiser"
    type = "Battle Cruiser"
    def __init__(self, name):
        self.name = name
        self.crew = []
        self.captain = None # Character in charge of the vessel
        self.affiliation = "Pirates"
        self.location = "Dock" # (0, 0) Coordinates?
        self.speed_max = 10 # Depends on ship class & energy
#         self.speed = 0 # Present speed
        self.hp_mx = 50 # Maximum hull hitpoints
        self.hp = 50 # Present hull hitpoints
        self.hp_status = self.hp / self.hp_mx # *100 Percent
        self.destroyed = False
        self.shield_max = 25 # Maximum defensive shield
        self.shield = 25 # Present defensive shield
        self.shield_status = self.shield / self.shield_max # *100 Percent
        self.energy = 0 # Ships systems, propulsion, shields, ...
        self.systems_online = False
        self.target = None
        self.phaser = None # Phaser w/ stats
        self.torpedo_bay = [] # Torpedo Bay List
        self.torpedos = [] # List of loaded torpedos
        
    def __repr__(self):
        return self.name
        
    def systems_check(self):
        if self.energy >= 1 and not self.systems_online:
            self.systems_online = True
            print(f"{self.name.upper()}: Systems coming online ...\n")
            
    def load_magazine(self, magazine):
#         magazine.location.torpedo_bay = None
        self.torpedo_bay.append(magazine)
        self.torpedos = magazine.torpedos
        magazine.location = self

    def arm_with(self, torpedo):
        self.torpedo_bay[0].arm_with(torpedo)
            
    def attack(self, target, weapon): ### split up into parts!
        if self.destroyed: # check if fight over in main while loop!
            pr(f"Outcome of the engagement: {self} lost.")
            quit()
        pr(f"{self.name.upper()} ATTACKS {target.name.upper()} with {weapon}.")
        # sleep(2.45)
        if type(weapon) == Torpedo: # Check if torpedo left ship / explodes later
            self.torpedos.remove(weapon)
            # pr(f"w.loc.torp: {weapon.location.torpedos}")
            # weapon.location.torpedos.remove(weapon)
        else:
            pass
        self.target = target # important for Engangement class
        if weapon.force < target.shield:
            target.shield -= weapon.force
            target.shield_status = target.shield / target.shield_max
            if target.shield_status > 0.15:
                pr(f"{target.name.upper()}: Shield down to {target.shield}!")
            else:
                pr(f"{target.name.upper()}: Shields in critial condition, barely holding at {target.shield_status*100} percent!")
            # check casualties or other further damage
        elif target.shield <= weapon.force < (target.shield + target.hp):
            target.hp -= (weapon.force - target.shield)
            target.hp_status = target.hp / target.hp_mx
            target.shield = 0
            if target.shield_status != 0: # hadn't been destroyed yet
                target.shield_status = 0
                pr(f"{target.name.upper()}: Shield destroyed! {target.hp} HP left!")
            else:
                pr(f"{target.name.upper()}: Shield gone. {target.hp} HP left!")
            # check casualties or other further damage
        else: # TARGET DESTROYED
            target.shield = 0
            target.shield_status = 0
            target.hp = 0
            target.hp_status = 0
            target.destroyed = True
            for member in target.crew:
                member.hp = 0
                member.status = "KIA"
            Engagement.destruction_report(target)

        # sleep(2.45)
        pr("")

class Phaser:
    """ Phaser Class """
    def __init__(self, location, rng, force):
        self.location = location
        self.range = rng
        self.force = force
        location.phaser = self
        
    def __repr__(self):
        return f"FRC-{self.force} {self.location}-PH{self.range}R"

class Torpedo:
    """ Torpedo Class """
    def __init__(self, name, location):
        self.id = name
        self.type = None
        self.location = location
        self.range = 17
        self.precision = 1
        self.force = 12
        location.torpedos.append(self)
        if isinstance(location, TorpedoBay):
            location.location.torpedos.append(self)
        
    def __repr__(self):
        if self.id < 10:
            return f"{self.type} Torpedo (TID-00{self.id})"
        elif 9 < self.id < 100:
            return f"{self.type} Torpedo (TID-0{self.id})"
        else:
            return f"{self.type} Torpedo (TID-{self.id})"

    def show(self):
        print(self.type)
                
class TorpedoBay:
    """ Torpedo Bay Class """
    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.reload_time = 12
        self.torpedos = []
        location.torpedo_bay.append(self)
        
    def __repr__(self):
        return f"{self.location} MAG-{self.capacity}"
        
    def show(self):
        for torpedo in self.torpedos:
            torpedo.show()
            
    def arm_with(self, torpedo):
#       if len[self.torpedos] < self.capacity:
        torpedo.location = self
        # self.torpedos.append(torpedo)
        self.location.torpedos.append(torpedo)
        pr(f"Now newly loaded into {self}: {torpedo}")
        # sleep(2.45)
        pr("")

class Engagement:
    """ Engagement Class """
    # pass # init only once ship.target exists
    def destruction_report(target):
        pr(f"· " * ((len(target.name) + 3) // 2 + 6))  # 6 wegen destroyed
        pr(f"· {target.name.upper()} DESTROYED ·")
        pr(f"· " * ((len(target.name) + 3) // 2 + 6))
        pr(f"{target.type} \n"
           f"{target.name}\n"
           f"Captained by {target.captain}\n"
           f"of the {target.affiliation}\n"
           f"\nCrew lost (( {len(target.crew)} ))")
        for crmb in target.crew:
            pr(f"{crmb.rank} {crmb.name}")

def ship_stats(ship):
    """ Show SHIP STATISTICS """
    pr(f"{ship.name.upper()} - SHIP STATS")
    for k, v in ship.__dict__.items():
        pr(f"{k}: {v}")
        # sleep(0.1625)
    pr("")

def pr(x, **kwargs):
    """ Print """
    print(x, **kwargs)

def example_1():
    """ EXAMPLE NO. 1 """
    bob = Character()
    bob.name = "Bob"
    bob.location = "Dock"
    bob.credits = 25
    # bob.ship_assignment = "Venus"
    venus = Ship("Venus")
    venus.crew.append(bob) ### venus.add_to_crew() and v.make_captain() instead
    bob.location = venus ###
    bob.ship_assignment = venus
    bob.rank = "Captain" ### venus.assign_posts() / v.promote()
    venus.captain = bob ### venus.make_captain()
    phaser_ven = Phaser(venus, 7, 7)
    mag_ven = TorpedoBay(venus, 2)
    shark_001 = Torpedo(1, mag_ven)
    shark_001.type = "Shark"
    whale_001 = Torpedo(2, mag_ven)
    whale_001.type = "Whale"
    venus.energy += 1
    venus.systems_check()
    ship_stats(venus)

    mars = Ship("Mars") # Target
    phaser_mar = Phaser(mars, 5, 10)
    mars.energy += 1 # Shields need energy
    mars.systems_check() # Systems ON

    # who_acts_first() -> Venus because Mars online but no captain
    venus.attack(mars, phaser_ven)
    john = Character()
    john.name = "John"
    john.ship_assignment = mars
    john.location = mars
    mars.crew.append(john)
    john.rank = "Captain" ### Make Rank Class
    mars.captain = john ### mars.make_captain()
    mars.attack(venus, phaser_mar) # assuming Mars has now a captain
    venus.attack(mars, whale_001) # TID-002 gone! First torpedo hit.
    ship_stats(venus)
    venus.attack(mars, phaser_ven)
    dock_1 = Dock("Iono Dock")
    mag_mars = TorpedoBay(dock_1, 3)
    shark_010 = Torpedo(3, mag_mars)
    shark_010.type = "Shark"

    mars.load_magazine(mag_mars)
    whale_011 = Torpedo(4, dock_1) # in dock and too late for mag_mars
    whale_011.type = "Whale"
    whale_012 = Torpedo(5, dock_1) # id-005 also in dock instead of mars
    whale_012.type = "Whale"
    pr("Venus steals Whale torpedo designated for Mars!")
    mag_ven.arm_with(whale_011) # venus steals whale_011 from mars
    ship_stats(venus)
    pr("No normal 2nd torpedo for Mars! \nBut yes, replacement was sent. TID-005")
    mag_mars.arm_with(whale_012) # mars gets 5th replacement whale_012
    ship_stats(mars)
    # Surprise Attack by Venus
    venus.attack(mars, shark_001) # TID-001 gone! Both oldest torpedos fired and hit.
    ship_stats(venus)

    dolphin = Torpedo(6, dock_1) # 'Geheime Waffenlieferung': Prototype 'Dolphin'
    dolphin.type = "Dolphin"
    dolphin.force += 1
    dolphin.range += 2
    dolphin.precision += 1
    mag_ven.arm_with(dolphin) # Venus in a good position

    carl = Character()
    carl.name = "Carl"
    carl.ship_assignment = venus
    carl.location = venus
    venus.crew.append(carl)
    carl.rank = "First Officer" ### Make Rank Class
    ship_stats(venus)

    octopus = Torpedo(7, dock_1) # Multihead-Torpedo
    octopus.type = "Octopus Quattro"
    octopus.force = int(octopus.force * 4 * 0.33)
    octopus.range -= 2
    octopus.precision += 3
    mars.arm_with(octopus)
    mars.attack(venus, octopus)
    mars.attack(venus, shark_010)
    ship_stats(venus)
    venus.attack(mars, whale_011)
    ship_stats(mars)
    mars.attack(venus, phaser_mar)
    ship_stats(venus)
    venus.attack(mars, dolphin)
    ship_stats(mars)
    mars.attack(venus, phaser_mar)
    mars.attack(venus, whale_012)
    ship_stats(venus)
    venus.attack(mars, phaser_ven)
    mars.attack(venus, phaser_mar)
    # pr(bob.__dict__)

example_1()