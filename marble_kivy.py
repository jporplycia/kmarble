# File name: marble_kivy.app
#:kivy 2.1.0
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class ObrazovkaHry(Screen):
    pass

class ObrazovkaNastaveni(Screen):
    pass
        
class Pozadi(BoxLayout):
    pass

class MarbleApp(MDApp):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ObrazovkaHry(name='obrazovka_hry'))
        sm.add_widget(ObrazovkaNastaveni(name='obrazovka_nastaveni'))
        return sm

if __name__ == '__main__':
    LabelBase.register(name='Roboto', fn_regular='Roboto-Medium.ttf')
    MarbleApp().run()
