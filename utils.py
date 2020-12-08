""" . UTILS """
import os
# from numpy import random as npr
# import numpy as np

''' Clear the screen '''
def clear_screen():
    os.system('cls')

''' Print '''
def pr(txt, **kwargs):
    print(txt, **kwargs)

"""FX Print"""
def pr_fx(txt):
    print(txt, end='\n\n')

def gauss_random(base, spread_limiter, rolls):
    """
    Take skill base value, spread_limiter and no. of rolls and give a random, min or max pick to decide the skill test
    base = 10
    spread_limiter = 4 # 4 slightly volatile; 6 medium; 8 pretty stable
    rolls = 10 # default & more/less for buffs, edge, ...
    """
    a = (npr.normal(loc=base, scale=base/spread_limiter, size=rolls))
    np.round_(a, decimals = 0, out = a)
    pr(a)
    pr(f"scale: {round(base/spread_limiter, 1)}")
    pr(f"max: {max(a)}") # player can give f.e. "edge" to choose the unknown max roll in a test
    pr(f"min: {min(a)}") # pretty surely a fail; penalty for ... ?
    pr(f"avg: {round(sum(a)/len(a),1)}") # avg
    pr(f"res: {round(npr.choice(a))}")
#
# gauss_random(7,3.5,10)
# gauss_random(10,5,10)
#
# with open('untracked/log.txt', 'r') as f:
#     # f.write('abc')
#     for line in f:
#         print(line, end='')
