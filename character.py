"""
character.py: Character and License classes
"""
from time import *
from item import *
from colors import *
from utils import *

# random name gen: \
# pr(f"{choice(N.f + N.m)} {choice(FN.n)}")

class Character:
    """ CHARACTER Class - All people & creatures """
    def __init__(self, name, location):
        self.name = name ### mission_one?
        self.hp = 25 ### mission_one?
        self.armor = None
        self.location = location # node or area? object instead of str!
        self.node = None
        self.path = ["INTRO"]
        self.inv = [] ### class Inventory w/ modified __add__, __sub__, etc.!
        self.credits = 0
        self.licences = [] # License / Right / Permit Class
        self.time = 0
        self.date = None

    def show_stats(self):
        pr(f"Health: {C.BOLD}{self.hp}{C.END}")
        pr(f"Wealth: {C.BOLD}€{self.credits} · Φ0 · &+0 · ?!0{C.END}")
        pr("")

    def show_inv(self): # Try making one multiline f-String!
        # try:
        #     unique_species = sorted(set([x.species for x in self.inv]))
        # except AttributeError:
        #     pass
        prey = [i for i in self.inv if isinstance(i, Prey)]
        # pr(prey)
        unique_species = sorted(set([x.species for x in prey]))
        giants_id = [i for i, a in enumerate(prey) if a.is_giant]
        pr(f"INVENTORY ({len(self.inv)})", end="")
        for item in self.inv:
            pr (f" · {item.size_name} {item} (€{item.value})", end="") # chronologically
        if len(unique_species) > 0:
            pr("")
            pr("")
            pr(f"SPECIES ({len(unique_species)})", end="") # alphabetically
            pr(" · ", end="")
        pr(" · ".join(str(species) for species in unique_species))
        if len(giants_id) > 0:
            pr("")
            pr(f"GIANTS ({len(giants_id)})", end="") # chronologically
            for idx in giants_id:
                pr(f" · {self.inv[idx]}", end="")
            pr("")
        pr("")

    def calc_date(self):
        """Calculate self.date out of self.time"""
        minutes = self.time * 5  # time_passed is in 5-minute units
        days_passed = minutes // 1440
        time_leftover = minutes % 1440
        hours_passed = time_leftover // 60
        min_passed = time_leftover % 60
        self.date = f"{days_passed} days, {hours_passed} hours, {min_passed} min"
        return self.date

    def hp_mod(self, hp, *higher_hp):
        hp_mod = randint(hp, higher_hp[0]) if higher_hp else hp
        self.hp += hp_mod
        plus_minus = "Plus" if hp_mod >= 0 else "Minus"
        pr(f"{plus_minus} {abs(hp_mod)} HP!\n")

    def skill_mod(self, skill, mod, *higher_mod): # !?
        pass

    def sell_to(self, buyer):
        sale_value = 0
        pr(f"Sell something to {buyer.name} (*/+ for all):")
        pr(f"{C.YELLOW}0{C.END} · Stop trade.")
        for i, item in enumerate(self.inv):
            pr(f"{C.YELLOW}{i + 1}{C.END} · {item.size_name} {item} (€{item.value})")
        while True:
            try:
                raw_inp = input()
                inp = raw_inp.replace(","," ").replace("."," ").replace(";"," ")
                if raw_inp == "*" or raw_inp == "+":
                    sale_items = [i for i, e in enumerate(self.inv)]
                elif raw_inp == "0":
                    pr(f"Stop Trade.")
                    pr("")
                    break
                else:
                    sale_items = [(int(s) - 1) for s in inp.split() if s.isdigit()]
                if not sale_items:
                    pr(f"No items selected.")
                    pr("")
                    break
                else:
                    items_str = "item" if len(sale_items) == 1 else "items"
                    pr(f"{C.GRAY}{C.CURSIVE}Sell {len(sale_items)} {items_str}{C.END}", end="")
                    for i in sorted(sale_items, reverse=True):
                        buyer.inv.append(self.inv[i]) # Add to buyer
                        sale_value += self.inv[i].value
                        pr(f" · {C.GRAY}{self.inv[i].size_name} {self.inv[i]}{C.END}", end="")
                        del self.inv[i] # Remove from seller
                    pr("\n")
                    buyer.credits -= sale_value # Subtract credits from buyer
                    self.credits += sale_value # Add credits to seller
                    pr(f"Buyer: {buyer.name.upper()} €{buyer.credits}")
                    pr(f"Total value of the sale: {sale_value}")
                    pr(f"Your credits now: {self.credits}")
                    pr("")
                    break
            except IndexError:
                pr("")
                pr("Enter valid number(s) of item(s) to sell.")
                pr("")

    # def catch(self, attempts, targets): # merge fish() & hunt()
    #     pass

    def fish(self, attempts):
        quarry = []
        hits = []
        for attempt in range(attempts):
            sleep(T.XL)
            hits.append(round(random(),2))
            if hits[attempt] >= 0.62:
                slain_animal = (Prey(attempt, Prey.fish_species))
                self.inv.append(slain_animal)
                quarry.append(slain_animal)
                pr(f"Success ({hits[attempt]}) - {slain_animal.size_name} {slain_animal} caught!") # "Success"-variety
            else:
                pr("Fail.") # Variety! This triggers a lot!
        sleep(T.XXXL)
        pr(f"You had {attempts} nibbles and got {len(quarry)} fish!")
        sleep(T.XXL)

    def hunt(self, attempts):
        quarry = []
        hits = []
        for attempt in range(attempts):
            sleep(T.XS)
            hits.append(round(random(),2))
            if hits[attempt] >= 0.72:
                slain_animal = (Prey(attempt, Prey.game_species))
                self.inv.append(slain_animal)
                quarry.append(slain_animal)
                pr(f"Success ({hits[attempt]}) - {slain_animal.size_name} {slain_animal} caught!") # "Success"-variety
            else:
                pr("Fail.") # Variety! This triggers a lot!
        sleep(T.XXXL)
        pr(f"You had {attempts} sightings and got {len(quarry)} animals!")
        sleep(T.XXL)
        
class Licence:
    """LICENCE Class - for RIGHTS, TICKETS, PAPERS, PERMITS, ..."""
    def __init__(self, name, holder, *permits):
        self.name = name
        self.holder = holder
        holder.licences.append(self)
        self.permits = []
        for p in permits:
            self.permits.append(p)

    def __repr__(self):
        return f"{self.name}"