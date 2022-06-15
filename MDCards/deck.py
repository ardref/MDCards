import csv
import random
import os

from common import Card


CSV_FILE = ".chaos.csv"
CSV_INIT = [['1', 'CHAOS', 'Event Deck', 'Choose CSV File to Build Deck', 'Nav Bar: Back, Shuffle, Forward']]


# Card deck.
class Deck(list):

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
            _, *data = csv.reader(f, dialect="reader")
            header = tuple(_)
            fieldnames = Card().fieldnames()

            if header != fieldnames:
                raise ValueError("Invalid CSV file (Header)")

        return fieldnames, data

    def __init__(self):
        super().__init__()
        self.index = 0

        # Hidden CSV file is created if it does not yet exist.
        if not os.path.exists(CSV_FILE):
            self.csv_write(Card().fieldnames(), CSV_INIT, CSV_FILE)

    def build_deck(self):
        """ Populate card deck from hidden CSV file """

        self.clear()

        header, data = self.csv_read(CSV_FILE)

        for row in data:
            card = Card(*row)
            weight = int(card.Weight)

            # Add number of duplicate cards, according to 'Weight'.
            for n in range(weight):
                card.Weight = weight
                self.append(card)

    def load(self, pathname):
        """ Load data from CSV file """

        header, data = self.csv_read(pathname)
        self.csv_write(header, data, CSV_FILE)

        self.build_deck()

        return

    def forward(self):
        # ToDo: handle IndexError
        return self.get_card(self.index+1)

    def backward(self):
        # ToDo: handle IndexError
        return self.get_card(self.index-1)

    def shuffle(self):
        """ Random shuffle of cards, excluding top card """
        random.shuffle(self[1:])

    def get_card(self, index):

        try:
            card = self[index]
        except IndexError:
            raise
        else:
            self.index = index

        return card


deck = Deck()
