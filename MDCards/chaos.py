from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger, LOG_LEVELS

from deck import deck
from common import Card

import os.path

Logger.setLevel(LOG_LEVELS["debug"])
Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')


class LoadDialog(FloatLayout):
    """ <LoadDialog> Class Rule in KV file """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class CardScreen(Screen):
    """ Common Screen for all cards """

    toolbar = ObjectProperty(None)
    title = ObjectProperty(None)
    body = ObjectProperty(None)
    extra = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fill(self, card):

        self.toolbar.title = card.Toolbar
        self.title.text = card.Title
        self.body.text = card.Body
        self.extra.text = card.Extra


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.card_count = deck.build_deck()
        self.sm = ScreenManager(transition=CardTransition())
        self.top_card = Card(Weight=1, Toolbar='TEST', Title='Title', Body='Body', Extra=f'Total: {self.card_count}')

        self._popup = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def load_dialog(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.6))
        self._popup.open()

    def load(self, directory, filename):
        pathname = os.path.join(directory, filename[0])
        if len(pathname) > 0:
            deck.load(pathname)
            self.sm.current = 'Card 0'

        self.cancel()

    def cancel(self):
        self.dismiss_popup()

    def make_screen(self, index, card):
        screen = CardScreen(name=f'Card {index}')
        screen.fill(card)
        self.sm.add_widget(screen)  # 'screen' inserted at head of self.sm.screens list.

    def build(self):
        self.title = 'CHAnce Organising System'

        self.reset()

        # 'root' reference in .kv file.
        return self.sm

    def reset(self):
        self.sm.clear_widgets()

        deck.shuffle()

        for index, card in enumerate(deck):
            self.make_screen(index, card)

        # LIFO - puts card at head of 'screens' list.
        self.make_screen(0, self.top_card)

        self.sm.current = 'Card 0'

    def forward(self):
        self.sm.current = self.sm.next()

    def backward(self):
        self.sm.current = self.sm.previous()


# Factory.register('EventCard', cls=EventCard)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ChaosApp().run()
