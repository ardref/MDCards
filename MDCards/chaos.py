from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger, LOG_LEVELS
from collections import namedtuple

import csv
import random
import os.path

Logger.setLevel(LOG_LEVELS["debug"])

Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')

# TODO: Fill values in .kv 'card'

# CSV file. Default (reset) is preceded by a '.'
CSV_FILE = '.chaos.csv'
CSV_HDR = ['Weight', 'Header', 'Title', 'Body', 'Extra']
CSV_INIT = ['1', 'CHAOS', 'Event Deck', 'Choose CSV File to Build Deck', 'Nav Bar: Back, Shuffle, Forward']

CSVFile = namedtuple('CSV_File', ['header', 'data'])
Fields = namedtuple('CSV_Header', CSV_HDR)


def csv_read(pathname):
    """ Read/Validate CSV file - then return header, data rows """

    csv.register_dialect('reader', skipinitialspace=True)

    with open(pathname) as f:
        header, *data = csv.reader(f, dialect="reader")
        if header != CSV_HDR:
            raise ValueError("Invalid CSV file (Header)")

    return header, data


def csv_write(header, data, pathname):
    """ Write header and data rows as CSV file """

    with open(pathname, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)


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

    def load(self, directory, filename):
        """ Validate CSV file, then save data to hidden file """

        pathname = os.path.join(directory, filename[0])
        if len(pathname) > 0:
            header, data = csv_read(pathname)
            csv_write(header, data, CSV_FILE)

        self.dismiss_popup()

    def selected(self, filename):
        self.ids.header.text = filename[0]


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # CSV file is created if it does not yet exist.
        if not os.path.exists(CSV_FILE):
            csv_write(CSV_HDR, CSV_INIT, CSV_FILE)

        self.deck = list()

    def build_deck(self):
        """ Populate Event deck from hidden CSV file """

        self.deck.clear()

        header, data = csv_read(CSV_FILE)

        for row in data:
            weight = int(row[0])

            # Add number of duplicate cards, according to 'Weight'.
            for n in range(weight):
                self.deck.append(row[1:])

    def shuffle(self):
        # N.B.: This method changes the original list, it does not return a new list.
        random.shuffle(self.deck)

    def build(self):
        self.title = 'CHAnce Organising System'

        self.build_deck()

        return


Factory.register('EventCard', cls=EventCard)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ChaosApp().run()
