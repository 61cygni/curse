import os
import curses
import message 
import curseconf

def draw_main_title(stdscr):
    
    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = "Curse"[:width-1]
    
    subtitle = "Press <space> to enter ..."[:width-1]
    if os.path.exists(curseconf.SAVE_FILE) and os.path.isfile(curseconf.SAVE_FILE) : 
        subtitle = "<l> load game <n> new game ..."[:width-1]

    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_y = int((height // 2) - 2)

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    stdscr.addstr(height - (height/3), start_x_subtitle, subtitle)
    
def draw_exit_screen(stdscr):
    
    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = "Ar you sure you want to quit?"[:width-1]
    subtitle = "y = quit, n = resume, m = main menu"[:width-1]

    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_y = int((height // 2) - 2)

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    stdscr.addstr(height - (height/3), start_x_subtitle, subtitle)


def draw_intro_sequence(stdscr):

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    first_message = \
"""\
This story takes place a long time ago.  Like, a really long time ago.
Or perhaps not so long in fact.  I always seem to forget. 
In any case, our hero's name is bip.

Sat hello to bip
"""
    subtitle = "Press <SPACE> to Continue ..."[:width-1]

    scroll = message.create_scroll(first_message)
    message.animate_scroll(stdscr, scroll)

    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    stdscr.addstr(height - (height/3), start_x_subtitle, subtitle)


