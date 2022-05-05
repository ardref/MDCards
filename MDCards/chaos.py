from kivy.lang import Builder
from kivymd.app import MDApp


class Chaos(MDApp):
    def build(self):
        return Builder.load_file('chaos.kv')


Chaos().run()
