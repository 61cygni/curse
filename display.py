import curses

def hero_hud_compact(stdscr):
    stdscr.addstr(0, 0, "+----------------------------+", curses.color_pair(4)) 
    stdscr.addstr(1, 0, "|lvl:%d Exp:%d Gld:%d HP:%s|" % (1,2,3), curses.color_pair(4)) 
    stdscr.addstr(2, 0, "+----------------------------+", curses.color_pair(4)) 

def dungeon_hud_compact(stdscr, level):
    height, width = stdscr.getmaxyx()

    starty = height - 3

    stdscr.addstr(starty    , 0, "+-----------------+", curses.color_pair(2)) 
    stdscr.addstr(starty + 1, 0, "|dungeon lvl:%3d  |" % (level), curses.color_pair(2)) 
    stdscr.addstr(starty + 2, 0, "+-----------------+", curses.color_pair(2)) 

# --
# The lower right hand corner of the screen is going to be used for all
# status messages so implement a message queue that will rate limit them
# to the screen 
# --

import Queue
import time 

class ActionMessage:

    def __init__(self, stdscr):
        self.stdscr  = stdscr
        self.queue   = Queue.Queue()
        self.cur_msg = None  # current message on display
        self.time_d  = 0     # time current message was displayed

    def add(self, msg, displaytime):
        self.queue.put((msg, displaytime))
    
    def run(self):

        # check to see if the current message has timed out
        if self.cur_msg:
            if time.time() - self.time_d > self.cur_msg[1]:
                self.clear_message()
                self.cur_msg = None
                self.time_d = 0
                # fall through
            else:
                return # current message hasn't time out


        if not self.queue.empty():
            self.cur_msg = self.queue.get()
            self.time_d  = time.time()
            self.display_message()

    def display_message(self):
        my, mx = self.stdscr.getmaxyx()
        self.stdscr.addstr(my - 1, mx - 40, "%s " % (self.cur_msg[0]))

    def clear_message(self):
        my, mx = self.stdscr.getmaxyx()
        self.stdscr.addstr(my - 1, mx - 40, " "*39)
        
