# Programmieren mit Python
# Projektarbeit Klimadiagramm
# Gruppe C
# Teilbereich: Data Quality (Nutzung der Pandas Bibliothek)
# Entwickler: Gero Krikawa
# Datum: 24.11.2022

import pandas as pd

# Funktionen zur Prüfung der Datenqualität
# Missing Values, Unique Values, Maximum Values, Minimum Values
# Inputfile: Mannheim_data.csv
def data_quality_rep(input_data_file):
    data = pd.read_csv(input_data_file, sep= ',')

    # DataFrame - datatypes
    data_types = pd.DataFrame(data.dtypes, columns=['Data Type'])

    # Check for missing data:
    missing_data = pd.DataFrame(data.isnull().sum(), columns=['Missing Values'])

    # Check if the values are unique
    unique_values = pd.DataFrame(columns=['Unique Values'])
    for row in list(data.columns.values):
        unique_values.loc[row] = [data[row].nunique()]

    # maximum values
    maximum_values = pd.DataFrame(columns=['Maximum Value'])
    for row in list(data.columns.values):
        maximum_values.loc[row] = [data[row].max()]

    # minimum values
    minimum_values = pd.DataFrame(columns=['Minimum Value'])
    for row in list(data.columns.values):
        minimum_values.loc[row] = [data[row].min()]


    dq_report = data_types.join(missing_data).join(unique_values).join(maximum_values).join(minimum_values)
    print(dq_report)


data_input_file ='Mannheim_data.csv'

data_quality_rep(data_input_file)