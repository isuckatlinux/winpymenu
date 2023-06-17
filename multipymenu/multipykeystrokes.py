""" File that contains functions to detect key strokes in linux
"""
import curses

class MultiPyKeyStrokes:
     
    stdscr:any
    def init(self):
        """Initializes the library and configures settings in the terminal to make it usable in the way we want it
        """
        self.stdscr = curses.initscr() # Initialize curses
        curses.noecho() # Deactivates automatic echoing of keys to the screen
        curses.cbreak() # React to keys instantly without requiring the Enter key to be pressed
        self.stdscr.keypad(True) # Activate key dictionary managed by curses

    def deinit(self):
        """Returns terminal to default settings and de-initialize the library
        """
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def handleStroke(self):

        key = self.stdscr.getkey()
        return key

kshandler = MultiPyKeyStrokes()
kshandler.init()

while True:
    print(kshandler.handleStroke())
        
