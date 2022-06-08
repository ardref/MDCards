from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger, LOG_LEVELS
from deck import deck

import os.path

Logger.setLevel(LOG_LEVELS["debug"])
Logger.info('ChaosApp: This is a info message.')
Logger.debug('ChaosApp: This is a debug message.')


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
        pathname = os.path.join(directory, filename[0])
        if len(pathname) > 0:
            deck.load(pathname)

        self.dismiss_popup()

        # Display deck's cover card.
        self.show_card(0)

    def show_card(self, index=None):

        card = deck.get_card(index)

        self.toolbar.title = card.Toolbar
        self.title.text = card.Title
        self.body.text = card.Body
        self.extra.text = card.Extra


class ChaosApp(MDApp):
    """ Kivy app to manage 'Event Cards' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'CHAnce Organising System'

        deck.build_deck()

        return


Factory.register('EventCard', cls=EventCardLayout)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    ChaosApp().run()
