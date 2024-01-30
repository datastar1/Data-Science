# Programmieren mit Python
# Projektarbeit Klimadiagramm
# Gruppe C
# Teilbereich: Data Quality (Nutzung der Pandas Bibliothek)
# Entwickler: Gero Krikawa
# Datum: 24.11.2022

import pandas as pd
from pandas_profiling import ProfileReport

""" 
Funktion zur Erstellung eines Daten Profilreport zur Beurteilung der Datenqualität
Tutorial: https://pandas-profiling.ydata.ai/docs/master/index.html

Input:  Mannheim_data.csv
output: Mannheim_DataProfil.html
"""

def create_data_profilreport(input_data_file):
    df = pd.read_csv(input_data_file)
    print(df.info())
    print(df.to_string)

    # umfangreicher Profilreport: minimal=False
    # einfacher Profilreport (bei großen Datenmengen) : minimal=True
    prof = ProfileReport(df, minimal=False)

    # create filename for export in html
    output_data_file_list = input_data_file.split(".")
    output_data_file = output_data_file_list[0] + "_Profil.html"
    print(output_data_file)
    #Output in html file
    prof.to_file(output_file=output_data_file)



data_input_file = "Mannheim_data.csv"
create_data_profilreport(data_input_file)
