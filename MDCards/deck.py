from collections import namedtuple

import csv
import random
import os

CSV_FILE = ".chaos.csv"
CSV_HDR = namedtuple('Header', ('Weight', 'Toolbar', 'Title', 'Body', 'Extra'))
CSV_INIT = [['1', 'CHAOS', 'Event Deck', 'Choose CSV File to Build Deck', 'Nav Bar: Back, Shuffle, Forward']]


# Card deck.
class Deck(list):

    def __init__(self):
        super().__init__()
        self.index = -1

        # CSV file is created if it does not yet exist.
        if not os.path.exists(CSV_FILE):
            self.csv_write(CSV_HDR._fields, CSV_INIT, CSV_FILE)

    def forward(self):
        self.index += 1
        return self[self.index]

    def backward(self):
        if self.index > 0:
            self.index -= 1
        return self[self.index]

    def shuffle(self):
        random.shuffle(self)

    def build_deck(self):
        """ Populate Event deck from hidden CSV file """

        self.clear()

        header, data = self.csv_read(CSV_FILE)

        for row in data:
            weight = int(row[0])

            # Add number of duplicate cards, according to 'Weight'.
            for n in range(weight):
                self.append(row)

    def get_card(self, index=None):

        index = self.index if not index else index

        return CSV_HDR(*self[index])

    @staticmethod
    def csv_write(header, data, pathname):
        """ Write header and data rows as CSV file """

        with open(pathname, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)

    @staticmethod
    def csv_read(pathname):
        """ Read/Validate CSV file - then return header, data rows """

        csv.register_dialect('reader', skipinitialspace=True)

        with open(pathname) as f:
            header, *data = csv.reader(f, dialect="reader")
            if tuple(header) != CSV_HDR._fields:
                raise ValueError("Invalid CSV file (Header)")

        return header, data

    def load(self, pathname):
        """ Validate CSV file, then save data to hidden file """
        header, data = self.csv_read(pathname)
        self.csv_write(header, data, CSV_FILE)


deck = Deck()
