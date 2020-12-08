""" item.py """
from random import *

class Item:
    """ ITEM Class """
    size_names = ['regular', 'tiny', 'very small', 'small',
              'large', 'very large', 'huge']

    def __init__(self, name):
        self.name = name
        self.size = 0 # default is 'regular'; choice(Item.size_names) for random
        self.size_name = Item.size_names[self.size]
        self.value = 0
        self.status = None # f.e. 'lovely' becomes 'torn'

    def __repr__(self):
        return f"{self.name}"

class Prey(Item):
    """ PREY Class """
    size_names = ['rotten', 'infant', 'tiny', 'famished', 'very small', 'young', 'small', 'slightly small', 'regular', 'large', 'fat', 'very large', 'massive', 'huge', 'giant', 'colossal']

    """ Species Pools """ # Needs Value Multiplicators per Species!
    fish_species = ['Trout', 'Pike', 'Carp', 'Catfish', 'Tench',
                    'Bass', 'Zander', 'Eel', 'Cod', 'Crayfish']
    game_species = ['Rabbit', 'Wild Goose', 'Turkey', 'Mallard', 'Deer','Squirrel',
                    'Boar', 'Pheasant', 'Grouse', 'Partridge', 'Weasel', 'Muskrat']
    nick_titles = ['Monster', 'Uncle', 'Señor', 'King', 'Lord', 'Sweet',
                     'Maestro', 'Silly', 'Big', 'Old Boy']
    nicknames = ['Joey', 'Steve', 'Magnus', 'Herman', 'Fritz', 'Hank', 'Bob',
             'Al', 'Otto', 'Willie', 'Tommy', 'Ricky', 'Dewy', 'Georgie', 'Olaf']

    def __init__(self, name, species_pool):
        super().__init__(name)
        self.species_pool = species_pool
        self.species = choice(self.species_pool)
        self.title = ""
        self.size = randint(0,15) # Prey objects have random size
        self.size_name = Prey.size_names[self.size]
        self.is_giant = self.size >= 13
        self.is_young = self.size == 5
        self.is_infant = self.size == 1
        self.is_puny = self.size < 3
        self.value_mod = round(uniform(0.85, 1.15), 2)
        if self.is_giant:
            self.value_mod = round(uniform(1.35, 1.75), 2) # Trophy Bonus
            if random() > 0.50:
                self.title = f"{choice(self.nick_titles)} "
            self.name = f"{self.title}{choice(self.nicknames)}"
        elif self.is_young:
            self.value_mod = round(uniform(1.55, 1.95), 2)
        elif self.is_infant:
            self.value_mod = round(uniform(2.75, 3.95), 2)
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