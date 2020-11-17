""" Choose Your Own Adventure Node-Choice-FX System """
import os
from random import *

''' Clear the screen '''
def clear_screen():
    os.system('cls')

''' Print '''
def pr(txt, **kwargs):
    print(txt, **kwargs)

''' C Class (Colors) '''
class C:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

''' NODE Class '''
class Node:
    def __init__(self, name, area, txt):
        self.name = name
        self.area = area
        self.txt = txt
        self.choices = []
        self.decision = None
        self.next_node = None

    def __repr__(self):
        return f"{self.name} in {self.area}"

    def play(self):
        player.node = self
        player.location = self.name
        pr(f"You're at the {C.DARKCYAN}{player.location}{C.END}")
        self.node_text_update_and_print()
        self.choices_update_and_print()
        if not self.choices:
            return # or quit()
        self.take_decision()
        self.fx_fallout()
        self.play_next_node()

    def node_text_update_and_print(self):
        t = f'pr(f"{self.txt}")'
        new_txt = compile(t, "New_txt", "exec")
        exec(new_txt)  # Print Node Text

    def choices_update_and_print(self):
        for i, chc in enumerate(self.choices):  # Print all Choices Texts
            c = f'pr(f"{i + 1}) {chc.txt}")'
            new_choice_txt = compile(c, "New_Choice_txt", "exec")
            exec(new_choice_txt)

    def take_decision(self):
        input_tries = 1 # including successful input
        punc_mark = "."
        while True:
            if input_tries >= 3:
                punc_mark = "!"
            try:
                self.decision = int(input(""))  # Decision Integer Check
                if len(self.choices) >= self.decision > 0:  # Decision in Choices Check
                    break
                pr(f"Enter number within choices{punc_mark}")
                input_tries += 1
            except ValueError: # No Integer Exception
                print(f"ValueError - Enter number{punc_mark}")
                input_tries += 1
        pr("")

    def fx_fallout(self):
        self.choices[self.decision - 1].fx_repercussions()  # FX of Decision

    def play_next_node(self):
        self.next_node = self.choices[self.decision - 1].dest # Determine NEXT NODE
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
        self.inventory = []

    def show_stats(self):
        pr(f"HP: {self.hp}")

    def show_inv(self):
        pr(f"Inventory ({len(self.inventory)}):", end=" ")
        for item in self.inventory:
            pr(item, end=" · ")
        pr("\n")
        # pr(self.__dict__)

    def hp_plus(self, hp, *args):
        if not args:
            self.hp += hp
            pr(f"Plus{hp} HP!\n")
        else:
            randhp = randint(hp, args[0])
            self.hp += randhp
            pr(f"Plus {randhp} HP!\n")

    def fish(self, number):
        pr(f"{number} Fish caught!\n")
        for i in range(number):
            self.inventory.append(Fish(i))

''' ITEM Class '''
class Item:
    sizes = ["small", "medium", "large", "enormous"]
    def __init__(self, name):
        self.name = name
        self.size = choice(Item.sizes)

    def __repr__(self):
        return f"{self.size} {self.name}"

class Fish(Item):
    names = ["Trout", "Pike", "Carp", "Wels Catfish", "Tench", "Bass", "Zander"]
    nicknames = ["Joey", "Sad Steve", "Bobby D", "Uncle Herman", "Popeye", "Hank"]
    def __init__(self, name):
        super().__init__(name)
        self.name = choice(self.names)
        if self.size == "enormous":
            self.name = f'{self.name} ("{choice(self.nicknames)}")'

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
# fish = Fish()

''' NODES & CHOICES '''
gate = Node(
    "City Gate", geryna,
    "Welcome to {self.area.name}. You're in front of the {self.name}")
# gate.city = geryna
gate_c1 = Choice(
    gate, "Hunt rabbits.",
    "woods", "pr('Rabbit!')", "player.hp_plus(3,15)") # random hp+
gate_c2 = Choice(
    gate, "Fish in a pond inside.",
    "pond", "player.fish(randint(1, 9))") # random catch
woods = Node(
    "Woods", geryna,
    "The deep woods.")
woods_c1 = Choice(
    woods, "Back to the city gate.",
    "gate")
pond = Node(
    "Fish Pond", geryna,
    "The fish pond is beautiful.")
pond_c1 = Choice(
    pond, "Hunt in the woods.",
    "woods", "pr('A little workout does wonders!')", "player.hp_plus(2,6)") # fixed hp+
pond_c2 = Choice(
    pond, "To the harbour!",
    "harbour")
harbour = Node(
    "City Harbour", geryna,
    "The waves are breaking softly on the dock.")
harbour_c1 = Choice(
    harbour, "Show stats & inventory",
    "harbour", "player.show_stats()", "player.show_inv()")
gate.play()