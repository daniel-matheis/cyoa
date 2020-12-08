""" 
colors.py: TIME, COLORS, NAMES, ... 
"""

''' T Class (Time & Tempo) '''
class T:    # all in seconds
    PERCENT   =    0.99     # 1.00 for Original Time of Pauses
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
    
class N:
    """PRE-NAMES"""
    f = ["Celine", "Josephine", "Alena", "Lauren", "Isabel", "Tamina", "Beth"]
    m = ["Paul", "Alan", "Lawrence", "Bernhard", "Henry", "Mark", "Michael"] 
    
class FN:
    """FAMILY NAMES"""
    n = ["Smith", "van den Kook", "Mayer", "Dunhill", "Hunter", "Ashcroft"]