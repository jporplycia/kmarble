#!/usr/bin/python3
#############################
# Modul: marble_kivy.py
# Autor: Jaroslav Porplycia
# Datum: 2023/01/26
# Verze: 0.01
'''
Hra na čtvercové desce o několika polích
V každém kole přibude několik kuliček několika barev
Hráč vybere kuličku a posune ji na jiné místo
Pokud kuličky vytvoří řadu vodorovnou, svislou nebo šikmou, o předem daném počtu kuliček nebo větším, tak kuličky zmizí a hráči se připíšou body
Hra končí v okamžiku, kdy je celé hrací pole obsazené
'''
###############################
# Log:
# # 2023/01/26 JP - začátek migrace hotové hry v PYQT6 na kivy, do této doby probíhalo jen seznamování s kivy
# # 2023/01/26 JP - načtení proměnných
# # 2023/02/09 JP - postupné seznamování s kivy a přebudování původního kódu do nové aplikace
################################
# File name: marble_kivy.app
#:kivy 2.1.0

import marble_funkce, marble_lang
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class MarbleApp(App):
    # načtení proměnných
    Config.read('config.ini')
    sirka_matice = int(Config.get('settings', 'sirka_matice'))
    pocet_barev = int(Config.get('settings', 'pocet_barev'))
    prirustek = int(Config.get('settings', 'prirustek'))
    min_rada = int(Config.get('settings', 'min_rada'))
    zisk = Config.get('settings', 'zisk')
    jazyk = Config.get('settings', 'jazyk')
    texty = marble_lang.nacti_text(jazyk)
    # nastavení dalších proměnných
    grid_size, zmenseni = 0, 8
    offset = (0, 0)
    circles = {}
    vyber, cil = 0, 0
    animace = 0
    cas_posunu, cas_pauzy, cas_zmizeni = 0.05, 0.5, 0.05
    body, krok = 0, 0
    pole, barva, kulicky, pozice_vybrane_kulicky, cil_pozice, cesta, smazat_mista = [], [], [], [], [], [], []
    hra_bezi, hrac_je_na_tahu, vybrana_kulicka, byla_hra = False, False, False, False
    
    def build(self):
        Window.bind(size=self.vykresli_herni_pole)
        self.root.ids.obrazovka_hry.ids.herni_pole.bind(on_touch_down=self.vyber_kulicky_stisk)
    
    # def on_size(self, instance, value):
        # self.vykresli_herni_pole()
    
    def nacti_obrazky(self):
        # načtení obrázků kuliček
        self.barva = []
        for i in range(self.pocet_barev+1):
            self.barva.append(Image(source='images/b' + str(i).zfill(2) + '.png'))
    
    def vykresli_herni_pole(self, *args):
        # POZOR - nereaguje na situaci maximalizace okna a zpět ve windows
        if self.hra_bezi:
            herni_pole = self.root.ids.obrazovka_hry.ids.herni_pole
            # vypočte pozice a rozestupy
            width, height = herni_pole.width, herni_pole.height
            self.grid_size = int(min(width, height)) // self.sirka_matice
            size = self.grid_size * self.sirka_matice
            x, y = herni_pole.x + (width - size) // 2, herni_pole.y + (height - size) // 2
            self.offset = (x, y)
            # vymaže plátno a seznam čar
            herni_pole.canvas.clear()
            # nakreslí mřížku a kuličky
            with herni_pole.canvas:
                Color(1, 1, 1, 0.5)
                for offset in range(0, size + self.grid_size, self.grid_size):
                    Line(points=(x, y + offset, x + size, y + offset))
                    Line(points=(x + offset, y, x + offset, y + size))
                Color(1, 1, 1, 1)
                if self.vyber != 0:
                    self.vyber = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + self.grid_size * self.pozice_vybrane_kulicky[0], self.offset[1] + self.grid_size * self.pozice_vybrane_kulicky[1]), size=(self.grid_size, self.grid_size))
                for x, y in self.circles.keys():
                    self.add_ball(x, y)
                if self.cil != 0:
                    self.cil = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + self.grid_size * self.cil_pozice[0], self.offset[1] + self.grid_size * self.cil_pozice[1]), size=(self.grid_size, self.grid_size))
        elif self.byla_hra:
            self.oznam_konec()
    
    def start_hry(self): # akce při stisku tlačítka start hry
        if self.hra_bezi: # hra probíhá, dojde k jejímu předčasnému ukončení
            self.root.ids.obrazovka_hry.ids.btn_start.text = 'Začni hru'
            self.root.ids.obrazovka_hry.ids.herni_pole.canvas.clear()
            self.circles = {}
            self.root.ids.obrazovka_hry.ids.btn_nastaveni.disabled = False
            self.hra_bezi = False
            self.byla_hra = True
            self.vyber, self.cil = 0, 0
            self.oznam_konec()
        else:   # hra začíná
            self.body = 0
            self.root.ids.obrazovka_hry.ids.btn_vysledky.text = str(self.body)
            self.root.ids.obrazovka_hry.ids.btn_start.text = 'Ukonči hru'
            self.root.ids.obrazovka_hry.ids.btn_nastaveni.disabled = True
            self.pole = marble_funkce.vytvor_pole(self.sirka_matice) # vytvoření herního pole
            self.nacti_obrazky()
            self.hra_bezi = True
            self.vykresli_herni_pole() # smaže herní pole a nakreslí čáry
            self.herni_kolo()
    
    def animuj_zmizeni(self, dt):
        # animace smazání řady
        if self.krok < len(self.smazat_mista):
            self.remove_ball(self.smazat_mista[self.krok][0],self.smazat_mista[self.krok][1])
            self.krok += 1
        else:
            self.animace.cancel()     
            self.hrac_je_na_tahu = True
    
    def stisk_nastaveni(self):
        self.root.ids.obrazovka_nastaveni.ids.sld_sirka_matice.value = self.sirka_matice
        self.root.ids.obrazovka_nastaveni.ids.sld_pocet_barev.value = self.pocet_barev
        self.root.ids.obrazovka_nastaveni.ids.sld_prirustek.value = self.prirustek
        self.root.ids.obrazovka_nastaveni.ids.sld_min_rada.value = self.min_rada
        self.root.ids.obrazovka_nastaveni.ids.ti_zisk.text = self.zisk
        self.root.ids.obrazovka_nastaveni.ids.lb_jazyk.text = self.jazyk
        self.root.current = 'ObrazovkaNastaveni'
    
    def stisk_zpet(self):
        self.root.current = 'ObrazovkaHry'
        
    def stisk_uloz(self):
        self.sirka_matice = self.root.ids.obrazovka_nastaveni.ids.sld_sirka_matice.value
        self.pocet_barev = self.root.ids.obrazovka_nastaveni.ids.sld_pocet_barev.value
        self.prirustek = self.root.ids.obrazovka_nastaveni.ids.sld_prirustek.value
        self.min_rada = self.root.ids.obrazovka_nastaveni.ids.sld_min_rada.value
        self.zisk = self.root.ids.obrazovka_nastaveni.ids.ti_zisk.text
        self.jazyk = self.root.ids.obrazovka_nastaveni.ids.lb_jazyk.text
        self.root.current = 'ObrazovkaHry'
        Config.set('settings', 'sirka_matice', self.sirka_matice)
        Config.set('settings', 'pocet_barev', self.pocet_barev)
        Config.set('settings', 'prirustek', self.prirustek)
        Config.set('settings', 'min_rada', self.min_rada)
        Config.set('settings', 'zisk', self.zisk)
        Config.set('settings', 'jazyk', self.jazyk)
        Config.write()
    
    def remove_ball(self, x, y):
        circle = self.circles.pop((x, y))
        self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(circle)
    
    def add_ball(self, x, y, pozadi = False):
        grid = self.grid_size
        with self.root.ids.obrazovka_hry.ids.herni_pole.canvas:
            Color(1,1,1,1)
            if pozadi:
                self.vyber = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + grid * x, self.offset[1] + grid * y), size=(grid, grid))
            self.circles[(x, y)] = Ellipse(texture=self.barva[self.pole[x][y]].texture, pos=(self.offset[0] + grid * x + self.zmenseni // 2, self.offset[1] + grid * y + self.zmenseni // 2), size=(grid - self.zmenseni, grid - self.zmenseni))
    
    def oznam_konec(self):
        # Oznámení konce hry a dosaženého počtu bodů
        herni_pole = self.root.ids.obrazovka_hry.ids.herni_pole
        herni_pole.canvas.clear()
        with herni_pole.canvas:
            Label(text='Konec hry.\nDosažený počet bodů: ' + str(self.body), font_size='24sp', halign='center', center=herni_pole.center)
    
    def smaz_vybery(self, dt):
        vyber, cil = 0, 0
        self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(self.vyber)
        self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(self.cil)
        self.hrac_je_na_tahu = True
    
    def animuj(self, dt):
        # přesun kuličky do cíle
        self.remove_ball(self.cesta[self.krok][0],self.cesta[self.krok][1])
        self.add_ball(self.cesta[self.krok+1][0],self.cesta[self.krok+1][1])
        self.krok += 1
        if self.krok > len(self.cesta)-2:
            self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(self.cil)
            self.animace.cancel()
            self.herni_kolo()
    
    def herni_kolo(self):
        zisk = [int(n) for n in self.zisk.split(',')]
        self.smazat_mista, pocet_bodu = marble_funkce.zkontroluj_rady(self.pole, self.min_rada, zisk)
        if pocet_bodu == 0:
            self.pole, nove_kulicky = marble_funkce.nove_kulicky(self.pole, self.prirustek, self.pocet_barev)
            for kulicka in nove_kulicky:
                self.add_ball(kulicka[0],kulicka[1])
            self.smazat_mista, pocet_bodu = marble_funkce.zkontroluj_rady(self.pole, self.min_rada, zisk)
        self.body += pocet_bodu
        self.root.ids.obrazovka_hry.ids.btn_vysledky.text = str(self.body)
        if len(self.smazat_mista) > 0:
            # smazání řady
            for misto in self.smazat_mista:
                self.pole[misto[0]][misto[1]] = 0
            self.krok = 0
            self.animace = Clock.schedule_interval(self.animuj_zmizeni, self.cas_zmizeni)
        else:
            # pokud se pole zaplnilo, ukonči hru
            if marble_funkce.je_pole_plne(self.pole):
                self.hra_bezi = False
                self.root.ids.obrazovka_hry.ids.btn_start.text = 'Začni hru'
                self.root.ids.obrazovka_hry.ids.herni_pole.canvas.clear()
                self.circles = {}
                self.root.ids.obrazovka_hry.ids.btn_nastaveni.disabled = False
                self.byla_hra = True
                self.oznam_konec()
            else:
                self.hrac_je_na_tahu = True
    
    def vyber_kulicky_stisk(self, instance, touch, *args):
        # akce při výběru kuličky nebo prázdného pole
        if self.hra_bezi and self.hrac_je_na_tahu: # pokud probíhá hra a hráč je na tahu tak pokračuj, jinak nic
            # výpočet hranic herní mřížky
            x, y = touch.pos
            x_min, y_min = self.offset
            x_max = x_min + self.grid_size * self.sirka_matice
            y_max = y_min + self.grid_size * self.sirka_matice
            if x >= x_min and y >= y_min and x < x_max and y < y_max: # pokud je kliknuto do mřížky, zjisti pozici kliknutí, jinak skonči
                # výpočet kam se kliklo
                i, j = int((x - self.offset[0])/self.grid_size), int((y - self.offset[1])/self.grid_size)
                self.hrac_je_na_tahu = False
                if self.vybrana_kulicka: # je vybraná kulička, kterou chceme přesunout, nyní vybíráme kam
                    if self.pole[i][j] > 0:
                        # změna výběru kuličky, původní dej zpět, označ novou
                        self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(self.vyber)
                        self.pozice_vybrane_kulicky = [i, j]
                        self.vybrana_kulicka = True
                        self.add_ball(i, j, True)
                        self.hrac_je_na_tahu = True
                    else:
                        # označ cíl a zavolej animaci
                        self.cil_pozice = [i, j]
                        with self.root.ids.obrazovka_hry.ids.herni_pole.canvas:
                            Color(1,1,1,1)
                            self.cil = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + self.grid_size * i, self.offset[1] + self.grid_size * j), size=(self.grid_size, self.grid_size))
                        je_cesta, self.cesta = marble_funkce.najdi_cestu(self.pole, self.pozice_vybrane_kulicky, self.cil_pozice)
                        self.vybrana_kulicka = False
                        if je_cesta:
                            self.pole[self.cesta[-1][0]][self.cesta[-1][1]] = self.pole[self.cesta[0][0]][self.cesta[0][1]]
                            self.pole[self.cesta[0][0]][self.cesta[0][1]] = 0
                            self.krok = 0
                            self.root.ids.obrazovka_hry.ids.herni_pole.canvas.remove(self.vyber)
                            self.animace = Clock.schedule_interval(self.animuj, self.cas_posunu)
                        else:
                            Clock.schedule_once(self.smaz_vybery, self.cas_pauzy)
                else: # vybíráme kuličku, kterou chceme přesunout
                    if self.pole[i][j] > 0: # klikli jsme na kuličku?
                        self.pozice_vybrane_kulicky = [i, j]
                        self.vybrana_kulicka = True
                        self.remove_ball(i, j)
                        self.add_ball(i, j, True)
                    self.hrac_je_na_tahu = True

if __name__ == '__main__':
    LabelBase.register(name='Roboto', fn_regular='Roboto-Medium.ttf')
    MarbleApp().run()