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
