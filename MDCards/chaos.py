from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

import csv
import random
import os

CSV_FILE = 'chaos.csv'

class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deck = list()
        self.readcsv()

    def readcsv(self):
        """ Populate Event deck from CSV file """

        self.deck.clear()
        with open(CSV_FILE, newline='') as csvfile:

            # Ignore first row - Header.
            rows = list(csv.reader(csvfile))[1:]

            for row in rows:
                self.deck.append(row)

    def shuffle(self):
        # N.B.: This method changes the original list, it does not return a new list.
        random.shuffle(self.deck)

    def build(self):
        self.title = 'CHAnce Organising System'

        config = self.config
        
        return

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        # Snackbar(text=text_item).open()


ChaosApp().run()
