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

    match jazyk:
        case 'česky':
            texty = ['Marble','Začni hru','Ukonči hru','Nastavení','Konec hry','Konec hry! Počet bodů: ','Šířka hracího pole: ','Počet barev: ','Přírůstek kuliček: ','Délka řady pro smazání: ','Zisk za počet kuliček ','Adresa obrázků ','Adresa vybraných obrázků ','Jazyk ','Uložit a zavřít','Zpět bez uložení']

        case 'english':
            texty = ['Marble','Start Game','End Game','Settings','End Game','End Game! Number of points: ','Width of playing field: ','Number of colours: ','Marble increment: ','Length of row for deletion: ','Profit per number of marbles: ','Address of images: ','Address of selected images: ','Language: ','Save and close','Back without saving']

        case 'espanol':
            texty = ['Marble','Empezar Juego','Terminar Juego','Ajustes','Terminar Juego','¡Terminar Juego! Número de puntos: ','Anchura del campo de juego: ','Número de colores: ','Incremento de canicas: ','Longitud de la fila para borrar: ','Ganancia por número de canicas: ','Dirección de las imágenes: ','Dirección de las imágenes seleccionadas: ','Idioma: ','Guardar y cerrar','Volver sin guardar']
        
        case 'polska':
            texty = ['Marble', 'Początek gry', 'Koniec gry', 'Ustawienia', 'Koniec gry', 'Koniec gry! Liczba punktów: ','Szerokość pola gry: ','Liczba kolorów: ','Przyrost marmurków: ','Długość rzędu do skreślenia: ','Zysk za liczbę marmurków: ','Adres zdjęć: ','Adres wybranych zdjęć: ','Język: ','Zapisz i zamknij','Powrót bez zapisywania']
        
        case 'deutsch':
            texty = ['Marble','Spiel starten','Spiel beenden','Einstellungen','Spiel beenden','Spiel beenden! Anzahl der Punkte: ','Breite des Spielfeldes: ','Anzahl der Farben: ','Murmeltierschrittweite: ','Länge der zu löschenden Reihe: ','Gewinn pro Anzahl Murmeln: ','Adresse der Bilder: ','Adresse der ausgewählten Bilder: ','Sprache: ','Speichern und schließen','Zurück ohne Speichern']
            
    return(texty)