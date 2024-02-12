import json
from datetime import datetime
from meteostat import Point, Daily

# definierte Parameter für den Gesamtenzeitraum der verfügbaren Daten der gewählten Stationen
start = datetime(1950, 1, 1)
end = datetime(2021, 12, 31)

avg_temp = []
date_list = []
stadt_list = []

"""Durch das Gruppen projekt ist der Code nicht sehr umfangreich, da viel über 
rechere und vergleichen der Outputs stattgefunden hat, daher wurde später eine
JSON manuell erstellt mit den Ausgewählten Wetterstationen"""

"""funktionsfähiger code, allerdings aufgrund der Menge der Stationen nicht verwendet"""
# einlesen der Erstellten JSON mit den Daten der ausgewählten Wetterstationen
# with open('lite.json', 'r', encoding="UTF-8") as ws:
#     weatherstation = json.load(ws)
#
#
# for i in range(0, len(weatherstation)):
#     if weatherstation[i]['country'] == 'DE':
#         stadt = str((weatherstation[i]['name']['en']))
#         stadt = stadt.replace("/", "_")
#         stadt = stadt.replace(" ", "_")
#         stadt = stadt.replace("___", "_")
#         stadt = stadt.replace(",", "_")
#         stadt = stadt.replace("._", "_")
#         long = (weatherstation[i]['location']['latitude'])
#         lat = (weatherstation[i]['location']['longitude'])
#         elevation = (weatherstation[i]['location']['elevation'])
#         start_time_str = weatherstation[i]['inventory']['daily']['start']
#         end_time_str = weatherstation[i]['inventory']['daily']['end']
#         if start_time_str and end_time_str:
#             try:
#                 start_time = datetime.strptime(start_time_str, '%Y-%m-%d')
#                 end_time = datetime.strptime(end_time_str, '%Y-%m-%d')
#                 if start_time <= start and end <= end_time:
#                     stadt_list.append(stadt)
#                     gps = Point(long, lat, elevation)
#                     data = Daily(gps, start, end)
#                     data = data.fetch()
#                     # data.to_csv(f'.\CSVs\{stadt}_data.csv')
#             except Warning as w:
#                 i += 1


# öffnent die Manuell erstellte Datei mit den Stationsdaten
with open('weatherstations.json', 'r', encoding="UTF-8") as ws:
    weatherstation = json.load(ws)
    stadt_list = weatherstation['Stadt']
    print(weatherstation["Stadt"])
    print(len(weatherstation['Stadt']))
    # Erstellung von CSV-Datei für die Daten der Wetterstation
    for i in range(0, len(stadt_list)):
        ort = stadt_list[i]['Name']
        long = stadt_list[i]['Longitute']
        lat = stadt_list[i]['Latitude']

        gps = Point(long, lat)
        data = Daily(gps, start, end)
        data = data.fetch()
        data.to_csv(f'.\CSVs\{ort}_data.csv')
