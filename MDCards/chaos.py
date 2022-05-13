from kivymd.app import MDApp
import configparser

import csv
import random

# N.B.: Kivy's own Config parser may be required in deployment, instead of the local .ini file.
INI_FILE = 'chaos.ini'

class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config = configparser.ConfigParser()
        config.read(INI_FILE)
        self.csv_file = config.get('User', 'CSV_FILE')

        self.deck = list()

    def read_csv(self):
        """ Populate Event deck from CSV file """

        self.deck.clear()

        with open(self.csv_file, newline='') as csvfile:
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
