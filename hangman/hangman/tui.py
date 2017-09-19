from hangman.dictionaries import AsciiArt
from xtermcolor import colorize, ColorMap
import urwid
import urwid.widget
from fysom import *
import random

def grab_random_puzzleword(filename="puzzlewords.txt"):
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return random.choice(lines)

class Tui:  # Well, uh, this has pretty much became my main program.
    # Rushed at the end to finish this, didn't have time to organize it very well....

    def __init__(self):
        self.colormap = ColorMap.XTermColorMap()
        self.titlecolors = list()
        # titlecolors list of tuples, (foreground, background)
        self.titlecolors = [
            (self.colormap.convert(0x198844)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0xa36ac7)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0xcc342b)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0x3971ed)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0xfba922)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0x9700c2)[1], self.colormap.convert(0x1d1f21)[1]),
            (self.colormap.convert(0x5a00bf)[1], self.colormap.convert(0x1d1f21)[1])
        ]
        self.title = "HANGMAN"
        self.fancytitle = AsciiArt(self.title, self.titlecolors)
        self.loop = urwid.MainLoop(urwid.Text(""))
        self.gamedata = GameData(puzzleword=grab_random_puzzleword())
        self.game_ascii_art = urwid.Text(self.gamedata.draw_hangman(self.gamedata.guesses))
        self.game_message = urwid.Text(self.gamedata.initial_message)
        self.game_over_message = urwid.Text("")
        self.fsm = Fysom({
            'initial': {'state': 'mainmenu', 'event': 'init', 'defer': True},
            'events': [
                {'name': 'start', 'src': "mainmenu", 'dst': "game"},
                {'name': 'gameover', 'src': "game", 'dst': "mainmenu"},
                {'name': 'gamewin', 'src': "game", 'dst': "mainmenu"},
                {'name': 'pause', 'src': 'game', 'dst': 'pausemenu'},
                {'name': 'resume', 'src': 'pausemenu', 'dst': 'game'},
                {'name': 'quit', 'src:': 'pausemenu', 'dst': 'mainmenu'}
            ],
            'callbacks': {'onchangestate': self.statechange}
        })
        self.urwidViews = {  # maps states to functions that return urwid.Overlay to be used in the main loop
            'none': None,
            'mainmenu': self.MainMenuView(),
            'game': self.gameView(),
            'pausemenu': self.pause_menu_view()
        }
        self.loop = urwid.MainLoop(self.urwidViews[self.fsm.current], palette=[('reversed', 'standout', '')], unhandled_input=self.gameInput)

    def MainMenuView(self) -> urwid.Overlay:
        body = [self.game_over_message]
        startbutton = urwid.Button("Start")
        exitbutton = urwid.Button("Exit")
        urwid.connect_signal(startbutton, 'click', self.fsm.start)
        urwid.connect_signal(exitbutton, 'click', self.exit_game)
        body.append(urwid.AttrMap(startbutton, None, focus_map='reversed'))
        body.append(urwid.AttrMap(exitbutton, None, focus_map='reversed'))
        output = urwid.Overlay(
            urwid.Padding(
                urwid.Frame(
                    urwid.Padding(
                        urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                        left=51, right=51
                    ),
                    header=urwid.Text(str(self.fancytitle))
                ),
                left=1, right=1
            ),
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=142,
            valign='middle', height=15,
            min_width=40, min_height=9
        )
        return output

    def gameInput(self, key: str):
        if len(key) == 1:
            keystr = str(key)  # sometimes urwid sends a tuple for the key (mouse events)
            if self.fsm.current is "game" and keystr.isalpha():
                if keystr in self.gamedata.puzzleword and keystr not in self.gamedata.letters_used:
                    self.gamedata.update_progress(keystr)
                    self.game_message.set_text("""You got lucky this time... \n \n Progress: {}""".format("".join(self.gamedata.progress)))
                    self.gamedata.letters_used += ",{}".format(keystr)
                    self.game_ascii_art.set_text(self.gamedata.draw_hangman(self.gamedata.guesses))
                    if "".join(self.gamedata.progress) == self.gamedata.puzzleword:
                        self.fsm.gamewin()
                elif keystr not in self.gamedata.puzzleword and keystr not in self.gamedata.letters_used:
                    self.gamedata.guesses += 1
                    newtext = "Watch yourself, that was the WRONG letter! That crowd is getting excited!\n\n Progress: {}".format("".join(self.gamedata.progress))
                    self.game_message.set_text(newtext)
                    self.gamedata.letters_used += ",{}".format(keystr)
                    self.game_ascii_art.set_text(self.gamedata.draw_hangman(self.gamedata.guesses))
                    if self.gamedata.guesses == 15:
                        self.fsm.gameover()
                else:
                    """Incorrect guess, but key is a letter"""
                    newtext = "Come on, you already tried that letter. Get on with it! Try again.\n\n Progress: {}".format("".join(self.gamedata.progress))
                    self.game_message.set_text(newtext)
        elif key in ('esc',):
            self.fsm.pause()


    def gameView(self):
        output = urwid.Frame(
            urwid.Columns(
                [
                    ('weight', 2, urwid.LineBox(
                        urwid.Overlay(
                            urwid.ListBox(urwid.SimpleListWalker([self.game_ascii_art])),
                            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            'left',
                            ('relative', 100),
                            'middle',
                            ('relative', 100)
                        )
                    )),
                    urwid.LineBox(
                        urwid.Overlay(
                            urwid.ListBox(urwid.SimpleListWalker([self.game_message])),
                            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            'left',
                            ('relative', 100),
                            'middle',
                            ('relative', 100)
                        )
                    )
                ]
            ),
            header=urwid.LineBox(
                urwid.GridFlow(
                    [
                        urwid.Text("H A N G M A N")
                    ], 15, 0, 0, 'center'
                )
            ),
            footer=urwid.LineBox(
                urwid.GridFlow(
                    [
                        urwid.Button("Pause", on_press=self.fsm.pause)
                    ], 10, 0, 5, 'left'
                )
            )
        )
        self.loop.unhandled_input(self.gameInput)
        return output

    def pause_menu_view(self) -> urwid.Overlay:
        body = [urwid.Text("Paused"), urwid.Divider()]
        yesbutton = urwid.Button("Exit")
        mainmenubutton = urwid.Button("Main Menu")
        nobutton = urwid.Button("Resume")
        urwid.connect_signal(yesbutton, 'click', self.exit_game)
        urwid.connect_signal(mainmenubutton, 'click', self.fsm.quit)
        urwid.connect_signal(nobutton, 'click', self.fsm.resume)
        body.append(urwid.AttrMap(nobutton, None, focus_map='reversed'))
        body.append(urwid.AttrMap(mainmenubutton, None, focus_map='reversed'))
        body.append(urwid.AttrMap(yesbutton, None, focus_map='reversed'))
        output = urwid.Overlay(
            urwid.Padding(
                urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                left=2, right=2
            ),
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 30),
            valign='middle', height=('relative', 30),
            min_width=10, min_height=5
        )
        return output

    def statechange(self, e):
        """add event listener for on state change, and change the main loop's content to match the current state"""
        self.loop.widget = self.urwidViews[e.fsm.current]
        if e.src == "game" and e.dst == "mainmenu" and e.event == "gameover":
            message = "You Lost. The word was {}".format(self.gamedata.puzzleword)
            self.game_over_message.set_text(message)
        if e.src == "game" and e.dst == "mainmenu" and e.event == "gamewin":
            message = "You Win! The word was {}".format(self.gamedata.puzzleword)
            self.game_over_message.set_text(message)
        if e.event == "start":
            self.gamedata = GameData(puzzleword=grab_random_puzzleword())  # clear previous game info
            self.game_ascii_art.set_text(self.gamedata.draw_hangman(self.gamedata.guesses))
            self.game_message.set_text(self.gamedata.initial_message)
            self.game_over_message.set_text("")

    def start_game(self):
        self.loop.run()

    def exit_game(self, button):
        raise urwid.ExitMainLoop


class GameData:

    def __init__(self, puzzleword="wewlad"):
        self.guesses = 0  # Keep track of current guesses
        self.letters_used = ""
        self.puzzleword = puzzleword  # to be randomly selected from a file
        self.progress = ["?" for c in puzzleword]
        self.initial_message = """
*The executioner prepares your noose*
"This is your last chance, VARMINT! Guess the right letters and i'll let you live. BUT, there's a catch, you see..."  
*The noose tightens around your neck*
"Make the wrong guess 15 times, and it's OVER."
"""

    def update_progress(self, guess):
        for idx, c in enumerate(self.puzzleword):
            if guess == self.puzzleword[idx]:
                self.progress[idx] = guess

    def draw_hangman(self, guesses):
        lines = [
            "______",
            "|     |",
            "|     0",
            "|   0   0",
            "|   0   0",
            "|     0",
            "|    /|\\",
            "|   / | \\",
            "|  /  |  \\",
            "|     |",
            "|    / \\",
            "|   /   \\",
            "|  /     \\",
            "|",
            "|"
        ]
        return "\n".join(lines[0:guesses])

class SwitchingPadding(urwid.Padding):
    def padding_values(self, size, focus):
        maxcol = size[0]
        width, ignore = self.original_widget.pack(size, focus=focus)
        if maxcol > width:
            self.align = "left"
        else:
            self.align = "right"
        return urwid.Padding.padding_values(self, size, focus)