#!/usr/bin/python3
#############################
# Modul: marble_kivy.py
# Autor: Jaroslav Porplycia
# Datum: 2023/01/26
# Verze: 0.02
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
# # 2023/02/14 JP - zprovoznění hry, zvuky, jazykové mutace
# # 2023/02/21 JP - ošetření neexistence souboru config.ini
# # 2023/02/22 JP - změna ukládání dat, nyní se ukládají do souboru data.json - vše funkční, aplikace na androidu jede
# # 2023/02/27 JP - začátek práce na verzi 0.02 - Požadavky - překreslení vlastním testem změny pomocí časovače (hotovo), změna vzhledu, přidání vypnutí a zapnutí zvuku
################################
# File name: marble_kivy.app
#:kivy 2.1.0

import marble_funkce, marble_lang
from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

class MarbleApp(App):
    # načtení proměnných
    sirka_matice, pocet_barev, prirustek, min_rada, zisk, jazyk, zvuk = marble_funkce.nacti_data()
    # nastavení dalších proměnných
    texty = marble_lang.nacti_text(jazyk)
    grid_size, zmenseni, old_width, old_height = 0, 8, 0, 0
    offset = (0, 0)
    circles = {}
    cas_posunu, cas_pauzy, cas_zmizeni, cas_testu_zmeny_velikosti = 0.05, 0.5, 0.05, 0.1
    body, krok = 0, 0
    animace, barva, cesta, cil, cil_pozice, kulicky, pole, pozice_vybrane_kulicky, smazat_mista, test_zmeny_velikosti, vyber, zvuky = None, None, None, None, None, None, None, None, None, None, None, None
    hp, platno = None, None
    hra_bezi, hrac_je_na_tahu, je_vybrana_kulicka, byla_hra = False, False, False, False
    
    def build(self):
        self.barva = []
        for i in range(self.pocet_barev+1):
            self.barva.append(Image(source='images/b' + str(i).zfill(2) + '.png'))
        self.zvuky = [SoundLoader.load('sounds/01.wav'),\
                      SoundLoader.load('sounds/02.wav'),\
                      SoundLoader.load('sounds/03.wav'),\
                      SoundLoader.load('sounds/04.wav'),\
                      SoundLoader.load('sounds/05.wav')]
        self.hra = self.root.ids.obrazovka_hry.ids
        self.hp = self.hra.herni_pole
        self.platno = self.hp.canvas
        self.nastaveni = self.root.ids.obrazovka_nastaveni.ids
        self.hp.bind(on_touch_down=self.stisk_vyber_kulicky)
        self.nastav_texty()
        self.test_zmeny_velikosti = Clock.schedule_interval(self.je_zmena_velikosti, self.cas_testu_zmeny_velikosti)
    
    def nastav_texty(self):
        self.texty = marble_lang.nacti_text(self.jazyk)
        self.hra.btn_start.text = self.texty[0]
        self.hra.btn_nastaveni.text = self.texty[2]
        self.hra.btn_vysledky.text = str(self.body)
    
    def je_zmena_velikosti(self, dt):
        # zkontroluje, zda se změnila velikost okna, pokud ano, tak je překreslí
        if self.old_height != self.hp.height or self.old_width != self.hp.width:
            self.vykresli_herni_pole()
            self.old_height, self.old_width = self.hp.height, self.hp.width

    def vykresli_herni_pole(self, *args):
        # POZOR - nereaguje na situaci maximalizace okna a zpět ve windows
        if self.hra_bezi:
            # vypočte pozice a rozestupy
            width, height = self.hp.width, self.hp.height
            self.grid_size = int(min(width, height)) // self.sirka_matice
            size = self.grid_size * self.sirka_matice
            x, y = self.hp.x + (width - size) // 2, self.hp.y + (height - size) // 2
            self.offset = (x, y)
            # vymaže plátno a seznam čar
            self.platno.clear()
            # nakreslí mřížku a kuličky
            with self.platno:
                Color(1, 1, 1, 0.5)
                for offset in range(0, size + self.grid_size, self.grid_size):
                    Line(points=(x, y + offset, x + size, y + offset))
                    Line(points=(x + offset, y, x + offset, y + size))
                Color(1, 1, 1, 1)
                if self.vyber != None:
                    self.vyber = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + self.grid_size * self.pozice_vybrane_kulicky[0], self.offset[1] + self.grid_size * self.pozice_vybrane_kulicky[1]), size=(self.grid_size, self.grid_size))
                for x, y in self.circles.keys():
                    self.add_ball(x, y)
                if self.cil != None:
                    self.cil = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + self.grid_size * self.cil_pozice[0], self.offset[1] + self.grid_size * self.cil_pozice[1]), size=(self.grid_size, self.grid_size))
        elif self.byla_hra:
            self.oznam_konec()
    
    def remove_ball(self, x, y):
        circle = self.circles.pop((x, y))
        self.platno.remove(circle)
    
    def add_ball(self, x, y, pozadi = False):
        grid = self.grid_size
        with self.platno:
            Color(1,1,1,1)
            if pozadi:
                self.vyber = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + grid * x, self.offset[1] + grid * y), size=(grid, grid))
            self.circles[(x, y)] = Ellipse(texture=self.barva[self.pole[x][y]].texture, pos=(self.offset[0] + grid * x + self.zmenseni // 2, self.offset[1] + grid * y + self.zmenseni // 2), size=(grid - self.zmenseni, grid - self.zmenseni))
    
    def oznam_konec(self):
        # Oznámení konce hry a dosaženého počtu bodů
        self.platno.clear()
        with self.platno:
            Label(text=self.texty[3] + str(self.body), font_size='24sp', halign='center', center=self.hp.center)
    
    def smaz_vybery(self, dt):
        self.platno.remove(self.vyber)
        self.platno.remove(self.cil)
        self.vyber, self.cil = None, None
        self.hrac_je_na_tahu = True
    
    def animuj_zmizeni(self, dt):
        # animace smazání řady
        if self.krok < len(self.smazat_mista):
            self.remove_ball(self.smazat_mista[self.krok][0],self.smazat_mista[self.krok][1])
            self.krok += 1
        else:
            self.animace.cancel()     
            self.hrac_je_na_tahu = True
    
    def animuj(self, dt):
        # přesun kuličky do cíle
        if self.zvuk:
            self.zvuky[1].play()
        self.remove_ball(self.cesta[self.krok][0],self.cesta[self.krok][1])
        self.add_ball(self.cesta[self.krok+1][0],self.cesta[self.krok+1][1])
        self.krok += 1
        if self.krok > len(self.cesta)-2:
            self.platno.remove(self.cil)
            self.animace.cancel()
            self.vyber, self.cil = None, None
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
        self.hra.btn_vysledky.text = str(self.body)
        if len(self.smazat_mista) > 0:
            # smazání řady
            for misto in self.smazat_mista:
                self.pole[misto[0]][misto[1]] = 0
            self.krok = 0
            if self.zvuk:
                self.zvuky[2].play()
            self.animace = Clock.schedule_interval(self.animuj_zmizeni, self.cas_zmizeni)
        else:
            # pokud se pole zaplnilo, ukonči hru
            if marble_funkce.je_pole_plne(self.pole):
                self.hra_bezi = False
                self.hra.btn_start.text = self.texty[0]
                self.platno.clear()
                self.circles = {}
                self.hra.btn_nastaveni.disabled = False
                self.byla_hra = True
                if self.zvuk:
                    self.zvuky[3].play()
                self.oznam_konec()
            else:
                self.hrac_je_na_tahu = True
    
    def sld_sirka_matice_change(self, instance, value):
        self.nastaveni.lb_sirka_matice.text = self.texty[4] + str(value)
    
    def sld_pocet_barev_change(self, instance, value):
        self.nastaveni.lb_pocet_barev.text = self.texty[5] + str(value)
    
    def sld_prirustek_change(self, instance, value):
        self.nastaveni.lb_prirustek.text = self.texty[6] + str(value)
    
    def sld_min_rada_change(self, instance, value):
        self.nastaveni.lb_min_rada.text = self.texty[7] + str(value)
    
    def stisk_start(self): # akce při stisku tlačítka start hry
        if self.hra_bezi: # hra probíhá, dojde k jejímu předčasnému ukončení
            self.hra.btn_start.text = self.texty[0]
            self.platno.clear()
            self.circles = {}
            self.hra.btn_nastaveni.disabled = False
            self.hra_bezi = False
            self.byla_hra = True
            self.vyber, self.cil = None, None
            if self.zvuk:
                self.zvuky[3].play()
            self.oznam_konec()
        else:   # hra začíná
            self.body = 0
            self.hra.btn_vysledky.text = str(self.body)
            self.hra.btn_start.text = self.texty[1]
            self.hra.btn_nastaveni.disabled = True
            self.pole = marble_funkce.vytvor_pole(self.sirka_matice) # vytvoření herního pole
            self.hra_bezi = True
            self.vykresli_herni_pole() # smaže herní pole a nakreslí čáry
            self.old_height, self.old_width = self.hp.width, self.hp.height
            self.herni_kolo()
    
    def stisk_nastaveni(self):
        self.nastaveni.lb_sirka_matice.text = self.texty[4] + str(self.sirka_matice)
        self.nastaveni.lb_pocet_barev.text = self.texty[5] + str(self.pocet_barev)
        self.nastaveni.lb_prirustek.text = self.texty[6] + str(self.prirustek)
        self.nastaveni.lb_min_rada.text = self.texty[7] + str(self.min_rada)
        self.nastaveni.lb_zisk.text = self.texty[8]
        self.nastaveni.lb_jazyk.text = self.texty[9]
        self.nastaveni.btn_uloz.text = self.texty[10]
        self.nastaveni.btn_zpet.text = self.texty[11]
        self.nastaveni.sld_sirka_matice.value = self.sirka_matice
        self.nastaveni.sld_pocet_barev.value = self.pocet_barev
        self.nastaveni.sld_prirustek.value = self.prirustek
        self.nastaveni.sld_min_rada.value = self.min_rada
        self.nastaveni.ti_zisk.text = self.zisk
        self.nastaveni.sp_jazyk.text = self.jazyk
        self.nastaveni.sp_jazyk.values = marble_lang.jazyky()
        self.root.current = 'ObrazovkaNastaveni'
    
    def stisk_uloz(self):
        self.sirka_matice = self.nastaveni.sld_sirka_matice.value
        self.pocet_barev = self.nastaveni.sld_pocet_barev.value
        self.prirustek = self.nastaveni.sld_prirustek.value
        self.min_rada = self.nastaveni.sld_min_rada.value
        self.zisk = self.nastaveni.ti_zisk.text
        self.jazyk = self.nastaveni.sp_jazyk.text
        marble_funkce.uloz_data(self.sirka_matice, self.pocet_barev, self.prirustek, self.min_rada, self.zisk, self.jazyk, self.zvuk)
        self.nastav_texty()
        self.root.current = 'ObrazovkaHry'
    
    def stisk_zpet(self):
        self.root.current = 'ObrazovkaHry'
        
    def stisk_vyber_kulicky(self, instance, touch):
        # akce při výběru kuličky nebo prázdného pole
        grid = self.grid_size
        if self.hra_bezi and self.hrac_je_na_tahu: # pokud probíhá hra a hráč je na tahu tak pokračuj, jinak nic
            # výpočet hranic herní mřížky
            x, y = touch.pos
            x_min, y_min = self.offset
            x_max = x_min + grid * self.sirka_matice
            y_max = y_min + grid * self.sirka_matice
            if x >= x_min and y >= y_min and x < x_max and y < y_max: # pokud je kliknuto do mřížky, zjisti pozici kliknutí, jinak skonči
                # výpočet kam se kliklo
                i, j = int((x - self.offset[0])/grid), int((y - self.offset[1])/grid)
                self.hrac_je_na_tahu = False
                if self.je_vybrana_kulicka: # je vybraná kulička, kterou chceme přesunout, nyní vybíráme kam
                    if self.pole[i][j] > 0:
                        # změna výběru kuličky, původní dej zpět, označ novou
                        if self.zvuk:
                            self.zvuky[0].play()
                        self.platno.remove(self.vyber)
                        self.pozice_vybrane_kulicky = [i, j]
                        self.je_vybrana_kulicka = True
                        self.remove_ball(i, j)
                        self.add_ball(i, j, True)
                        self.hrac_je_na_tahu = True
                    else:
                        # označ cíl a zavolej animaci
                        self.cil_pozice = [i, j]
                        with self.platno:
                            Color(1,1,1,1)
                            self.cil = Rectangle(texture=self.barva[0].texture, pos=(self.offset[0] + grid * i, self.offset[1] + grid * j), size=(grid, grid))
                        je_cesta, self.cesta = marble_funkce.najdi_cestu(self.pole, self.pozice_vybrane_kulicky, self.cil_pozice)
                        self.je_vybrana_kulicka = False
                        if je_cesta:
                            self.pole[self.cesta[-1][0]][self.cesta[-1][1]] = self.pole[self.cesta[0][0]][self.cesta[0][1]]
                            self.pole[self.cesta[0][0]][self.cesta[0][1]] = 0
                            self.krok = 0
                            self.platno.remove(self.vyber)
                            self.animace = Clock.schedule_interval(self.animuj, self.cas_posunu)
                        else: # cesta nenalezena
                            if self.zvuk:
                                self.zvuky[4].play()
                            Clock.schedule_once(self.smaz_vybery, self.cas_pauzy)
                else: # vybíráme kuličku, kterou chceme přesunout
                    if self.pole[i][j] > 0: # klikli jsme na kuličku?
                        self.pozice_vybrane_kulicky = [i, j]
                        if self.zvuk:
                            self.zvuky[0].play()
                        self.je_vybrana_kulicka = True
                        self.remove_ball(i, j)
                        self.add_ball(i, j, True)
                    self.hrac_je_na_tahu = True

if __name__ == '__main__':
    LabelBase.register(name='Roboto', fn_regular='Roboto-Medium.ttf')
    MarbleApp().run()