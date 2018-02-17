import curses
import random
import npc

class Hero(npc.Monster):

    def __init__(self, curlevel):
        
        npc.Monster.__init__(self, '@', curses.color_pair(4), curlevel.start, curlevel)

        self.lvl = 0
        self.exp = 0
        self.gld = 0

        self.hp = 100 

    def reset_start(self):
        self.y = self.curlevel.start[0]
        self.x = self.curlevel.start[1]

    def reset_exit(self):
        self.y = self.curlevel.exity
        self.x = self.curlevel.exitx+1

    def display(self, stdscr):
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(self.y,self.x,self.char, self.color)
        stdscr.attroff(curses.A_BOLD)

    def move(self, k):
        if k == curses.KEY_DOWN:
            if self.curlevel.map[self.y + 1][self.x] == ' ':
                self.y = self.y + 1
        elif k == curses.KEY_UP:
            if self.curlevel.map[self.y - 1][self.x] == ' ':
                self.y = self.y - 1
        elif k == curses.KEY_RIGHT:
            if self.curlevel.map[self.y][self.x + 1] == ' ':
                self.x = self.x + 1
        elif k == curses.KEY_LEFT:
            if self.curlevel.map[self.y][self.x - 1] == ' ':
                self.x = self.x - 1

    def display_hud(self, stdscr):
        stdscr.addstr(0, 0, "+-------------------------------------+", curses.color_pair(4)) 
        stdscr.addstr(1, 0, "|lvl:%3d exp:%6d gold:%6d hp:%3d|" % \
           (self.lvl,self.exp,self.gld, self.hp), curses.color_pair(4)) 
        stdscr.addstr(2, 0, "+-------------------------------------+", curses.color_pair(4)) 
