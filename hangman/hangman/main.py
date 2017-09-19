import os
import hangman.tui
from colorama import init as color_init
color_init()



def main():
    tui = hangman.tui.Tui()
    os.environ["TERM"] = "xterm"
    tui.fsm.init()
    tui.start_game()
    exit(0)
