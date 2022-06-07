from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger, LOG_LEVELS
from dataclasses import dataclass

import csv
import random
import os.path

Logger.setLevel(LOG_LEVELS["debug"])

Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')

# TODO: Fill values in .kv 'card'

CSV_FILE = ".chaos.csv"
CSV_HDR = ('Weight', 'Toolbar', 'Title', 'Body', 'Extra')
CSV_INIT = [['1', 'CHAOS', 'Event Deck', 'Choose CSV File to Build Deck', 'Nav Bar: Back, Shuffle, Forward']]

@dataclass
class Card:
    weight: int
    toolbar: str
    title: str
    body: str
    extra: str


# Card deck.
class Deck(list):

    def __init__(self):
        super().__init__()
        self.index = -1

    def forward(self):
        self.index += 1
        yield self[self.index]

    def backward(self):
        if self.index > 0:
            self.index -= 1
        yield self[self.index]

    def shuffle(self):
        random.shuffle(self)

    def build_deck(self):
        """ Populate Event deck from hidden CSV file """

        self.clear()

        header, data = csv_read(CSV_FILE)

        for row in data:
            weight = int(row[0])

            # Add number of duplicate cards, according to 'Weight'.
            for n in range(weight):
                self.append(row)


deck = Deck()


def csv_read(pathname):
    """ Read/Validate CSV file - then return header, data rows """

    csv.register_dialect('reader', skipinitialspace=True)

    with open(pathname) as f:
        header, *data = csv.reader(f, dialect="reader")
        if tuple(header) != CSV_HDR:
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


class EventCardLayout(FloatLayout):
    """ Root Rule in KV file """

    toolbar = ObjectProperty(None)
    title = ObjectProperty(None)
    body = ObjectProperty(None)
    extra = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__()
        self._popup = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def load_dialog(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.6))
        self._popup.open()

    def load(self, directory, filename):
        """ Validate CSV file, then save data to hidden file """

        pathname = os.path.join(directory, filename[0])
        if len(pathname) > 0:
            header, data = csv_read(pathname)
            csv_write(header, data, CSV_FILE)

        self.show_card()

        self.dismiss_popup()


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # CSV file is created if it does not yet exist.
        if not os.path.exists(CSV_FILE):
            csv_write(CSV_HDR, CSV_INIT, CSV_FILE)

        deck.clear()

    def build(self):
        self.title = 'CHAnce Organising System'

        deck.build_deck()

        return

    def next_card(self):
        deck.forward()
        self.show_card(deck.index)

    def show_card(self, index=0):
        card = deck[index]

        self.root.toolbar.title = card[0]
        self.root.title.text = card[1]
        self.root.body.text = card[2]
        self.root.extra.text = card[3]


Factory.register('EventCard', cls=EventCardLayout)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ChaosApp().run()
