from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
BoxLayout:
    orientation: "vertical"

    MDToolbar:
        title: "MDToolbar"

    MDLabel:
        text: "Content"
        halign: "center"
'''


class Chaos(MDApp):
    def build(self):
#       return Builder.load_string(KV)
        return Builder.load_file('chaos.kv')


Chaos().run()
