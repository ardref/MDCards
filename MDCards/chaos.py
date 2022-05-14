from kivymd.app import MDApp
from os.path import exists

import csv
import random
import shutil

# CSV file. Default (reset) is preceded by a '.'
CSV_FILE = 'chaos.csv'


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        """ CSV file is created if it does not yet exist """
        super().__init__(**kwargs)

        if not exists(CSV_FILE):
            shutil.copyfile('.' + CSV_FILE, CSV_FILE)

        self.deck = list()

    def read_csv(self):
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

        self.read_csv()

        return


ChaosApp().run()
