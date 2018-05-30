import random
from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder


GRID_SIZE = 2


def build_options(total_options, duplicates=2):
    options = [i for i in range(total_options // duplicates) for _ in range(duplicates)]
    random.shuffle(options)
    return options


def show_winner(board):
    popup = ModalView(size_hint=(0.75, 0.5))
    victory_label = Label(text="You won!", font_size=50)
    popup.add_widget(victory_label)
    popup.bind(on_dismiss=board.on_win)
    popup.open()


Builder.load_string('''
<GameGrid>:
    cols: %s  # Number of columns

<SpellIcon>:
    font_size: self.height // 3
    label: str(self.label)

<Interface>:
    orientation: 'vertical'
    AnchorLayout:
        GameGrid:
            id: board
            size: min(self.parent.size), min(self.parent.size)
            size_hint: None, None
            padding: sp(20)
    Label:
        size_hint_y: None
        height: sp(40)
        text: 
            'Matches left: {}'.format(board.left)
    Button:
        size_hint_y: None
        height: sp(40)
        text: 'New Game / Restart'
        on_press: board.reset()
''' % (GRID_SIZE,))


class SpellIcon(Button):
    coords = ListProperty([0, 0])
    label = NumericProperty(-1)

class GameGrid(GridLayout):
    board = ObjectProperty([[None for __ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
    left = NumericProperty(-1)
    selection = [-1, -1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        options = build_options(GRID_SIZE * GRID_SIZE, 2)
        self.left = len(options) // 2

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                label = options.pop()
                grid_entry = SpellIcon(coords=(x, y), label=label)
                grid_entry.text = str(label)
                grid_entry.background_color = (1, 1, 1, 1)
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)
                self.board[x][y] = grid_entry
                    

    def button_pressed(self, new_button):
        _x, _y = self.selection
        x, y = new_button.coords
        self.selection = [x, y]

        new_button.background_color = (0,1,0,1)

        if _x == -1 or _y == -1:
            return

        old_button = self.board[_x][_y]
        old_button.background_color = (0,1,0,1)
        
        if new_button.label == old_button.label:
            old_button.opacity = 0
            new_button.opacity = 0
            self.left -= 1
        else:
            old_button.background_color = (1,1,1,1)
            new_button.background_color = (1,1,1,1)
        
        self.selection = [-1, -1]

        if self.left == 0:
            show_winner(self)

    def on_win(self, *args):
        # GRID_SIZE += 2
        self.reset(*args)

    def reset(self, *args):
        options = build_options(GRID_SIZE * GRID_SIZE, 2)

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                button = self.board[x][y]
                button.label = options.pop()

        self.left = (GRID_SIZE * GRID_SIZE) // 2
        self.selection = [0, 0]

        for child in self.children:
            child.opacity = 1
            child.background_color = (1,1,1,1)


class Interface(BoxLayout):
    pass


class Application(App):
    
    def build(self):
        self.title = 'LOL Connect'
        return Interface()

if __name__ == "__main__":
    Application().run()

