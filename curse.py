import sys,os
import getopt
import curses
import random

import pickle

import level
import message
import splash
import display
import npc
import hero
import curseconf

import pickle

def game_state_machine(stdscr, state_machine = 0):
    k = 0


    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # do not wait for input when calling getch
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN,  curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_RED)

    curses.curs_set(0)

    msg_queue = display.ActionMessage(stdscr)

    # generate 100 levels
    levels = []
    for i in range(0, 99):
        levels.append(level.Level(stdscr))

    levelindex = 0
    curlevel = levels[levelindex]    
    curlevel.msg_queue = msg_queue
    
    
    myhero    = hero.Hero(curlevel)

    # Initialization
    stdscr.clear()

    drawme = False

    state_transition = True

    # Loop where k is the last character pressed
    while state_machine != 99: 


        # --
        # Regardless of state, on 'q' jump to quite screen 
        # --

        if k == ord('q'):
            splash.draw_exit_screen(stdscr)

            while 1:
                k = stdscr.getch()
                if k == ord('y'):
                    state_machine = 99
                    state_transition = True
                    break
                elif k == ord('n'):
                    state_transition = True
                    break
                elif k == ord('m'):
                    state_machine = 0
                    state_transition = True
                    break

            # If we're exiting, skip reading the next character from
            # the user
            if state_machine == 99 :
                continue

        # --
        # Main title
        # --

        if state_machine == 0:
            splash.draw_main_title(stdscr)

            if k == ord('n'): 
                k = 'XXX'
                stdscr.clear()
                state_machine = 1
                state_transition = True
                continue
            elif k == ord('l'):
                fp = open(curseconf.SAVE_FILE, 'r')
                (myhero, curlevel, levels) = pickle.load(fp)
                fp.close()

                curlevel.msg_queue = msg_queue
                state_machine = 2
                continue

        # --
        # Introduction splash screen 
        # --

        if state_machine == 1:    

            if k == ord(' '): 
                state_machine = 2
                state_transition = True
                stdscr.clear()
                continue
            else:    
                if state_transition :
                    splash.draw_intro_sequence(stdscr)

        # --
        # Main game engine 
        # --

        # Give the queue that manages messages to the screen some cycle
        # time
        msg_queue.run()


        if state_machine == 2:    

            if k == ord('s'):  # save the current game
                fp = None

                for alevel in levels:
                    alevel.msg_queue = None

                try:
                    curlevel.msg_queue = None
                    fp = open(curseconf.SAVE_FILE, 'wb')
                    pickle.dump((myhero, curlevel, levels), fp)
                    fp.close()

                    msg_queue.add("Game saved", 2)
                except Exception as e:
                    msg_queue.add("Save file failed ", 2)
                
                curlevel.msg_queue = msg_queue
                    

            if not drawme:
                drawme = curlevel
                drawme.draw_level   (stdscr)
            elif state_transition:    
                drawme.draw_level   (stdscr)

            if levelindex > 0:
                curlevel.draw_entrance(stdscr, myhero)

            curlevel.draw_exit    (stdscr, myhero)
            curlevel.draw_monsters(stdscr, myhero)

            # Move and draw hero
            myhero.clear(stdscr)
            myhero.move(k)
            myhero.display(stdscr)
            myhero.display_hud(stdscr)

            # combat loop!
            for monster in curlevel.monsters:
                if monster.can_attack(myhero):
                    if monster.attack(myhero):
                        monster.clear(stdscr)
                        monster.display_killed()
                        curlevel.monsters.remove(monster)

            # make sure only check that hero descends/ascends after combat            
            if myhero.y == curlevel.exity and myhero.x == curlevel.exitx:
                levelindex += 1
                curlevel = levels[levelindex]
                curlevel.msg_queue = msg_queue
                myhero.curlevel = curlevel
                myhero.reset_start()
                drawme = False
                continue

            if levelindex and myhero.y == curlevel.starty and myhero.x == curlevel.startx:
                levelindex -= 1
                curlevel = levels[levelindex]
                curlevel.msg_queue = msg_queue
                myhero.curlevel = curlevel
                myhero.reset_exit()
                drawme = False
                continue

            # Print status HUD
            display.dungeon_hud_compact(stdscr, levelindex)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        # End of while loop, on each state machine transition we
        # "continue" to the top so if we've reached here, reset
        # transition flag
        state_transition = False


def main():

    state_machine = 0
    
    args = getopt.getopt(sys.argv[1:],"","state_machine=")
    for arg, val in args[0]:
        if arg == '--state_machine':
            state_machine = int(val)

    curses.wrapper(game_state_machine, state_machine)

if __name__ == "__main__":
    main()
