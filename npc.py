import curses
import random

class Monster:

    def __init__(self, char, color, startroom, curlevel, speed = 0):
        self.y     = startroom[0] + 1
        self.x     = startroom[1] + 1  
        self.curlevel = curlevel 

        self.char  = char   # single character 
        self.color = color  # curses.color_pair
        self.speed = speed  # 0 is the faster
        self.speedtimer = self.speed

        self.lvl = 0
        self.hp  = 10
        self.gld = 10

        # generate name from class name
        self.name  = str(self.__class__)

    def display(self, stdscr):
        stdscr.addstr(self.y,self.x,self.char, self.color)

    def clear(self, stdscr):
        stdscr.addstr(self.y,self.x, ' ')

    def debug_hud(self, stdscr, y,x):
        stdscr.addstr(y, x, 'self.y %d' % (self.y),  self.color) 

    def move(self, hero):
        if self.speedtimer:
            self.speedtimer -= 1
        
        if not self.speedtimer:
            self.speedtimer = self.speed
            return True

        return False    

    def _simple_track_hero(self, hero, shortcut = False):

        yoffset = 0
        xoffset = 0
        
        if hero.y < self.y:
            yoffset = -1 
        elif hero.y > self.y:    
            yoffset =  1 

        if self.y + yoffset < 0 or self.y + yoffset > len(self.curlevel.map):
            yoffset = 0
        if self.curlevel.map[self.y + yoffset][self.x] == ' ':
            self.y = self.y + yoffset

        # If this monster can't take shortcuts and it already moved in
        # the Y axes, then don't try and move on the X axis
        if not shortcut and yoffset:
            return

        if hero.x < self.x:
            xoffset = -1 
        elif hero.x > self.x:    
            xoffset =  1 

        if self.x + xoffset < 0 or self.x + xoffset > len(self.curlevel.map[self.y]):
            xoffset = 0
        if self.curlevel.map[self.y][self.x + xoffset] == ' ':
            self.x = self.x + xoffset
        

    def _brownian(self):

        # pick a random direction
        yorx = random.randint(0,1)

        if yorx:
            yoffset = random.randint(-1,1)
            if self.y + yoffset < 0 or self.y + yoffset > len(self.curlevel.map):
                yoffset = 0
            if self.curlevel.map[self.y + yoffset][self.x] == ' ':
                self.y = self.y + yoffset
        else:        
            xoffset = random.randint(-1,1)
            if self.x + xoffset < 0 or self.x + xoffset > len(self.curlevel.map[self.y]):
                xoffset = 0
            if self.curlevel.map[self.y][self.x + xoffset] == ' ':
                self.x = self.x + xoffset

    def can_attack(self, hero):
        
        dy = abs(self.y - hero.y)
        dx = abs(self.x - hero.x)

        if dy <= 1 and dx <= 1: 
            return not (dy and dx) # only return true if directly adjacent
                                   # not caddy corner
        return False    

    def attack(self, hero, stdscr):
        my, mx = stdscr.getmaxyx()
        stdscr.addstr(my - 1, mx - 40, "%s attacks! " % (self.name), self.color)

        hero.gld += self.gld
        hero.exp += self.lvl + 1

        return True # let's just assume the hero kills this monster
        
    
class RedBat(Monster):

    def __init__(self, startroom, curlevel):
        Monster.__init__(self, '~', curses.color_pair(2), startroom, curlevel)

    def move(self, hero):
        if not Monster.move(self, hero):
            return
        Monster._brownian(self)

# These guyes are the worst.  They will track the hero anywhere on the
# map, they take shortcuts and they have the fastest speed
class YellowStinger(Monster):

    def __init__(self, startroom, curlevel):
        Monster.__init__(self, '+', curses.color_pair(7), startroom, curlevel, 0)

    def move(self, hero):
        if not Monster.move(self, hero):
            return
        Monster._simple_track_hero(self, hero, shortcut=True)

class HungryBear(Monster):

    def __init__(self, startroom, curlevel):
        Monster.__init__(self, '&', curses.color_pair(5), startroom, curlevel, speed = 3)

    def move(self, hero):
        if not Monster.move(self, hero):
            return

        eyesight = 15 # if within 10 spaces, track hero.  Otherwise just
                      # meander
        if abs(hero.y - self.y) < eyesight and abs(hero.x - self.x) < eyesight:
            Monster._simple_track_hero(self, hero)
        else:    
            Monster._brownian(self)
