import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5 import QtWidgets
import json
from collections.abc import MutableMapping
import numpy as np

class DataProcessor:
    def __init__(self, text_edit_widget):
        self.data_dict = {}
        self.textEdit = text_edit_widget
        self.league = None
        self.passing_headers = ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%', 'T%', 'Int', 'Int%', 'I%', 'Lg', 'Sack', 'Loss', 'Rate']
        self.rushing_headers = ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM']
        self.receiving_headers = ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM']
        
    def determine_stats_type(self, stats):
        stats_keys = stats.keys()
        stat_types = [("passing", self.passing_headers), 
                      ("rushing", self.rushing_headers), 
                      ("receiving", self.receiving_headers)]

        for stat_type, headers in stat_types:
            if all(item in stats_keys for item in headers):
                return stat_type

        return "unknown"
    
    @classmethod
    def clean_lg_field(cls, data):
        for year, players in data.items():
            for player, stats in players.items():
                if 'Lg' in stats and isinstance(stats['Lg'], str):
                    stats['Lg TD'] = 't' in stats['Lg']
                    stats['Lg'] = int(stats['Lg'].replace('t', ''))
        return data
    
    @classmethod
    def clean_player_name(cls, data):
        for year, players in data.items():
            for player, stats in players.items():
                name_parts = stats['Player'].split('\xa0')
                clean_name = name_parts[0]
                if '.' in clean_name:
                    clean_name = clean_name.split('.')[0]
                stats['Player'] = clean_name
        return data

    
    def clean_data(self, data):
        data = self.clean_player_name(data)
        data = self.clean_lg_field(data)
        return data

    def calculate_score(self, player_data):
        player = player_data.copy()
        stats_type = self.determine_stats_type(player_data)
        weights = None
        if stats_type == "passing":
            weights = {
                "Yds": 0.05,
                "YPA": 0.15,
                "Pct": 0.15,
                "TD:INT Ratio": 0.2,
                "Rate": 0.05,
                "Sack": -0.05,
                "Loss": -0.05,
                "ANY/A": 0.2,
            }

            if player.get("Int") != 0:
                player["TD:INT Ratio"] = round(player["TD"] / player["Int"], 2)
            else:
                player["TD:INT Ratio"] = round(player["TD"], 2)

            player["ANY/A"] = round((player["Yds"] + 20 * player["TD"] - 45 * player["Int"] - player["Loss"]) / (player["Att"] + player["Sack"]), 2)

        elif stats_type == "rushing":
            weights = {
                "Rush Yds": 0.05,
                "Att": 0.15,
                "TD": 0.2,
                "20+": 0.05,
                "40+": 0.05,
                "Lng": 0.2,
                "Rush 1st": 0.05,
                "Rush 1st%": 0.15,
                "Rush FUM": -0.1,
            }
        
        elif stats_type == "receiving":
            weights = {
                "Rec": 0.15,
                "Yds": 0.15,
                "TD": 0.2,
                "20+": 0.05,
                "40+": 0.05,
                "LNG": 0.1,
                "Rec 1st": 0.1,
                "1st%": 0.1,
                "Rec FUM": -0.1,
                "Rec YAC/R": 0.05,
                "Tgts": 0.05,
            }

        if weights is None:
            return None

        score = 0
        for stat, weight in weights.items():
            score += player.get(stat, 0) * weight

        return score

    def flatten_json(self, data):
        flattened_data = []
        for year, players in data.items():
            for player, stats in players.items():
                if isinstance(stats, dict):
                    stats['Year'] = year  
                    stats['Player'] = player  
                    flattened_data.append(stats)
                
        return pd.DataFrame(flattened_data)
    
    def load_json(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open JSON File", "", "JSON Files (*.json)")
        if file_name[0]:
            self.file_name = file_name[0]
            with open(self.file_name, 'r') as json_file:
                data = json.load(json_file)
                data = self.clean_data(data)
                for year, year_data in data.items():
                    df = pd.DataFrame.from_records(list(year_data.values()))
                    for _, player in df.iterrows():
                        player['Score'] = self.calculate_score(player)
                    self.data_dict[year] = df

            with open(self.file_name, 'w') as json_file:
                json.dump(data, json_file)
                
            columns = self.get_columns()

    def get_file_name(self):
        return self.file_name if hasattr(self, 'file_name') else 'No file loaded.'
    
    def get_player_names(self, year=None):
        player_names = []
        if year is not None:
            if year in self.data_dict:
                player_names = self.data_dict[year]['Player'].unique().tolist()
        else:
            for year in self.data_dict:
                player_names.extend(self.data_dict[year]['Player'].unique().tolist())
        return list(set(player_names))

    def get_columns(self, year=None):
        if year:
            if year in self.data_dict:
                return self.data_dict[year].columns.tolist()
            else:
                return []
        else:
            all_columns = set()
            for df in self.data_dict.values():
                all_columns.update(df.columns.tolist())
            return list(all_columns)

    def sort_dataframe(self, year, sort_by, sort_order):
        dataframe = self.data_dict[year]
        if not sort_by:
            return
        if sort_order == "Ascending":
            self.data_dict[year] = dataframe.sort_values(by=sort_by)
        else:
            self.data_dict[year] = dataframe.sort_values(by=sort_by, ascending=False)
  
    def correlation_analysis(self, year=None):
        if year is None: 
            combined_df = pd.concat(self.data_dict.values())
        elif year in self.data_dict:  
            combined_df = self.data_dict[year]
        else: 
            return None
        numeric_df = combined_df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    def descriptive_stats(self, year=None):
        if year is None: 
            combined_df = pd.concat(self.data_dict.values())  
        elif year in self.data_dict:  
            combined_df = self.data_dict[year]
        else:
            return None
        numeric_df = combined_df.select_dtypes(include=[np.number])
        return numeric_df.describe()
    
    def distribution(self, stat, year=None):
        if year is None: 
            combined_df = pd.concat(self.data_dict.values())
        elif year in self.data_dict:
            combined_df = self.data_dict[year]
        else:
            return None
        stat_data = combined_df[stat]
        return stat_data

    def plot_player_stat(self, player_name, stat_column):
        df_selected = pd.DataFrame()
        for year, dataframe in self.data_dict.items():
            df_year_selected = dataframe[dataframe['Player'] == player_name][['Player', stat_column]]
            df_year_selected['Year'] = year  
            df_selected = pd.concat([df_selected, df_year_selected])
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Year', y=stat_column, data=df_selected)
        plt.title(f'{player_name} {stat_column} Over Years')
        plt.show()


