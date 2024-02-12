from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.offsetbox import AnchoredText
import os.path

matplotlib.use('TkAgg')
show_reg = False
bearbeitet = ''
normals_periods = 1


class Klimadiagramm:
    # Input der Daten für Diagramm, Plotten per Funktion innerhalb der Klasse
    def __init__(self, city_name, startdate, enddate, dia_type):

        self.city_name = city_name
        self.startdate = startdate
        self.enddate = enddate
        self.dia_type = dia_type

    def diagramm_printer(self):
        # Auslesen der csv-Files, abspeichern als Pandas Dataframes, Umwandeln der Datumsformate
        # Je nach Diagrammtyp (daily, monthly, annually, normals) plotten des Diagramms
        filename = f'{self.city_name}_data{bearbeitet}.csv'
        df_wetterdaten = pd.read_csv(filename, usecols=['time', 'tavg', 'tmin', 'tmax', 'prcp'])
        df_wetterdaten['daily'] = pd.to_datetime(df_wetterdaten['time'])
        global meteo_root

        # Plot dia_type = daily ##############################################################
        if self.dia_type == 'daily':
            # Datenaufbereitung entfällt, da bereits als daily Datensatz

            # Initialisierung Tkinter

            meteo_root = tk.Tk()
            meteo_root.wm_title("Klimadiagramm")

            # Plotten der Daten

            df_wetterdaten = df_wetterdaten.loc[
                (df_wetterdaten['daily'] >= self.startdate) & (df_wetterdaten['daily'] <= self.enddate)]
            if len(df_wetterdaten) / 1.5 <= 12:
                breite = len(df_wetterdaten) / 1.5
            else:
                breite = 12

            fig, ax2 = plt.subplots(figsize=(breite, 6), layout='constrained')
            ax1 = ax2.twinx()
            ax1.set_xlabel('Zeitraum', fontsize=11)
            ax1.plot(df_wetterdaten.daily, df_wetterdaten.tmax, color='crimson', label='tmax')
            ax1.plot(df_wetterdaten.daily, df_wetterdaten.tavg, color='orange', label='tavg')
            ax1.plot(df_wetterdaten.daily, df_wetterdaten.tmin, color='gold', label='tmin')
            ax1.fill_between(df_wetterdaten.daily, df_wetterdaten.tmin, df_wetterdaten.tmax, color='peru', alpha=0.5)
            ax1.set_ylabel('Temperatur (°C)', fontsize=11, color='orangered')
            # ax1.set(ylim=(-20, 40), yticks=np.arange(-20, 40, 5))
            ax1.yaxis.set_label_position('left')
            ax1.yaxis.set_ticks_position('left')
            for label in ax1.get_yticklabels():
                label.set_color('orangered')
            ax1.grid()
            ax2.bar(df_wetterdaten.daily, df_wetterdaten.prcp, color='mediumblue')
            ax2.set_ylabel('Niederschlag (mm)', fontsize=11, color='mediumblue')
            # ax2.set(ylim=(0, 60))
            ax2.yaxis.set_label_position('right')
            ax2.yaxis.set_ticks_position('right')
            for label in ax2.get_yticklabels():
                label.set_color('mediumblue')
            plt.legend(loc='upper left')
            plt.setp(ax2.get_xticklabels(), rotation=75, ha='right')
            plt.title(f'Wetterdaten {self.city_name} nach Tagen', fontsize=14)

            # Übergabe a Tkinter

            meteo_canvas = FigureCanvasTkAgg(fig, master=meteo_root)
            plot_widget = meteo_canvas.get_tk_widget()
            plot_widget.grid(row=0, column=0, columnspan=2)
            button = tk.Button(master=meteo_root, text="Quit", command=_quit)
            button.grid(row=1, column=0)
            # Button wird nur angezeigt, wenn bearbeitetes File existiert
            checkfile = f'{city_name}_data_bearbeitet.csv'
            if os.path.exists(checkfile):
                button3 = tk.Button(master=meteo_root, text='Show improved data', command=set_improved)
                button3.grid(row=1, column=1)

            # Toolbar
            toolbar = NavigationToolbar2Tk(meteo_canvas, meteo_root, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=2, column=0, columnspan=2)

            meteo_root.mainloop()

        # Plot dia_type = monthly ##############################################################
        elif self.dia_type == 'monthly':
            # Aggregierung der Datenbasis
            df_wetterdaten = df_wetterdaten.loc[
                (df_wetterdaten['daily'] >= self.startdate) & (df_wetterdaten['daily'] < self.enddate)]
            df_wetterdaten['monthly'] = df_wetterdaten['daily'].dt.strftime('%Y%m')
            df_wetterdaten_agg = df_wetterdaten.groupby(
                by='monthly', as_index=False).agg(
                {'tavg': 'mean', 'tmin': 'mean', 'tmax': 'mean', 'prcp': 'sum'})
            df_wetterdaten_agg['ausgabe'] = pd.to_datetime(df_wetterdaten_agg['monthly'], format='%Y%m')
            df_wetterdaten_agg['ausgabe'] = df_wetterdaten_agg['ausgabe'].dt.strftime('%Y %b')

            # Initialisierung Tkinter

            meteo_root = tk.Tk()
            meteo_root.wm_title("Klimadiagramm")

            # Plotten der Daten

            if len(df_wetterdaten_agg) / 1.5 <= 12:
                breite = len(df_wetterdaten_agg) / 1.5
            else:
                breite = 12
            fig, ax2 = plt.subplots(figsize=(breite, 6), layout='constrained')
            ax1 = ax2.twinx()
            ax1.set_xlabel('Zeitraum', fontsize=11)
            ax1.plot(df_wetterdaten_agg.ausgabe, df_wetterdaten_agg.tmax, color='crimson', label='tmax')
            ax1.plot(df_wetterdaten_agg.ausgabe, df_wetterdaten_agg.tavg, color='orange', label='tavg')
            ax1.plot(df_wetterdaten_agg.ausgabe, df_wetterdaten_agg.tmin, color='gold', label='tmin')
            ax1.fill_between(df_wetterdaten_agg.ausgabe, df_wetterdaten_agg.tmin, df_wetterdaten_agg.tmax, color='peru', alpha=0.5)
            ax1.set_ylabel('Temperatur (°C)', fontsize=11, color='orangered')
            ax1.set(ylim=(-20, 100), yticks=np.arange(-20, 100, 5))
            ax1.yaxis.set_label_position('left')
            ax1.yaxis.set_ticks_position('left')
            for label in ax1.get_yticklabels():
                label.set_color('orangered')
            ax1.grid()
            ax2.bar(df_wetterdaten_agg.ausgabe, df_wetterdaten_agg.prcp, color='mediumblue')
            ax2.set_ylabel('Niederschlag (mm)', fontsize=11, color='mediumblue')
            ax2.set(ylim=(-40, 200), yticks=np.arange(-40, 200, 10))
            ax2.yaxis.set_label_position('right')
            ax2.yaxis.set_ticks_position('right')
            for label in ax2.get_yticklabels():
                label.set_color('mediumblue')
            plt.legend(loc='upper left')
            plt.setp(ax2.get_xticklabels(), rotation=75, ha='right')
            plt.title(f'Wetterdaten {self.city_name} nach Monaten', fontsize=14)

            # Übergabe an Tkinter

            meteo_canvas = FigureCanvasTkAgg(fig, master=meteo_root)
            plot_widget = meteo_canvas.get_tk_widget()
            plot_widget.grid(row=0, column=0, columnspan=2)
            button = tk.Button(master=meteo_root, text="Quit", command=_quit)
            button.grid(row=1, column=0)
            # Button wird nur angezeigt, wenn bearbeitetes File existiert
            checkfile = f'{city_name}_data_bearbeitet.csv'
            if os.path.exists(checkfile):
                button3 = tk.Button(master=meteo_root, text='Show improved data', command=set_improved)
                button3.grid(row=1, column=1)

            # Toolbar
            toolbar = NavigationToolbar2Tk(meteo_canvas, meteo_root, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=2, column=0, columnspan=2)

            meteo_root.mainloop()

        # Plot dia_type = annually ##############################################################
        elif self.dia_type == 'annually':
            # Aggregierung der Datenbasis
            df_wetterdaten = df_wetterdaten.loc[
                (df_wetterdaten['daily'] >= self.startdate) & (df_wetterdaten['daily'] < self.enddate)]
            df_wetterdaten['annually'] = df_wetterdaten['daily'].dt.strftime('%Y')
            df_wetterdaten_agg = df_wetterdaten.groupby(
                by='annually', as_index=False).agg(
                {'tavg': 'mean', 'tmin': 'mean', 'tmax': 'mean', 'prcp': 'sum'})
            # Berechnung der linearen Regression mit scipy
            list_years_str = df_wetterdaten_agg['annually'].tolist()
            list_years = list(map(int, list_years_str))
            list_tavg = df_wetterdaten_agg['tavg'].tolist()
            b, a, r, p, std = linregress(list_years, list_tavg)
            b_rnd = round(b, 3)
            # annually ist string und muss durch int_Liste ersetzt werden (Darstellung Regressionsgerade)
            df_wetterdaten_agg.insert(loc=5, column='year', value=list_years)

            # Initialisierung Tkinter

            meteo_root = tk.Tk()
            meteo_root.wm_title("Klimadiagramm")

            # Plotten der Daten
            if len(df_wetterdaten_agg) / 1.5 <= 12:
                breite = len(df_wetterdaten_agg) / 1.5
            else:
                breite = 12
            fig, ax2 = plt.subplots(figsize=(breite, 6), layout='constrained')
            ax1 = ax2.twinx()
            ax1.set_xlabel('Zeitraum', fontsize=11)
            ax1.plot(df_wetterdaten_agg.year, df_wetterdaten_agg.tmax, color='crimson', label='tmax')
            ax1.plot(df_wetterdaten_agg.year, df_wetterdaten_agg.tavg, color='orange', label='tavg')
            ax1.plot(df_wetterdaten_agg.year, df_wetterdaten_agg.tmin, color='gold', label='tmin')
            ax1.fill_between(df_wetterdaten_agg.year, df_wetterdaten_agg.tmin, df_wetterdaten_agg.tmax, color='peru',
                             alpha=0.5)
            if show_reg:
                ax1.plot(df_wetterdaten_agg.year, (a + (df_wetterdaten_agg.year * b)), 'k--', label='regression')
            ax1.set_ylabel('Temperatur (°C)', fontsize=11, color='orangered')
            # ax1.set(yticks=np.arange(5, 20, 2.5))
            ax1.yaxis.set_label_position('left')
            ax1.yaxis.set_ticks_position('left')
            for label in ax1.get_yticklabels():
                label.set_color('orangered')
            ax1.grid()
            ax2.bar(df_wetterdaten_agg.year, df_wetterdaten_agg.prcp, color='mediumblue')
            ax2.set_ylabel('Jahresiederschlag (mm)', fontsize=11, color='mediumblue')
            # ax2.set(ylim=(0, 1000))
            ax2.yaxis.set_label_position('right')
            ax2.yaxis.set_ticks_position('right')
            for label in ax2.get_yticklabels():
                label.set_color('mediumblue')
            plt.legend(loc='upper left')
            plt.setp(ax2.get_xticklabels(), rotation=75, ha='right')
            # plt.text(6, 8, f'Jährliche Temperaturentwicklung:\n{b_rnd}°C')
            if show_reg:
                reg_text = AnchoredText(f'Jährliche Temperaturentwicklung:\n{b_rnd}°C', loc='upper right')
                ax2.add_artist(reg_text)
            plt.title(f'Wetterdaten {self.city_name} nach Jahren', fontsize=14)

            # Übergabe an Tkinter

            meteo_canvas = FigureCanvasTkAgg(fig, master=meteo_root)
            plot_widget = meteo_canvas.get_tk_widget()
            plot_widget.grid(row=0, column=0, columnspan=3)
            button = tk.Button(master=meteo_root, text="Quit", command=_quit)
            button.grid(row=1, column=0)
            button2 = tk.Button(master=meteo_root, text='Show regression', command=set_regression)
            button2.grid(row=1, column=1)
            # button3 wird nur angezeigt, wenn bearbeitetes File existiert
            checkfile = f'{city_name}_data_bearbeitet.csv'
            if os.path.exists(checkfile):
                button3 = tk.Button(master=meteo_root, text='Show improved data', command=set_improved)
                button3.grid(row=1, column=2)

            # Toolbar
            toolbar = NavigationToolbar2Tk(meteo_canvas, meteo_root, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=2, column=0, columnspan=3)

            meteo_root.mainloop()

        # plot dia_type = normals (30-Jahres-Klimaperioden) ######################################
        elif self.dia_type == 'normals':
            # Aggregierung der Datenbasis
            df_wetterdaten['monthly'] = df_wetterdaten['daily'].dt.strftime('%Y%m')
            df_wetterdaten_agg = df_wetterdaten.groupby(
                by='monthly', as_index=False).agg(
                {'tavg': 'mean', 'tmin': 'mean', 'tmax': 'mean', 'prcp': 'sum'})
            # Funktion zur Zuordnung der Klimaperioden
            df_wetterdaten_agg['normal'] = df_wetterdaten_agg.apply(make_normals, axis=1)
            df_wetterdaten_agg['monthly2'] = pd.to_datetime(df_wetterdaten_agg['monthly'], format='%Y%m', errors='ignore')
            df_wetterdaten_agg['month'] = df_wetterdaten_agg.monthly2.dt.month
            df_wetterdaten_agg_tmp = df_wetterdaten_agg.groupby(
                by=['normal', 'month'], as_index=False).agg(
                {'tavg': 'mean', 'tmin': 'mean', 'tmax': 'mean', 'prcp': 'mean'})

            # Initialisierung Tkinter

            meteo_root = tk.Tk()
            meteo_root.wm_title("Klimadiagramm")

            # Plotten der Daten
            if normals_periods == 1:
                df_wetterdaten_agg = df_wetterdaten_agg_tmp.loc[(df_wetterdaten_agg_tmp.normal == '1990 - 2021')]
                zeitraum = '1990 bis 2020'
                fig, ax2 = plt.subplots(figsize=(12, 6), layout='constrained')
                ax1 = ax2.twinx()
                ax1.set_xlabel('Zeitraum', fontsize=11)
                ax1.plot(df_wetterdaten_agg.month, df_wetterdaten_agg.tavg, color='orangered', linewidth=3)
                ax1.set_ylabel('Temperatur (°C)', fontsize=11, color='orangered')
                ax1.set(ylim=(-20, 100), yticks=np.arange(-20, 100, 5))
                ax1.yaxis.set_label_position('left')
                ax1.yaxis.set_ticks_position('left')
                for label in ax1.get_yticklabels():
                    label.set_color('orangered')
                ax1.grid()
                ax2.bar(df_wetterdaten_agg.month, df_wetterdaten_agg.prcp, color='mediumblue')
                ax2.set_ylabel('Niederschlag (mm)', fontsize=11, color='mediumblue')
                ax2.set(ylim=(-40, 200), yticks=np.arange(-40, 200, 10))
                ax2.yaxis.set_label_position('right')
                ax2.yaxis.set_ticks_position('right')
                for label in ax2.get_yticklabels():
                    label.set_color('mediumblue')
                ax2.set_xticks(range(1, 13))
                plt.setp(ax2.get_xticklabels(which='both'))
                plt.title(f'Klimadiagramm {self.city_name} im Zeitraum {zeitraum}', fontsize=14)
            elif normals_periods == -1:
                df_wetterdaten_agg = df_wetterdaten_agg_tmp.loc[(df_wetterdaten_agg_tmp.normal == '1961 - 1990')]
                zeitraum = '1961 - 1990'
                fig, ax2 = plt.subplots(figsize=(12, 6), layout='constrained')
                ax1 = ax2.twinx()
                ax1.set_xlabel('Zeitraum', fontsize=11)
                ax1.plot(df_wetterdaten_agg.month, df_wetterdaten_agg.tavg, color='orangered', linewidth=3)
                ax1.set_ylabel('Temperatur (°C)', fontsize=11, color='orangered')
                ax1.set(ylim=(-20, 100), yticks=np.arange(-20, 100, 5))
                ax1.yaxis.set_label_position('left')
                ax1.yaxis.set_ticks_position('left')
                for label in ax1.get_yticklabels():
                    label.set_color('orangered')
                ax1.grid()
                ax2.bar(df_wetterdaten_agg.month, df_wetterdaten_agg.prcp, color='mediumblue')
                ax2.set_ylabel('Niederschlag (mm)', fontsize=11, color='mediumblue')
                ax2.set(ylim=(-40, 200), yticks=np.arange(-40, 200, 10))
                ax2.yaxis.set_label_position('right')
                ax2.yaxis.set_ticks_position('right')
                for label in ax2.get_yticklabels():
                    label.set_color('mediumblue')
                ax2.set_xticks(range(1, 13))
                plt.setp(ax2.get_xticklabels(which='both'))
                plt.title(f'Klimadiagramm {self.city_name} im Zeitraum {zeitraum}', fontsize=14)

            # Übergabe an Tkinter

            meteo_canvas = FigureCanvasTkAgg(fig, master=meteo_root)
            plot_widget = meteo_canvas.get_tk_widget()
            plot_widget.grid(row=0, column=0, columnspan=3)
            button = tk.Button(master=meteo_root, text="Quit", command=_quit)
            button.grid(row=1, column=0)
            button2 = tk.Button(master=meteo_root, text='Change climate period', command=set_normals_period)
            button2.grid(row=1, column=1)
            # Button wird nur angezeigt, wenn bearbeitetes File existiert
            checkfile = f'{city_name}_data_bearbeitet.csv'
            if os.path.exists(checkfile):
                button3 = tk.Button(master=meteo_root, text='Show improved data', command=set_improved)
                button3.grid(row=1, column=2)

            # Toolbar
            toolbar = NavigationToolbar2Tk(meteo_canvas, meteo_root, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=2, column=0, columnspan=3)

            meteo_root.mainloop()


def diagramm_server(city_name, startdate, enddate, dia_type):
    global my_diagramm
    my_diagramm = Klimadiagramm(city_name, startdate, enddate, dia_type)
    my_diagramm.diagramm_printer()


def _quit():
    # Quit-Button für Diagramme
    global show_reg
    meteo_root.quit()
    meteo_root.destroy()
    show_reg= False


def set_regression():
    global show_reg
    show_reg = True
    meteo_root.destroy()
    my_diagramm.diagramm_printer()


def set_improved():
    global bearbeitet
    bearbeitet = '_bearbeitet'
    meteo_root.destroy()
    my_diagramm.diagramm_printer()


def set_normals_period():
    global normals_periods
    normals_periods = normals_periods * -1
    meteo_root.destroy()
    my_diagramm.diagramm_printer()


def make_normals(row):
    if row['monthly'] < '196101':
        val = 'vor 1961'
    elif row['monthly'] < '199101':
        val = '1961 - 1990'
    elif row['monthly'] < '202101':
        val = '1990 - 2021'
    elif row['monthly'] < '205101':
        val = 'ab 2021'
    return val


# Test der Funktion
# city_name = 'Mannheim'
# startdate = datetime.strptime('01,04,1950', '%d,%m,%Y')
# enddate = datetime.strptime('01,08,1950', '%d,%m,%Y')
# dia_type = 'daily'
#
# my_diagramm = diagramm_server(city_name, startdate, enddate, dia_type)
