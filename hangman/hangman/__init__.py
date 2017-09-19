import os
from hangman import main

if __name__ == '__main__':
    os.environ["TERM"] = "xterm"  # need this to show RGB colors
    main.main()
