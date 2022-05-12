from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


class ChaosApp(MDApp):
    def build(self):
        self.title = 'CHAnce Organising System'

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{item}",
                "height": dp(56),
                "on_release": lambda x=f"{item}": self.menu_callback(x),
             } for item in ('Import', 'Shuffle', 'Reset', 'About')
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return Builder.load_file('chaosui.kv')

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        # Snackbar(text=text_item).open()


ChaosApp().run()
