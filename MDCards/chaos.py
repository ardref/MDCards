from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger, LOG_LEVELS
from collections import namedtuple
from os.path import exists

import os
import csv
import random
import shutil


Logger.setLevel(LOG_LEVELS["debug"])

Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')

# TODO: Fill values in .kv 'card'

# CSV file. Default (reset) is preceded by a '.'
CSV_FILE = '.chaos.csv'
CSV_INIT = """1, CHAOS, Event Deck, Choose CSV File to Build Deck, Use 'Nav Bar' below: Back, Forward
"""

Fields = namedtuple('CSV_Header', 'Weight, Header, Title, Body, Extra')


class LoadDialog(FloatLayout):
    """ <LoadDialog> Class Rule in KV file """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class EventCard(FloatLayout):
    """ EventCard Root Rule in KV file """
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__()
        self._popup = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.6))
        self._popup.open()

    def load(self, path, filename):
        # TODO: Update hidden file.
        """ Validate CSV file, then save data to hidden file """
        if len(filename) > 0:
            with open(os.path.join(path, filename[0])) as stream:
                rows = stream.read()
                if not csv.Sniffer().has_header(rows):
                    raise Exception("Header row not found in CSV file.")
        self.dismiss_popup()

    def selected(self, filename):
        self.ids.header.text = filename[0]


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # CSV file is created if it does not yet exist.
        if not exists(CSV_FILE):
            with open(CSV_FILE, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(CSV_INIT)

        self.deck = list()

    def read_csv(self):
        """ Populate Event deck from hidden CSV file """

        self.deck.clear()

        with open(CSV_FILE) as csvfile:
            # Ignore first row - Header.
            reader = csv.DictReader(csvfile)

            for row in reader:
                weight = int(row['Weight'])

    def shuffle(self):
        # N.B.: This method changes the original list, it does not return a new list.
        random.shuffle(self.deck)

    def build(self):
        self.title = 'CHAnce Organising System'

        self.read_csv()

        return


Factory.register('EventCard', cls=EventCard)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ChaosApp().run()
