import time
import curses

#   ____________________
# @=____________________=@
#   \                  \
#   |                  |
#   |                  |
#   | This is a scroll |
#   \__________________\
#  @=__________________=@


def create_scroll (printme) :

    lines = printme.split('\n')
    max_len = 0
    for line in lines:
        if len(line) > max_len :
            max_len = len(line) 

    scroll = []
    scroll.append( "  _"+'_'*max_len+"__")
    scroll.append( "@=_"+'_'*max_len+"__=@")
    scroll.append( "  \\"+' '*max_len+"  \ ")
    scroll.append( "  |"+' '*max_len+"  | ")
    for line in lines:
        scroll.append( "  | "+line+' '*(max_len - len(line))+" | ")
    scroll.append( "  |"+' '*max_len+"  | ")
    scroll.append( "  |"+' '*max_len+"  | ")
    scroll.append( "  \\"+'_'*max_len+"__\ ")
    scroll.append( "@=_"+'_'*max_len+"__=@")
    return scroll

def animate_scroll(stdscr, scroll, speed=0):
    
    maxlen = len(scroll)
    for i in range(0,maxlen-4): 
        ypos = 2
        stdscr.clear()
        stdscr.addstr(ypos, 10, scroll[0])
        ypos += 1
        stdscr.addstr(ypos, 10, scroll[1])
        ypos += 1
        for midsection in scroll[2:i]:
            stdscr.addstr(ypos, 10, midsection) 
            ypos += 1
        stdscr.addstr(ypos, 10, scroll[maxlen-2])
        ypos += 1
        stdscr.addstr(ypos, 10, scroll[maxlen-1])
        ypos += 1

        stdscr.refresh()
        time.sleep(.1)
            

def create_dialog (printme) :

    lines = printme.split('\n')
    max_len = 0
    for line in lines:
        if len(line) > max_len :
            max_len = len(line) 

    dialog = []
    dialog.append( "+-"+'-'*max_len+"-+")
    for line in lines:
        dialog.append( "| "+line+' '*(max_len - len(line))+" |")
    dialog.append( "+-"+'-'*max_len+"-+")
    return dialog

def display_monster_killed(stdscr, monster) :
    height, width = stdscr.getmaxyx()

    printme = "You killed a %s!" %(monster.name)

    dialog = create_dialog(printme)

    y = (height / 2) - 2
    x = (width / 2) - (len(dialog[0]) / 2)
    for line in dialog:
        stdscr.addstr(y, x, line, curses.color_pair(8))
        y += 1
