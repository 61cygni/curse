import curses
import random
import sys
import npc

brick = '#'
space = ' '

# --
# Blit open space over the level at (y1, x1, y2, x2)
# --

def blit_rectangle(coords, level):
    for i in range(coords[0], coords[2]):
        for j in range (coords[1], coords[3]):
            if i >= len(level) or j >= len(level[i]):
                continue
            level[i][j] = space
    
    
def create_random_room(maxyx, hallway = False):

    maxy = maxyx[0]
    maxx = maxyx[1]
    
    # create a random size for room with min size 4x4 and max size 1/4
    # of the screen
    sizey = random.randint(2, int(maxy / 6)) 
    sizex = random.randint(2, int(maxx / 6))

    if hallway: 
        if random.randint(0,1) > 0:
            sizey = random.randint(2, int(maxy / 2)) 
            sizex = random.randint(2, 4)
        else:
            sizex = random.randint(2, int(maxx / 2)) 
            sizey = random.randint(2, 4)
            

    # create a random starting location for room leave 1/8th of the room
    # for buffer

    paddingy = int(maxy/16)
    paddingx = int(maxx/16)

    starty = paddingy + random.randint(0, int(maxy - (paddingy*2 + int(sizey)) ) -1)
    startx = paddingx + random.randint(0, int(maxx - (paddingx*2 + int(sizex)) ) -1)
    
    return((starty,startx,starty+sizey,startx+sizex))

# XXX there has to be an easier way to solve this
def room_overlap(r1, r2):

    # These assignments are just for readability
    r1y1 = r1[0]
    r1x1 = r1[1]
    r1y2 = r1[2]
    r1x2 = r1[3]

    r2y1 = r2[0]
    r2x1 = r2[1]
    r2y2 = r2[2]
    r2x2 = r2[3]
    
    if r1y1 < r2y1:
        if r1x1 < r2x1: # r1's y and X is less
            return r1y2 > r2y1 and r1x2 > r2x1 
        else:    # r1's Y is less and X is greater
            return r2y1 < r1y2 and r2x2 > r1x1
    else:        
        if r1x1 < r2x1: # r1's y is greater and X is less
            return r1y1 < r2y2 and r1x2 > r2x1 
        else:   # r1's y is greater and X is greater 
            return r2y2 > r1y1 and r2x2 > r1x1
        

class Level:

    def __init__(self, stdscr):
        self.__create_level(stdscr.getmaxyx())
        self.__add_start() # Must be called after create_level!
        self.__add_exit()
        self.__create_monsters()
    
# -- 
# Create random level with hero starting position 
# -- 

    def __create_level(self, maxyx):

        level = []

        # Fill level full of bricks to start
        for i in range(1, maxyx[0]):
            level.append(bytearray(brick * maxyx[1]))

        maxy = maxyx[0]
        maxx = maxyx[1]

        rooms = []

        # Create the starting room.  We'll put the hero here
        eve = create_random_room(maxyx)
        blit_rectangle(eve, level)

        rooms.append(eve)

        # Create a minimum of 20 rooms and a maximum of 60

        accepted_rooms = 0

        # interesting levels have between 20 and 150 rooms
        TOTAL_ROOMS = random.randint(20,150) 
        HALLWAY_BIAS = 10 # Higher number means more hallways

        # The basic algorithm here is to randomly generate rooms and
        # hallways and then make sure they're connected to the existing room
        # map.  If not, we discard and retry.  This is clearly highly
        # inefficient, but it doesn't matter since this happens during
        # setup time, not gameplay

        while accepted_rooms < TOTAL_ROOMS:

            is_hallway = False
            if  random.randint(0, HALLWAY_BIAS) > 0 :
                is_hallway = True
            room    = create_random_room(maxyx, is_hallway)
            for old_room in rooms:
                if room_overlap(room, old_room):
                    accepted_rooms += 1
                    rooms.append(room)
                    blit_rectangle(room, level)
                    break
            

        self.start = eve

        self.rooms = rooms

        self.map = []
        for line in level:
            self.map.append(line.decode("utf-8"))

    def __create_monsters(self):
        self.monsters = []

        for i in range(0, random.randint(5,20)):
            monster_start = self.rooms[random.randint(0, len(self.rooms) - 1)]
            self.monsters.append(npc.RedBat(monster_start, self))

        for i in range(0, random.randint(1,3)):
            monster_start = self.rooms[random.randint(0, len(self.rooms) - 1)]
            self.monsters.append(npc.YellowStinger(monster_start, self))

        for i in range(0, random.randint(1,3)):
            monster_start = self.rooms[random.randint(0, len(self.rooms) - 1)]
            self.monsters.append(npc.HungryBear(monster_start, self))

# -- 
# Place exit in a random room  
# -- 
    def __add_exit(self):
        exit_room     = self.rooms[random.randint(0, len(self.rooms) - 1)]
        self.exity    = random.randint(exit_room[0],exit_room[2] - 1)
        self.exitx    = random.randint(exit_room[1],exit_room[3] - 1)
        self.exitchar = 'V'

    def __add_start(self):
        self.starty = self.start[0] + 1
        self.startx = self.start[1] + 1
        self.startchar = '^'

    def draw_level(self, stdscr):    
            line = 0
            for row in self.map:
                stdscr.addstr(line, 0, row, curses.color_pair(6) ) 
                line += 1

    def draw_monsters(self, stdscr, myhero):    
        # Move and draw all monsters
        for monster in self.monsters:
            monster.clear(stdscr)
            monster.move(myhero)
            monster.display(stdscr)
            
    def draw_exit(self, stdscr, myhero):    
            stdscr.addstr(self.exity, self.exitx,    self.exitchar, curses.color_pair(10))
    def draw_entrance(self, stdscr, myhero):    
            stdscr.addstr(self.starty, self.startx, self.startchar, curses.color_pair(9))

