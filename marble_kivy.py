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
# # 2023/01/27 JP - 
################################
# File name: marble_kivy.app
#:kivy 2.1.0

import marble_funkce, marble_lang
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Line, Color
from kivy.uix.image import Image
from kivy.config import Config

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
    cas_posunu, cas_pauzy, rychlost_animace = 50, 500, 50
    body, krok = 0, 0
    pole, barva, kulicky, pozice_vybrane_kulicky, cil_pozice, cesta, smazat_mista,lines = [], [], [], [], [], [], [], []
    hra_bezi, hrac_je_na_tahu, vybrana_kulicka = False, False, False
    
    def build(self):
        Window.bind(size=self.on_size)
    
    def on_size(self, instance, value):
        if self.hra_bezi:
            self.vykresli_herni_pole()
    
    def nacti_obrazky(self):
        # načtení obrázků kuliček
        self.barva = []
        for i in range(self.pocet_barev):
            self.barva.append(Image(source='images/b' + str(i+1).zfill(2) + '.png'))
    
    def vykresli_herni_pole(self):
        herni_pole = self.root.ids.obrazovka_hry.ids.herni_pole
        # vymaže původní mřížku, pokud je
        for line in self.lines:
            herni_pole.canvas.remove(line)
        self.lines = []
        # nakreslí mřížku
        width, height = herni_pole.width, herni_pole.height
        grid_size = int(min(width, height)) // self.sirka_matice 
        size = grid_size * self.sirka_matice
        x, y = herni_pole.x + (width - size) // 2, herni_pole.y + (height - size) // 2
        
        with herni_pole.canvas:
            Color(1, 1, 1, 0.5)
            for offset in range(0, size + grid_size, grid_size):
                self.lines.append(Line(points=(x, y + offset, x + size, y + offset)))
                self.lines.append(Line(points=(x + offset, y, x + offset, y + size)))    
    
    def start_hry(self): # akce při stisku tlačítka start hry
        if self.hra_bezi: # hra probíhá, dojde k jejímu předčasnému ukončení
            self.root.ids.obrazovka_hry.ids.btn_start.text = 'Začni hru'
            self.root.ids.obrazovka_hry.ids.herni_pole.canvas.clear()
            self.root.ids.obrazovka_hry.ids.btn_nastaveni.disabled = False
            self.hra_bezi = False
        else:   # hra začíná
            self.body = 0
            self.root.ids.obrazovka_hry.ids.btn_vysledky.text = str(self.body)
            self.root.ids.obrazovka_hry.ids.btn_start.text = 'Ukonči hru'
            self.root.ids.obrazovka_hry.ids.btn_nastaveni.disabled = True
            self.pole = marble_funkce.vytvor_pole(self.sirka_matice) # vytvoření herního pole
            self.vykresli_herni_pole() # smaže herní pole a nakreslí čáry
            self.nacti_obrazky()
            self.hra_bezi = True
            self.herni_kolo()
    
    def herni_kolo(self):
        self.smazat_mista, pocet_bodu = marble_funkce.zkontroluj_rady(self.pole, self.min_rada, self.zisk)
        if pocet_bodu == 0:
            nove_kulicky = marble_funkce.nove_kulicky(self.pole, self.prirustek, self.pocet_barev)
            ###self.prekresli_obraz() - TADY PŘIDÁME FUNKCI VYKRESLENÍ KULIČEK
            self.smazat_mista, pocet_bodu = marble_funkce.zkontroluj_rady(self.pole, self.min_rada, self.zisk)
        self.body += pocet_bodu
        ###self.lcd.display(self.body)
        if len(self.smazat_mista) > 0:
            # smazání řady
            for misto in self.smazat_mista:
                self.pole[misto[0]][misto[1]] = 0
            self.krok = 0
            ###self.snd_rada.play()
            ###self.pauza_az.start(self.rychlost_animace)
        else:
            # pokud se pole zaplnilo, ukonči hru
            if marble_funkce.je_pole_plne(self.pole):
                self.hra_bezi = False
                ###self.btn_nova_hra.setText(texty[1])
                ###self.btn_nastaveni.setEnabled(True)
                ###self.oznam_konec()
            else:
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
        #self.zisk = [int(n) for n in self.root.ids.obrazovka_nastaveni.ids.ti_zisk.text.split(',')]
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
if __name__ == '__main__':
    LabelBase.register(name='Roboto', fn_regular='Roboto-Medium.ttf')
    MarbleApp().run()

    
    '''
    def prekresli_obraz(self):
        # překreslí kuličky v přížce
        for i in range(sirka_matice):
            for j in range(sirka_matice):
                self.kulicky[i][j].setPixmap(self.barva[self.pole[i][j]])

    def vyber_kulicky_stisk(self, event):
    # akce při výběru kuličky nebo prázdného pole
    if self.hra_bezi and self.hrac_je_na_tahu:
        # pokud probíhá hra a hráč je na tahu tak pokračuj, jinak nic
        self.hrac_je_na_tahu = False
        point = event.scenePosition()
        i = int((point.y()-self.odsazeni_shora)/self.sirka_pole)
        j = int((point.x()-self.odsazeni_zleva)/self.sirka_pole)
        if self.vybrana_kulicka:
            # je vybraná kulička, kterou chceme přesunout, nyní vybíráme kam
            if self.pole[i][j] > 0:
                # změna výběru kuličky, původní dej zpět, označ novou
                self.kulicky[self.pozice_vybrane_kulicky[0]][self.pozice_vybrane_kulicky[1]].setPixmap(self.barva[self.pole[self.pozice_vybrane_kulicky[0]][self.pozice_vybrane_kulicky[1]]])
                self.snd_klik.play()
                self.pozice_vybrane_kulicky = [i, j]
                self.kulicky[i][j].setPixmap(self.barva_vyber[self.pole[i][j]])
                self.hrac_je_na_tahu = True
            else:
                # označ cíl a zavolej animaci
                self.cil_pozice = [i, j]
                self.kulicky[i][j].setPixmap(self.barva_vyber[0])
                je_cesta, self.cesta = marble_funkce.najdi_cestu(self.pole, self.pozice_vybrane_kulicky, self.cil_pozice)
                self.vybrana_kulicka = False
                if je_cesta:
                    self.animuj()
                else:
                    # cesta nenalezena, zruš výběr kuliček
                    self.snd_necesta.play()
                    self.pauza.start(self.cas_pauzy)
        else:
            # vybíráme kuličku, kterou chceme přesunout
            if self.pole[i][j] > 0:
                self.snd_klik.play()
                self.pozice_vybrane_kulicky = [i, j]
                self.vybrana_kulicka = True
                self.kulicky[i][j].setPixmap(self.barva_vyber[self.pole[i][j]])
            self.hrac_je_na_tahu = True
                    
    def konec_pauzy(self):
        # dokončení zrušení výběru kuliček při nenalezení cesty, je vyžadována pauza před tímto krokem, aby byl vidět výběr a jeho zrušení, bez pauzy to zanikalo
        self.pauza.stop()
        self.kulicky[self.pozice_vybrane_kulicky[0]][self.pozice_vybrane_kulicky[1]].setPixmap(self.barva[self.pole[self.pozice_vybrane_kulicky[0]][self.pozice_vybrane_kulicky[1]]])
        self.kulicky[self.cil_pozice[0]][self.cil_pozice[1]].setPixmap(self.barva[self.pole[self.cil_pozice[0]][self.cil_pozice[1]]])
        self.vybrana_kulicka = False
        self.hrac_je_na_tahu = True
    
    def animuj(self):
        # přesun kuličky do cíle
        self.pole[self.cesta[-1][0]][self.cesta[-1][1]] = self.pole[self.cesta[0][0]][self.cesta[0][1]]
        self.pole[self.cesta[0][0]][self.cesta[0][1]] = 0
        self.krok = 0
        self.snd_posun.setLoopCount(len(self.cesta)-1)
        self.snd_posun.play()
        self.pauza_krok.start(self.cas_posunu)
    
    def krok_krok(self):
        if self.krok == len(self.cesta)-1:
            self.pauza_krok.stop()
            self.herni_kolo()
        else:
            self.kulicky[self.cesta[self.krok][0]][self.cesta[self.krok][1]].setPixmap(self.barva[0])
            self.kulicky[self.cesta[self.krok+1][0]][self.cesta[self.krok+1][1]].setPixmap(self.barva[self.pole[self.cesta[-1][0]][self.cesta[-1][1]]])
            self.krok += 1
    
    def animuj_zmizeni(self):
        # animace smazání řady
        if self.krok < len(self.smazat_mista):
            self.kulicky[self.smazat_mista[self.krok][0]][self.smazat_mista[self.krok][1]].setPixmap(self.barva[0])
            self.krok += 1
        else:
            self.pauza_az.stop()      
            self.hrac_je_na_tahu = True
    
    def oznam_konec(self):
        # Oznámení počtu bodů na konci hry
        self.snd_konec.play()
        dlg = QMessageBox(self)
        dlg.setWindowTitle(texty[4])
        dlg.setText(texty[5] + ' ' + str(self.body))
        button = dlg.exec()
    '''
    
    