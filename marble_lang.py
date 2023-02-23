#!/usr/bin/python3
#############################
# Modul: marble_data.py
# Autor: Jaroslav Porplycia
# Datum: 2023/01/26
# Verze: 0.01

###############################
# Log:
# # 2023/01/26 JP - vytvoření souboru pro uložení dat - varianta python souboru místo dosavadního conf
################################

def nacti_text(jazyk):
    if jazyk == 'česky':
        texty = ['Začni hru','Ukonči hru','Nastavení','Konec hry.\nDosažený počet bodů: ','Šířka hracího pole: ','Počet barev: ','Přírůstek kuliček: ','Délka řady pro smazání: ','Zisk za počet kuliček','Jazyk','Uložit a zavřít','Zpět bez uložení']
    elif jazyk == 'english':
        texty = ['Start Game','End Game','Settings','End Game!\nNumber of points achieved: ','Width of playing field: ','Number of colours: ','Marble increment: ','Length of row for deletion: ','Profit per number of marbles:','Language:','Save and close','Back without saving']
    elif jazyk ==  'espanol':
        texty = ['Empezar Juego','Terminar Juego','Ajustes','¡Terminar Juego!\nNúmero de puntos obtenidos: ','Anchura del campo de juego: ','Número de colores: ','Incremento de canicas: ','Longitud de la fila para borrar: ','Ganancia por número de canicas:','Idioma:','Guardar y cerrar','Volver sin guardar']
    elif jazyk == 'polska':
        texty = ['Początek gry', 'Koniec gry', 'Ustawienia', 'Koniec gry!\nLiczba uzyskanych punktów: ','Szerokość pola gry: ','Liczba kolorów: ','Przyrost marmurków: ','Długość rzędu do skreślenia: ','Zysk za liczbę marmurków:','Język:','Zapisz i zamknij','Powrót bez zapisywania']
    elif jazyk == 'deutsch':
        texty = ['Spiel starten','Spiel beenden','Einstellungen','Spiel beenden!\nAnzahl der erreichten Punkte: ','Breite des Spielfeldes: ','Anzahl der Farben: ','Murmeltierschrittweite: ','Länge der zu löschenden Reihe: ','Gewinn pro Anzahl Murmeln:','Sprache:','Speichern und schließen','Zurück ohne Speichern']
    else:
        texty = []
    return(texty)

def jazyky():
    return(['česky','english','espanol','polska','deutsch'])