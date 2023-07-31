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
                if clean_name[-1].isalpha() and len(clean_name[-1]) == 1:
                    clean_name = clean_name[:-1]
                stats['Player'] = clean_name
        return data

    def clean_data(self, data):
        data = self.clean_player_name(data)
        data = self.clean_lg_field(data)
        return data

    def calculate_score(self, player_data):
        player = player_data.copy()
        
        def determine_stats_type(stats):
            stats_keys = stats.keys()
            stat_types = [("passing", ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%', 'Int', 'Int%', 'Lg TD', 'Lg', 'Sack', 'Loss', 'Rate']), 
                        ("rushing", ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD']),
                        ("receiving", ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD', 'Tar', 'YAC'])]

            for stat_type, headers in stat_types:
                if all(item in stats_keys for item in headers):
                    return stat_type
            return "unknown"

        stats_type = determine_stats_type(player_data)
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
            for key in ["Yds", "YPA", "Pct", "TD", "Int", "Rate", "Sack", "Loss", "Att"]:
                if key in player:
                    player[key] = float(player[key])
                                
            if player.get("Int") != 0:
                player["TD:INT Ratio"] = round(player["TD"] / player["Int"], 2)
            else:
                player["TD:INT Ratio"] = round(player["TD"], 2)

            player["ANY/A"] = round((player["Yds"] + 20 * player["TD"] - 45 * player["Int"] - player["Loss"]) / (player["Att"] + player["Sack"]), 2)

        elif stats_type == "rushing":
            player["Y/A"] = player["Yds"] / player["Att"] if player["Att"] else 0
            player["TD/A"] = player["TD"] / player["Att"] if player["Att"] else 0
            player["TD/G"] = player["TD"] / player["Gms"] if player["Gms"] else 0

            weights = {
                "Yds": 0.15,
                "Att": 0.15,
                "TD": 0.15,
                "Avg": 0.15,
                "YPG": 0.1,
                "Lg": 0.05,
                "Y/A": 0.1,
                "TD/A": 0.1,
                "TD/G": 0.1
            }

        elif stats_type == "receiving":
            player["Y/R"] = player["Yds"] / player["Rec"] if player["Rec"] else 0
            player["TD/R"] = player["TD"] / player["Rec"] if player["Rec"] else 0
            player["Y/Tgt"] = player["Yds"] / player["Tar"] if player["Tar"] else 0
            player["Rec/Tgt"] = player["Rec"] / player["Tar"] if player["Tar"] else 0
            player["TD/G"] = player["TD"] / player["Gms"] if player["Gms"] else 0

            weights = {
                "Rec": 0.1,
                "Yds": 0.1,
                "TD": 0.15,
                "Avg": 0.1,
                "YPG": 0.1,
                "Lg": 0.1,
                "Tar": 0.05,
                "YAC": 0.05,
                "Y/R": 0.05,
                "TD/R": 0.05,
                "Y/Tgt": 0.05,
                "Rec/Tgt": 0.05,
                "TD/G": 0.1
            }

        if weights is None:
            return None

        score = 0
        for stat, weight in weights.items():
            if player.get(stat) is not None:
                score += player.get(stat, 0) * weight

        return round(score, 2), player.get("TD:INT Ratio"), player.get("ANY/A"), player

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
                self.data_dict = {}
                for year, year_data in data.items():
                    df = pd.DataFrame.from_records(list(year_data.values()))
                    scores = []
                    td_int_ratios = []
                    any_as = []
                    efficiency_metrics = {"Y/A": [], "TD/A": [], "TD/G": [], 
                                        "Y/R": [], "TD/R": [], "Y/Tgt": [], "Rec/Tgt": []}
                    for _, player in df.iterrows():
                        score, td_int_ratio, any_a, updated_player = self.calculate_score(player)
                        scores.append(score)
                        if td_int_ratio is not None:
                            td_int_ratios.append(round(td_int_ratio, 2))
                        if any_a is not None:
                            any_as.append(round(any_a, 2))
                        for metric in efficiency_metrics.keys():
                            if updated_player.get(metric) is not None: 
                                efficiency_metrics[metric].append(round(updated_player.get(metric), 2))
                    df['Score'] = scores
                    if td_int_ratios:
                        df['TD:INT Ratio'] = td_int_ratios
                    if any_as:
                        df['ANY/A'] = any_as
                    for metric, values in efficiency_metrics.items():
                        if values and values[0] is not None:  # only append if the list is not empty and the first value is not None
                            df[metric] = values
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
    
    def detect_outliers(self, year=None):
        if year is None: 
            combined_df = pd.concat(self.data_dict.values())
        elif year in self.data_dict:
            combined_df = self.data_dict[year]
        else:
            return None
        numeric_df = combined_df.select_dtypes(include=[np.number])
        Q1 = numeric_df.quantile(0.25)
        Q3 = numeric_df.quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = (numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))
        outliers_df = numeric_df[outlier_mask]

        outliers_df = outliers_df.dropna(how='all')

        return outliers_df

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


