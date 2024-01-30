### Tag 16     24.11.22
### Sebastian Kulwicki
### Projektarbeit Klimadiagram

### JSON Klimadaten auf Karte ploten

import json                                                 # Import json Bibliothek für das Einlesen

with open('..\Daten\weatherstations.json', 'r', encoding="UTF-8") as ws:    # Wetterdaten json Datei zum Lesen öffnen
    weatherstation = json.load(ws)                                          # geöffnete json lesen
    stadt_list = weatherstation['Stadt']                                    # Aus Rubrik Stadt in stadt_list übernehmen
    # print(weatherstation["Stadt"])                                        # Ausgabe des erstellten Dictionary
    # print(len(weatherstation['Stadt']))                                   # Ausgabe der Länge des Dictionary

# Erstellung von CSV-Datei für die Daten der Wetterstation
for i in range(0, len(stadt_list)):                                   # mit Schleife alle Listeneinträge zuweisen
    ort = stadt_list[i]['Name']                                       # zuweisen Ort zu Stadt
    long = stadt_list[i]['Longitute']                                 # zuweisen Longitute zu long
    lat = stadt_list[i]['Latitude']                                   # zuweisen Latitude zu lat
    pkt = stadt_list[i]['size']                                       # zuweisen size zu pkt


import plotly.express as px                                 # Import Plotly Bibliothek für den Plot
# import pandas as pd                                       # Import pandas Bibliothek für CSV Einlesen
from plotly import offline                                  # Import Plotly Offline Bibliothek Offline Ausgabe

# de_cities = pd.read_csv("..\Daten\CSV deutschland.csv")   # Einlesen der CSV mit den Geografischen Datensätzen

fig = px.scatter_mapbox(                                    # Beschreibung der Figur
    stadt_list,                                             # Liste aus virtueller Liste
    lon="Latitude",                                         # zuweisen des Breitengrads
    lat="Longitute",                                        # zuweisen des Längengrads
    hover_name="Name",                                      # zuweisen des anzuzeigenden Title das Hover Textfelds
    # hover_data=["Bundesland", "Einwohner"],               # zuweisen weiterer Hover Textfeld Einträge
    color_discrete_sequence=["fuchsia"],                    # zuweisen der Farbe für Punkte und Hover Textfeld
    size="size",                                            # zuweisen der Größe für die Darstellung
    size_max=10,                                            # zugewiesene Größe mit einem Maximum begrenzen
    zoom=5.4,                                               # zuweisen des Standardwerts für das Zoomlevel
    height=900,                                             # zuweisen der Kartenfenster Höhe
    width=700,                                              # zuweisen der Kartenfenster Breite
    )

fig.update_layout(                                              # Erweitern der Figur Beschreibung
                  title_text="Wetterstationen",                 # zuweisen deiner Karten Überschrift
                  title_x=0.5,                                  # zuweisen der Karten Überschrift Position
                  mapbox=dict(                                  # zuweisen weiterer Kartendarstellungsparameter
                      center={'lat': 51.3515, 'lon': 10.4262},  # zuweisen des Standardwerts für die Start Koordinaten
                      style="open-street-map",                  # zuweisen eines Kartentyps / Projektionstyp
                             )
                  )

offline.plot(fig, filename='D:/Projekt/Stationen.html')     # Ausgabe der Figur als Offline Html Datei im Webbrowser
#fig.show()


# import webview                                              # Import Webview zur Ausgabe der Figur im tkinter Fenster
# from tkinter import *                                       # Import tkinter zum Erstellen eines tkinter Fenster
#
# tk = Tk()                                                   # aufruf eines tkinter Fenster
# tk.title('Wetterstationen')                                 # zuweisen eines Titels des tkinter Fenster
# tk.geometry('400x600+50+50')                                # zuweisen einer Fernster größe
#                                                             # (breite x höhe + abstand oben + abstand links)
#
# webview.create_window('Wetterstationen',                             # erstellen eines WebView Fenster mit Titel
#                       'http://localhost:63342/PyCharm'               # Aufruf der lokalen Html Datei über
#                       '/Stationen.html?_ijt=qqa5a'                   # Localhost und Port Nummer
#                       'smvcrgo0rhtmpi3qqqneq&'
#                       '_ij_reload=RELOAD_ON_SAVE'
#                       )
#
# webview.start()                                             # Aufruf der Figur über die WebView
#                                                             # innerhalb eines tkinter Fenster





