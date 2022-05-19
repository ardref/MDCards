from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.logger import Logger, LOG_LEVELS

from os.path import exists

import csv
import random
import shutil


Logger.setLevel(LOG_LEVELS["debug"])

Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')

# TODO: Fill values in .kv 'card'

# CSV file. Default (reset) is preceded by a '.'
CSV_FILE = 'chaos.csv'


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class EventCard(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__()
        self._popup = None

    # def show_load_list(self):
    #     content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup)
    #     self._popup = Popup(title="Load a file list", content=content, size_hint=(1, 1))
    #     # self.ids.header.text = 'TEST'
    #     self._popup.open()

    def load_list(self, path, filename):
        pass

    # def dismiss_popup(self):
    #     self._popup.dismiss()

    def selected(self, filename):
        self.ids.header.text = filename[0]


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
