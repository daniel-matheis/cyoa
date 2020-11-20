""" CYOA Node-Choice-FX System · imju.li/CYOA """

import os
from random import *
from time import *
import textwrap

''' Clear the screen '''
def clear_screen():
    os.system('cls')

''' Print '''
def pr(txt, **kwargs):
    print(txt, **kwargs)

''' T Class (Time & Tempo) '''
class T:    # all in seconds
    PERCENT   =    0.13     # 1.00 for Original Time of Pauses
    XXS     = 0.29*PERCENT
    XS      = 0.47*PERCENT
    S       = 0.56*PERCENT
    M       = 0.65*PERCENT
    L       = 0.74*PERCENT
    XL      = 0.83*PERCENT
    XXL     = 0.92*PERCENT
    XXXL    = 1.10*PERCENT

''' C(OLORS) Class (40-47 BG, 100-107 BG light) '''
class C:
    BLACK           = "\033[30m"
    RED             = "\033[31m"
    GREEN           = "\033[32m"
    YELLOW          = "\033[33m"
    BLUE            = "\033[34m"
    PURPLE          = "\033[35m"
    CYAN            = "\033[36m" # Location / Node
    GRAY            = "\033[90m" # Decision taken
    LIGRAY       = "\033[37m"
    LIRED        = "\033[91m"
    LIGREEN      = "\033[92m"
    LIYELLOW     = "\033[93m"
    LIBLUE       = "\033[94m"
    LIPURPLE     = "\033[95m"
    LICYAN       = "\033[96m"
    WHITE           = "\033[97m"
    BOLD            = "\033[1m"
    CURSIVE         = "\033[3m"
    UNDERLINE       = "\033[4m"
    END             = "\033[0m" # Reset All

''' AREA Class '''
class Area:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.sample_prey = [] # weighed sample of fauna for every area's flora

    def __repr__(self):
        return f"{self.name}"

''' NODE Class '''
class Node:
    instances = []
    def __init__(self, name, area, txt):
        self.name = name
        self.area = area
        self.txt = txt
        self.choices = []
        self.decision = None
        self.next_node = "x"
        self.been_here = 0
        self.familiar = ""
        Node.instances.append(self)

    def __repr__(self):
        return f"{self.name}" # ' in {self.area}'

    def play(self): # Main Method that calls upon the single parts
        self.node_prep()
        player.node = self
        player.location = self
        player.path.append(self)
        pr(f"You're {self.familiar}at the {C.CYAN}{player.location.name}{C.END}.")
        self.been_here += 1
        self.print_node_txt()
        self.print_choices_txt()
        # if not self.choices: # needed if no choices in node
        #     return # return or quit()
        self.catch_one_choice_case()
        self.take_decision()
        self.fx_fallout()
        self.play_next_node()

    def node_prep(self):
        if self.been_here >= 3:
            self.familiar = "once more back again "
        elif self.been_here == 2:
            self.familiar = "back again "
        elif self.been_here == 1:
            self.familiar = "again "
        elif self.been_here == -1:
            self.familiar = "still "
        else:
            self.familiar = ""

    def print_node_txt(self):
        t = f'pr(f"{self.txt}")'
        node_txt_updated = compile(t, "new_node_txt", "exec")
        exec(node_txt_updated)  # Print Node Text

    def print_choices_txt(self):
        for i, chc in enumerate(self.choices):  # Print all Choices Texts
            if len(self.choices) == 1:
                c = f'pr(f"{C.YELLOW}·{C.END} · {chc.txt}")'
            else:
                c = f'pr(f"{C.YELLOW}{i + 1}{C.END} · {chc.txt}")'
            choice_txt_updated = compile(c, "new_choice_txt", "exec")
            exec(choice_txt_updated)

    def catch_one_choice_case(self):
        if len(self.choices) == 1:
            self.decision = 1
            while True:
                try:
                    inp = input()
                    if inp == "" or inp == " " or inp == "0" or inp == "1":
                        break # Good Input, ready to continue
                    pr(f"Press 'Enter'.")
                except ValueError:
                    pr("ValueError")
            pr(f"{C.GRAY}{C.CURSIVE}{self.choices[self.decision - 1].txt}{C.END}")
            sleep(T.XS)
            pr("")
            globals()[self.choices[0].dest].play()

    def take_decision(self):
        input_tries = 1 # including successful input
        punc_mark = "."
        while True:
            if input_tries >= 3:
                punc_mark = "!"
            try:
                self.decision = int(input(""))  # Decision Integer Check
                if len(self.choices) >= self.decision > 0:
                    break # Good Input, ready to continue
                pr(f"Enter number within choices{punc_mark}")
                input_tries += 1
            except ValueError: # No Integer Exception
                print(f"ValueError - Enter number{punc_mark}")
                input_tries += 1
        sleep(0.07)
        pr(f"{C.GRAY}{C.CURSIVE}{self.choices[self.decision - 1].txt}{C.END}")
        sleep(T.XS)
        pr("")

    def fx_fallout(self):
        self.choices[self.decision - 1].fx_repercussions()  # FX of Decision

    def play_next_node(self):
        if self.choices[self.decision - 1].dest: # if there is a next_node
            self.next_node = self.choices[self.decision - 1].dest
            this_node = str(self.choices[self.decision].node.name)
            if self.next_node in this_node.lower():
                self.been_here = -1
            globals()[self.next_node].play() # Play NEXT NODE
        else:
            self.been_here = -1 # "still " and reset familiarity
            self.play() # Play the SAME NODE AGAIN if no destination (def_choices)

''' CHOICE Class '''
class Choice:
    def __init__(self, node, txt, dest, *effects):
        self.node = node
        node.choices.append(self)
        self.txt = txt
        self.dest = dest
        self.fx = []
        for effect in effects:
            self.fx.append(effect)

    def fx_repercussions(self):
        for effect in self.fx:
            compile(effect, "fx-c-name", "exec")
            exec(effect)

''' CHARACTER Class - All people & creatures '''
class Character: # Child Class for Player?
    def __init__(self, name, location):
        self.name = name
        self.hp = 50
        self.location = location
        self.node = None
        self.path = []
        self.inventory = [] # CREATE INVENTORY CLASS!
        self.credits = 0
        self.time = None # Time of day at Character's location

    def show_stats(self):
        pr(f"HP: {self.hp}")
        pr("")

    def show_inv(self): # Try making one multiline f-String!
        pr(f"{C.BOLD}€{self.credits}{C.END}")
        unique_species = sorted(set([x.species for x in self.inventory]))
        giants_id = [i for i, a in enumerate(self.inventory) if a.is_giant]
        pr(f"INVENTORY ({len(self.inventory)})", end="")
        for item in self.inventory:
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
                pr(f" · {self.inventory[idx]}", end="")
            pr("")
        pr("")

    def hp_mod(self, hp, *higher_hp):
        plus_minus = "Plus"
        if not higher_hp:
            self.hp += hp
            if hp < 0:
                plus_minus = "Minus"
                hp = abs(hp)
            pr(f"{plus_minus} {hp} HP!\n")
        else:
            randhp = randint(hp, higher_hp[0])
            self.hp += randhp
            if randhp < 0:
                plus_minus = "Minus"
                randhp = abs(randhp)
            pr(f"{plus_minus} {randhp} HP!\n")

    def skill_mod(self, skill, mod, *higher_mod): # !?
        pass

    def sell(self, buyer, *wares):
        sale_value = 0
        pr(f"Sell something to {buyer.name}:")
        pr(f"{C.YELLOW}0{C.END} · Stop trade.")
        for i, item in enumerate(self.inventory):
            pr(f"{C.YELLOW}{i + 1}{C.END} · {item.size_name} {item} (€{item.value})")
        while True:
            try:
                raw_inp = input()
                inp = raw_inp.replace(","," ").replace("."," ").replace(";"," ")
                sale_items = [(int(s) - 1) for s in inp.split() if s.isdigit()]
                if not sale_items:
                    pr(f"No items selected.")
                    pr("")
                    break
                else:
                    items_str = "items"
                    if len(sale_items) == 1:
                        items_str = "item"
                    pr(f"{C.GRAY}{C.CURSIVE}Sell {len(sale_items)} {items_str}{C.END}", end="")
                    for i in sorted(sale_items, reverse=True):
                        buyer.inventory.append(self.inventory[i]) # Add to buyer
                        sale_value += self.inventory[i].value
                        pr(f" · {C.GRAY}{self.inventory[i].size_name} {self.inventory[i]}{C.END}", end="")
                        del self.inventory[i] # Remove from seller
                    pr("\n")
                    # pr(f"{buyer.name.upper()}'S", end=" ")
                    # buyer.show_inv()
                    pr(f"Total value of the sale: {sale_value}")
                    self.credits += sale_value
                    pr(f"Your credits now: {self.credits}")
                    pr("")
                    break
            except:
                pr("")
                pr("Enter valid number(s) of item(s) to sell.")
                pr("")

    def catch(self, attempts, targets): # merge fish() & hunt()
        pass

    def fish(self, attempts):
        quarry = []
        hits = []
        for attempt in range(attempts):
            sleep(T.XL)
            hits.append(round(random(),2))
            if hits[attempt] >= 0.42:
                slain_animal = (Prey(attempt, Prey.fish_species))
                self.inventory.append(slain_animal)
                quarry.append(slain_animal)
                pr(f"Success ({hits[attempt]}) - {slain_animal.size_name} {slain_animal} caught!") # "Success"-variety
            else:
                pr("Fail.") # Variety! This triggers a lot!
        sleep(T.XXXL)
        pr(f"You had {attempts} nibbles and got {len(quarry)} fish!\n")
        sleep(T.XXL)

    def hunt(self, attempts):
        quarry = []
        hits = []
        for attempt in range(attempts):
            sleep(T.XS)
            hits.append(round(random(),2))
            if hits[attempt] >= 0.52:
                slain_animal = (Prey(attempt, Prey.game_species))
                self.inventory.append(slain_animal)
                quarry.append(slain_animal)
                pr(f"Success ({hits[attempt]}) - {slain_animal.size_name} {slain_animal} caught!") # "Success"-variety
            else:
                pr("Fail.") # Variety! This triggers a lot!
        sleep(T.XXXL)
        pr(f"You had {attempts} sightings and got {len(quarry)} animals!\n")
        sleep(T.XXL)

''' ITEM Class ''' # REMAKE INTO ANIMAL CLASS
class Item:
    def __init__(self, name):
        self.name = name
        # self.size = choice(Item.size_names)
        self.size = None
        self.size_name = "no .size_name"
        self.value = None # to calculate prize for trade

    def __repr__(self):
        return f"{self.size} {self.name}"

''' PREY Class '''
class Prey(Item):
    # Item.size_names.append("infant")
    size_names = ["rotten", "tiny", "infant", "famished", "very small", "young", "small", "slightly small", "average", "large", "very large", "massive", "enormous", "huge", "giant", "colossal"]

    ''' Species Pools ''' # Needs Value Multiplicators per Species!
    fish_species = ["Trout", "Pike", "Carp", "Catfish", "Tench",
                    "Bass", "Zander", "Eel", "Cod", "Crayfish"]
    game_species = ["Rabbit", "Wild Goose", "Turkey", "Mallard", "Deer","Squirrel",
                    "Boar", "Pheasant", "Grouse", "Partridge", "Weasel", "Muskrat"]
    nick_titles = ["Monster", "Uncle", "Señor", "King", "Lord", "Sweet",
                     "Maestro", "Silly", "Big", "Old Boy"]
    nicknames = ["Joey", "Steve", "Magnus", "Herman", "Fritz", "Hank", "Bob",
             "Al", "Otto", "Willie", "Tommy", "Ricky", "Dewy", "Georgie", "Olaf"]

    def __init__(self, name, species_pool):
        super().__init__(name)
        self.species_pool = species_pool
        self.species = choice(self.species_pool)
        self.title = ""
        self.size = randint(0,15) # Prey objects have random size
        self.size_name = Prey.size_names[self.size]
        self.is_giant = self.size >= 13
        self.is_puny = self.size < 3
        self.value_mod = round(uniform(0.85, 1.15), 2)
        if self.is_giant:
            self.value_mod = round(uniform(1.35, 1.75), 2) # Trophy Bonus
            if random() > 0.50:
                self.title = f"{choice(self.nick_titles)} "
            self.name = f"{self.title}{choice(self.nicknames)}"
        elif self.is_puny:
            self.value_mod = round(uniform(1.55, 1.95), 2)
        else:
            self.name = None
        self.value = int((self.size + 2) ** 2 * self.value_mod // 3) - 1

    def __repr__(self):
        if self.is_giant:
            return f"{self.species} '{self.name}'"
        else:
            return f"{self.species}"

''' EXAMPLE A '''
''' AREA '''
geryna = Area("Geryna")

''' CHARACTER & ITEMS '''
player = Character("Dan", "gate")
merchant = Character("Ando", "harbour")

''' NODES & CHOICES '''     # all choices '.', '!', etc. or not!
'''      STORY      '''
gate = Node(
    "City Gate", geryna,
    "Welcome to {self.area.name}. You're in front of the {self.name}")
gate_c1 = Choice(
    gate, "Try to catch some wild animals.",
    "woods", "pr('Let\\'s get the hunt on!')", "player.hunt(randint(2,5))","player.skill_mod(3,15)")
gate_c2 = Choice(
    gate, "Fish in a freshwater pond next to the harbour.",
    "pond", "player.fish(randint(2,7))")
sell_c3 = Choice(gate, "Sell some goods to the Merchant.", "gate", "pr('Sale!')", "player.sell(merchant, 0)")
woods = Node(
    "Woods", geryna,
    "The deep woods. Nothing much here yet.")
woods_c1 = Choice(
    woods, "Back to the city gate.",
    "gate")
pond = Node(
    "Fish Pond", geryna,
    "It's a beautiful spot and there seem to be plenty of fish but after a few hours you get tired.")
pond_c1 = Choice(
    pond, "Take a walk back through the woods.",
    "woods", "pr('A little workout does wonders!')", "player.hp_mod(2,6)")
pond_c2 = Choice(
    pond, "To the harbour!",
    "harbour")
harbour = Node(
    "Old Harbour", geryna,
    "The waves are breaking softly on the dock.")
harbour_c1 = Choice(
    harbour, "Show stats about your character.",
    "harbour", "player.show_stats()")
harbour_c2 = Choice(
    harbour, "Follow a small path back to the gate",
    "gate", "pr('You slip a couple of times!')", "player.hp_mod(-4,-1)")
harbour_c3 = Choice(
    harbour, "I really should go catch more fish!",
    "pond", "player.fish(randint(4,9))")

# DEFAULT CHOICES for certain Nodes · MUST be positioned between Nodes and .play()
for no in range (len(Node.instances)): # Add choice to all instances
    # Node.instances[no].next_node = Node.instances[no]
    inventory_choice = Choice(
        Node.instances[no], "Show Inventory.",
        None, "player.show_inv()")

''' START: first Node.play() '''
gate.play()
