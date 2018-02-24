import curses
import random

def generate_random_monster(startroom, curlevel):
    return GoldPile(startroom, curlevel)
    
class Loot:

    def __init__(self, char, color, startroom, curlevel):
        self.y     = startroom[0] + 1
        self.x     = startroom[1] + 1  
        self.curlevel = curlevel 

        self.char  = char   # single character 
        self.color = color  # curses.color_pair

        #  modifiers (can be positive or negative)
        self.lvl      = 0
        self.hp       = 0
        self.gld      = 0
        self.strength = 0
        self.speed    = 0
        self.agility  = 0

        # generate name from class name
        self.name  = str(self.__class__)

    def clear(self, stdscr):
        stdscr.addstr(self.y,self.x, ' ')

class GoldPile(Loot):
    def __init__(self, startroom, curlevel):
        Monster.__init__(self, '*', curses.color_pair(2), startroom, curlevel)
