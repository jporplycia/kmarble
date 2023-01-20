# File name: marble_kivy.app
#:kivy 2.1.0
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ObrazovkaHry(PageLayout):
    def switch_to(self, page):
        self.page = page

class Pozadi(BoxLayout):
    pass

class MojeTlacitko(Button):
    pass

class MarbleApp(App):
    def build(self):
        return ObrazovkaHry()
    


if __name__ == '__main__':
    MarbleApp().run()
