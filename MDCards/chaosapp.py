from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

import csv
import random

CSV_FILE = 'events.csv'

class ChaosApp(MDApp):
    """ Kivy app to manage Event Card Deck """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deck = list()
        self.readcsv()

    def readcsv(self):
        """ Populate Event deck from CSV file """

        self.deck.clear()
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.deck.append(row)

    def shuffle(self):
        # N.B.: This method changes the original list, it does not return a new list.
        random.shuffle(self.deck)

    def build(self):
        self.title = 'CHAnce Organising System'

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{item}",
                "height": dp(56),
                "on_release": lambda x=f"{item}": self.menu_callback(x),
             } for item in ('Load CSV', 'Shuffle', 'About')
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return Builder.load_file('chaosui.kv')

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        # Snackbar(text=text_item).open()


ChaosApp().run()
