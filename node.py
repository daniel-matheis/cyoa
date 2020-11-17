""" CYOA Node-Choice-FX System """

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
class T:
    XXS     = 0.29
    XS      = 0.47
    S       = 0.56
    M       = 0.65
    L       = 0.74
    XL      = 0.83
    XXL     = 0.92
    XXXL    = 1.10

''' C Class (Colors '''
class C:
    BLACK           = "\033[30m"
    RED             = "\033[31m"
    GREEN           = "\033[32m"
    YELLOW          = "\033[33m"
    BLUE            = "\033[34m"
    PURPLE          = "\033[35m"
    CYAN            = "\033[36m"
    GRAY            = "\033[90m"
    LIGHTGRAY       = "\033[37m"
    LIGHTRED        = "\033[91m"
    LIGHTGREEN      = "\033[92m"
    LIGHTYELLOW     = "\033[93m"
    LIGHTBLUE       = "\033[94m"
    LIGHTPURPLE     = "\033[95m"
    LIGHTCYAN       = "\033[96m"
    WHITE           = "\033[97m"
    BOLD            = "\033[1m"
    CURSIVE         = "\033[3m"
    UNDERLINE       = "\033[4m"
    END             = "\033[0m" # Reset All

''' NODE Class '''
class Node:
    def __init__(self, name, area, txt):
        self.name = name
        self.area = area
        self.txt = txt
        self.choices = []
        self.decision = None
        self.next_node = None
        self.been_here = False
        self.familiarity = ""

    def __repr__(self):
        return f"{self.name} in {self.area}"

    def play(self): # Main Method that calls upon the single parts
        self.node_prep()
        player.node = self
        player.location = self.name
        player.visited_nodes.append(self)
        pr(f"You're {self.familiarity}at the {C.CYAN}{player.location}{C.END}.")
        self.been_here = True
        self.print_node_txt()
        self.print_choices_txt()
        # if not self.choices: # needed if no choices in node
        #     return # return or quit()
        self.catch_one_choice_case()
        self.take_decision()
        self.fx_fallout()
        self.play_next_node()

    def node_prep(self):
        if self.been_here and self.familiarity == "back again ":
            self.familiarity = "once more back again "
        elif self.been_here and self.familiarity == "back ":
            self.familiarity = "back again "
        elif self.been_here:
            self.familiarity = "back "

    def print_node_txt(self):
        t = f'pr(f"{self.txt}")'
        node_txt_updated = compile(t, "new_node_txt", "exec")
        exec(node_txt_updated)  # Print Node Text

    def print_choices_txt(self):
        for i, chc in enumerate(self.choices):  # Print all Choices Texts
            c = f'pr(f"{i + 1} · {chc.txt}")'
            choice_txt_updated = compile(c, "new_choice_txt", "exec")
            exec(choice_txt_updated)

    def catch_one_choice_case(self):
        if len(self.choices) == 1:
            self.decision = 1
            while True:
                try:
                    inp = input()
                    if inp == "" or inp == "1":
                        break
                    pr(f"Press enter or choice number.")
                except ValueError:
                    pr("ValueError")
            pr(f"{C.GRAY}{C.CURSIVE}{self.choices[self.decision - 1].txt}{C.END}")
            sleep(0.48)
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
                    break
                pr(f"Enter number within choices{punc_mark}")
                input_tries += 1
            except ValueError: # No Integer Exception
                print(f"ValueError - Enter number{punc_mark}")
                input_tries += 1
        sleep(0.07)
        pr(f"{C.GRAY}{C.CURSIVE}{self.choices[self.decision - 1].txt}{C.END}")
        sleep(0.48)
        pr("")

    def fx_fallout(self):
        self.choices[self.decision - 1].fx_repercussions()  # FX of Decision

    def play_next_node(self):
        self.next_node = self.choices[self.decision - 1].dest
        globals()[self.next_node].play() # Play NEXT NODE

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
class Character:
    def __init__(self, name, location):
        self.name = name
        self.hp = 50
        self.location = location
        self.node = None
        self.visited_nodes = []
        self.inventory = []

    def show_stats(self):
        pr(f"HP: {self.hp}")

    def show_inv(self):
        pr(f"Inventory ({len(self.inventory)}):", end=" ")
        for item in self.inventory:
            pr(item, end=" · ")
        pr("\n")

    def hp_mod(self, hp, *higher_hp):
        if not higher_hp:
            self.hp += hp
            pr(f"Plus{hp} HP!\n")
        else:
            randhp = randint(hp, higher_hp[0])
            self.hp += randhp
            pr(f"Plus {randhp} HP!\n")

    def skill_mod(self, skill, value, *highervalue): # !?
        pass

    def fish(self, attempts):
        quarry = []
        hits = []
        for i in range(attempts):
            sleep(T.XL)
            hits.append(round(random(),2))
            if hits[i] >= 0.45:
                q = (Prey(i, Prey.fish_species))
                self.inventory.append(q)
                quarry.append(q)
                pr(f"Success ({hits[i]}) - {str(q).title()} caught!")
            else:
                pr("Fail.")
        sleep(T.XXXL)
        pr(f"You had {attempts} nibbles and got {len(quarry)} fish!\n")
        sleep(T.XXL)

    def hunt(self, attempts):
        quarry = []
        hits = []
        for i in range(attempts):
            sleep(T.XS)
            hits.append(round(random(),2))
            if hits[i] >= 0.65:
                q = (Prey(i, Prey.game_species))
                self.inventory.append(q)
                quarry.append(q)
                pr(f"Success ({hits[i]}) - {str(q).title()} caught!")
            else:
                pr("Fail.")
        sleep(T.XXXL)
        pr(f"You had {attempts} sightings and got {len(quarry)} animals!\n")
        sleep(T.XXL)

''' ITEM Class '''
class Item:
    sizes = ["small", "average", "large", "gigantic"]
    def __init__(self, name):
        self.name = name
        self.size = choice(Item.sizes)

    def __repr__(self):
        return f"{self.size} {self.name}"

''' PREY Class '''
class Prey(Item):
    fish_species = ["Trout", "Pike", "Carp", "Catfish", "Tench", "Bass", "Zander"]
    game_species = ["Rabbit", "Duck", "Turkey", "Mallard", "Deer", "Boar", "Pheasant"]
    nick_prefixes = ["Sad", "Uncle", "Señor", "King", "Lord", "Sweet", "Maestro", "Silly", "Big"]
    nicks = ["Joey", "Steve", "Magnus", "Herman", "Popeye", "Hank", "Bob", "Al", "Otto"]
    def __init__(self, name, species):
        super().__init__(name)
        self.prfx = ""
        self.species = species
        self.name = choice(self.species)
        if self.size == "gigantic":
            if random() > 0.50:
                self.prfx = choice(self.nick_prefixes) + " "
            self.name = f'{self.name} ("{self.prfx}{choice(self.nicks)}")'

''' AREA Class '''
class Area:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def __repr__(self):
        return f"{self.name}"

''' CHARACTER & ITEMS '''
geryna = Area("Geryna")
player = Character("Dan", "Gate")

''' NODES & CHOICES '''
gate = Node(
    "City Gate", geryna,
    "Welcome to {self.area.name}. You're in front of the {self.name}")
gate_c1 = Choice(
    gate, "Try to catch some wild animals.",
    "woods", "pr('Let\\'s get the hunt on!')", "player.hunt(randint(2,5))","player.skill_mod(3,15)")
gate_c2 = Choice(
    gate, "Fish in a freshwater pond next to the harbour.",
    "pond", "player.fish(randint(2,7))")
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
    "City Harbour", geryna,
    "The waves are breaking softly on the dock.")
harbour_c1 = Choice(
    harbour, "Show stats & inventory",
    "harbour", "player.show_stats()", "player.show_inv()")
harbour_c2 = Choice(
    harbour, "Follow a small path back to the gate",
    "gate", "pr('You slip a couple of times!')", "player.hp_mod(-4,-1)")
harbour_c3 = Choice(
    harbour, "I really should go catch more fish!",
    "pond", "player.fish(randint(4,9))")
gate.play()