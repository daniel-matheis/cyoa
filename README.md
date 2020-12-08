A BORING DYSTOPIA
=================
"A Boring Dystopia" is a Python-based COYA written by Daniel Matheis.
CYOA stands for Choose Your Own Adventure - Gamebooks popular in the 80s and 90s.
Instead of a linear story the user is in control of where to go and what to do next.
With Python there are many more possibilities than with a book, dice, pencil and rubber.

First though Nodes with their Text and possible Choices with their Texts, Destination Nodes and Outcomes have to be connected to make it all work. Here a first try to make writing a somewhat complex CYOA more elegant and fun.

-----------------

Nov 17th, 2020
All systems running. 300 lines including example.

-----------------

Nov 23rd, 2020
Split into abd.py for the main node functionality and screenplay itself plus 4 modules:
1. character.py - character and license classes
2. item.py - for the item classes and their children
3. colors.py - for colors and all other default settings
4. utils.py - for all special functions
5. (ship.py - not yet integrated) - for all travelling, resource hunting and fighting with a ship (its own mini-game)
