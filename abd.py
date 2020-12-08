"""
A BORING DYSTOPIA
"""
from character import *

class Area:
    """ AREA Class """
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def __repr__(self):
        return f"{self.name}"

class Node:
    """ NODE Class """
    instances = []
    def __init__(self, area, name, txt, *args):
        self.area = area
        self.name = name
        self.txt = txt
        self.choices = []
        self.dcsn_idx = None
        self.next_node = None
        self.been_here = 0
        self.fam = ""
        self.time_passed = args[0] if args else 0
        Node.instances.append(self)

    def __repr__(self):
        return f"{self.name}" # ' in {self.area}'

    def play(self):
        """Main Method that calls upon the single parts"""
        self.node_prep()
        player.node = self
        player.location = self
        if player.path[-1] != self.name:
            player.path.append(self.name)
        # pr(f"You're {self.fam}at the {C.CYAN}{player.location.name}{C.END}.")
        self.been_here += 1
        self.print_node_txt()
        player.time += self.time_passed
        pr("")
        self.print_choices_txt()
        if not self.choices:
            return # return or quit()
        self.catch_one_choice_case()
        self.take_decision()
        # self.fx_fallout()
        # if merchant.credits < 0:
        #     pr(f"The Merchant is bankrupt. You win!")
        #     quit()
        self.play_next_node()

    def node_prep(self):
        if self.been_here >= 3:
            self.fam = "once more back again "
        elif self.been_here == 2:
            self.fam = "back again "
        elif self.been_here == 1:
            self.fam = "again "
        elif self.been_here == -1:
            self.fam = "still "
        else:
            self.fam = ""

    def print_node_txt(self):
        t = f"pr(f'{self.txt}')"
        node_txt_updated = compile(t, "new_node_txt", "exec")
        exec(node_txt_updated)

    # def check_no_of_choices()

    def print_choices_txt(self):
        for i, chc in enumerate(self.choices):
            if len(self.choices) == 1:
                c = f"pr(f'{C.YELLOW}·{C.END} {chc.txt}', end='')"
            else:
                c = f"pr(f'{C.YELLOW}{i + 1}{C.END} · {chc.txt}')"
            choice_txt_updated = compile(c, "new_choice_txt", "exec")
            exec(choice_txt_updated)

    def catch_one_choice_case(self):
        if len(self.choices) == 1:
            self.dcsn_idx = 0
            if self.choices[0].txt:
                while True:
                    try:
                        inp = input()
                        if inp == "" or inp == " " or inp == "0" or inp == "1":
                            break # Good Input, ready to continue
                        pr(f"Press 'Enter'.")
                    except ValueError:
                        pr("ValueError")
                oc = f"pr(f'{C.GRAY}{C.CURSIVE}{self.choices[self.dcsn_idx].txt}{C.END}')"
                choice_txt_updated = compile(oc, "new_decision_txt", "exec")
                exec(choice_txt_updated)
            else:
                pr("")
            player.time += self.choices[self.dcsn_idx].time_passed
            sleep(T.XS)
            pr("")


    def take_decision(self):
        if len(self.choices) != 1: # cos we run through this after catch_one_chc
            input_tries = 1 # including successful input
            punc_mark = "."
            while True:
                if input_tries >= 3:
                    punc_mark = "!"
                try:
                    self.dcsn_idx = (int(input("")) - 1)  # Decision Integer Check
                    if len(self.choices) > self.dcsn_idx > -1:
                        break # Good Input, ready to continue
                    pr(f"Enter number within choices{punc_mark}")
                    input_tries += 1
                except ValueError: # No Integer Exception
                    print(f"ValueError - Enter number{punc_mark}")
                    input_tries += 1
            sleep(0.07)
            c = f"pr(f'{C.GRAY}{C.CURSIVE}{self.choices[self.dcsn_idx].txt}{C.END}')"
            choice_txt_updated = compile(c, "new_decision_txt", "exec")
            exec(choice_txt_updated)
            player.time += self.choices[self.dcsn_idx].time_passed
            sleep(T.XS)
            pr("")
        else:
            pass

    def fx_fallout(self):
        self.choices[self.dcsn_idx].fx_repercussions()  # FX of Decision

    def play_next_node(self): # split into update_dcsn_idx & play; fx inbetween
        if self.choices[self.dcsn_idx].dest: # check if destination or None
            self.next_node = self.choices[self.dcsn_idx].dest
            this_node = str(self.choices[self.dcsn_idx].node.name)
            if self.next_node in this_node.lower():
                self.been_here = -1
                player.time -= self.time_passed
            self.fx_fallout()
            globals()[self.next_node].play() # Play NEXT NODE
        else: # NO NEXT_NODE
            self.been_here = -1
            player.time -= self.time_passed
            self.fx_fallout()
            self.play() # Play the SAME NODE AGAIN if no destination (def_choices)

class Choice:
    """ CHOICE Class """
    def __init__(self, node, visible, txt, dest, *args):
        self.node = node
        self.visible = True
        self.visible = visible
        if self.visible: node.choices.append(self)
        self.txt = txt
        self.dest = dest
        try:
            self.time_passed = args[0] if type(args[0]) == int else 0
        except IndexError:
            self.time_passed = 0
        self.fx = [effect for effect in args if type(effect) == str]
    def fx_repercussions(self):
        for effect in self.fx:
            compile(effect, "fx-c-name", "exec")
            exec(effect)

    def hide(self):
        self.visible = False
        if self in self.node.choices:
            self.node.choices.remove(self)

    def show(self):
        self.visible = True
        if not self in self.node.choices:
            self.node.choices.append(self)

# for no in range (len(Node.instances)):
#     """DEFAULT CHOICES · MUST be between Nodes and start.play()"""
#     show_inv_choice = Choice(
#         Node.instances[no], True, "Show Inventory.",
#         None, 0, "player.show_inv()")
#     show_path_choice = Choice(
#         Node.instances[no], True, "Show Path & Length",
#         None, 0, "pr_fx(f'Path ({len(player.path)}): {[i for i in player.path]}')")

''' AREAS, CHARACTERS & ITEMS '''
area1 = Area("AreaName")
player = Character("NoName", "first")
ando = Character("Ando", "first")

'''      STORY      '''
pr("""
=====================================
             MAIN TITLE
=====================================
Intro Name defined in Character class.
1st static Node in the player's path.
""")

n1 = Node(area1, "N1",
  "First real Node. Some text, maybe even two or three sentences? \\n"
  "Still - quite early first interaction wanted, no decision yet - just a confirmation to continue.")
n1c1 = Choice(n1, True,
              "First Choice and its text.",
              "n1")
n1c2 = Choice(n1, True,
              "Second Choice is even nicer!",
              "n2", "player.show_stats()")

n2 = Node(area1, "N2",
          "Second Node. Coming from n1c2!")

n1.play()
