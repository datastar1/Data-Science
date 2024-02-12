# Programmieren mit Python
# Projektarbeit Klimadiagramm
# Gruppe C
# Teilbereich: Data Quality (Nutzung der Pandas Bibliothek)
# Entwickler: Gero Krikawa
# Datum: 24.11.2022


# Pandas Funktionen zur Datebereinigung

""" 
In Abhängigkeit der Datenqualität bzw. der identifizierten Datenprobleme aus dem Profilreport oder visueller Anzeige können 
unterschiedliche Funktionen auf den Datenbestand angewendet werden um diesen zu bereinigen
"""

import pandas as pd


# Funktionen zur Überprüfung der Datenqualität
# Missing Values, Unique Values, Maximum Values, Minimum Values
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




# drop unnecessary columns (reduce data amount)
def drop_columns(input_data_file, to_drop, output_data_file):
    df = pd.read_csv(input_data_file)
    #print(df.head())
    df.drop(to_drop, inplace=True, axis=1)                          # inplace operation, drop columns -> axis= 1
    # write new csv file
    df.to_csv(output_data_file, index=False, header=True)



# correct wrong values by rule
# rule definition ist important and defines further data quality!!
def correct_wrong_data_by_rule(input_data_file, var_wrong_value, output_data_file):
    df = pd.read_csv(input_data_file)
    for x in df.index:
        # defined rule to handle extreme values, here fix value for upper limit 50
        if df.loc[x, var_wrong_value] > 50:                         # access group of rows and columns by label
            #print("Var:", var_wrong_value, "with wrong value: ", df.loc[x, var_wrong_value])
            # replace via fix value
            # in this case: replace extreme value with empty value --> next function interpolate this empty entry
            df.loc[x, var_wrong_value] = ''
            """
            Tutorial DataFrame - loc property: 
            https://www.w3resource.com/pandas/dataframe/dataframe-loc.php
            https://towardsdatascience.com/a-python-beginners-look-at-loc-part-1-cb1e1e565ec2"""

    # write new csv file
    df.to_csv(output_data_file, index=False, header=True)



# Replace empty values with number (new_value) - fillna()
def replace_empty_values_with_number(input_data_file, var_empty_value, new_value, output_data_file):
    df = pd.read_csv(input_data_file)
    df[var_empty_value].fillna(new_value, inplace=True)

    df.to_csv(output_data_file, index=False, header=True)


# Replace empty values with mean/median/mode - fillna()
def replace_empty_value_with_mean_median_mode(input_data_file, var_empty_value, replace_typ, output_data_file):
    df = pd.read_csv(input_data_file)
    if replace_typ == "mean":
        # mean - Durchschnitt/Mittelwert: (Summe geteilt durch Anzahl Werte)
        new_value = df[var_empty_value].mean()
    elif replace_typ == "median":
        # median - Wert in der Mitte: alle Zahlen in aufsteigender Reihenfolge sortiert und dann Zahl in der Mitte der Verteilung ausgewählt
        new_value = df[var_empty_value].median()
    elif replace_typ == "mode":
        # mode - Wert der am häufigsten vorkommt
        new_value = df[var_empty_value].mode()

    # replace empty value with new value in column with empty values
    df[var_empty_value].fillna(new_value,inplace=True)

    # write new csv file
    df.to_csv(output_data_file, index=False, header=True)



#Replace empty values by interpolation
def replace_empty_values_interpolate(input_data_file, var_empty_value, output_data_file):
    df = pd.read_csv(input_data_file)
    #Interpolate in forward order across the column
    df[var_empty_value].interpolate(method='linear', limit_direction = 'forward', inplace=True)
    # write new csv file
    df.to_csv(output_data_file, index=False, header=True)




# *** Funktionsaufrufe für exemplarischen Beispiel Datensatz 'Mannheim_data.csv' ***
"""
Exemplarischen Beispiel Datensatz 'Mannheim_data.csv' ***
Datenfehler:
Variable: tmax
Missing Values: 20.04.1950 - 01.05.1950 --> tmax = ' '
Extremwerte: 15.06.1950 - 18.06.1950    --> tmax = 70
"""


#data_input_file = "Mannheim_data.csv"


# Schritt 1
"""Data_Quality_Report zur Beruteilung der Datenqualität vor der Datenbereinigung"""
print("\nDaten vor der Bereinigung")
print("var: tmax missing values: 12 - 20.04.1950 - 01.05.1950")
print("var: tmax extreme values: 70\n")

data_input_file = "Mannheim_data.csv"
data_quality_rep(data_input_file)


# Schritt 2
"""" Datenmenge reduzieren -> unnötige Spalten löschen"""
# Drop colums - reduce data size
data_input_file = "Mannheim_data.csv"
data_output_file="Mannheim_data_bearbeitet.csv"
# list of columns to drop
to_drop = ['wdir','wspd','wpgt','pres','tsun','snow']
drop_columns(data_input_file, to_drop, data_output_file)


# Schritt 3
"""Extremwerte korrigieren mit Regeln: hier Fixwert für tmax > 50 wird durch '' ersetzt und ich Schritt 4 durch Interpolation ersetzt 
# (Mannheim.csv: Extremwerte tmax: 15.06.1950 - 18.06.1950  -> 70 Grad)"""
# *** Replace wrong Value by Rule ***
data_input_file="Mannheim_data_bearbeitet.csv"
data_output_file="Mannheim_data_bearbeitet.csv"
var_wrong_value ="tmax"
correct_wrong_data_by_rule(data_input_file, var_wrong_value, data_output_file)


# Schritt 4
"""Leerstellen ersetzen durch Interpolation
Hinweis: Weitere Funktion um Leerstellen zu ersetzten (mean, median, mode) ebenfalls vorhanden   """

#Interpolate in forward order across the column
data_input_file="Mannheim_data_bearbeitet.csv"
data_output_file="Mannheim_data_bearbeitet.csv"
var_empty_value ="tmax"
replace_empty_values_interpolate(data_input_file, var_empty_value, data_output_file)



# Schritt 5
data_input_file = "Mannheim_data_bearbeitet.csv"
print("\nDaten nach der Bereinigung")
print("unnötige Spalten gelöscht, Var: tmax missing values und extrem values interpoliert\n")
data_quality_rep(data_input_file)






# *** Weitere Funktionen zur Datenbereinigung ***


#*** Replace Null Value with any Number ***
# data_output_file="Mannheim_data_bearbeitet.csv"
# var_null_value ="snow"
# var_new_value = 5000
# replace_empty_values_with_number(data_input_file, var_null_value, var_new_value, data_output_file)


#*** Replace Empty Value with Mean ***
#data_input_file = "Mannheim_data.csv"
#data_output_file="Mannheim_data_bearbeitet.csv"
#var_empty_value ="tmax"               # Variable with empty cells
#replace_typ ="mean"                   # replace_typ: mean, median, mode
#replace_empty_value_with_mean_median_mode(data_input_file, var_empty_value, replace_typ, data_output_file)


#Interpolate in forward order across the column
#replace_empty_values_interpolate(data_input_file, var_empty_value)