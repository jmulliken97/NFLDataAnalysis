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
        
    def determine_stats_type(self, stats):
        passing_headers = ['Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY']
        rushing_headers = ['Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM']
        receiving_headers = ['Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']

        stats_keys = stats.keys()

        if all(item in stats_keys for item in passing_headers):
            return "passing"
        elif all(item in stats_keys for item in rushing_headers):
            return "rushing"
        elif all(item in stats_keys for item in receiving_headers):
            return "receiving"
        else:
            return "unknown"


    def calculate_score(self, player_data):
        player = player_data.copy()
        stats_type = self.determine_stats_type(player_data)
        weights = None
        if stats_type == "passing":
            weights = {
                "Pass Yds": 0.05,
                "Yds/Att": 0.15,
                "Cmp %": 0.15,
                "TD:INT Ratio": 0.2,
                "Rate": 0.05,
                "Sck": -0.05,
                "SckY": -0.05,
                "ANY/A": 0.2,
            }

            if player.get("INT") != 0:
                player["TD:INT Ratio"] = round(player["TD"] / player["INT"], 2)
            else:
                player["TD:INT Ratio"] = round(player["TD"], 2)

            player["ANY/A"] = round((player["Pass Yds"] + 20 * player["TD"] - 45 * player["INT"] - player["SckY"]) / (player["Att"] + player["Sck"]), 2)

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

    def flatten(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

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
                for year, year_data in data.items():
                    for player, stats in year_data.items():
                        stats['Score'] = self.calculate_score(stats)
                    self.data_dict[year] = pd.DataFrame.from_records(list(year_data.values()))

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
  
    def correlation_analysis(self, year):
        if year in self.data_dict:
            numeric_df = self.data_dict[year].select_dtypes(include=[np.number])  
            return numeric_df.corr()
        return None

    def descriptive_stats(self, year=None):
        if year is None: 
            combined_df = pd.concat(self.data_dict.values())  
        elif year in self.data_dict:  
            combined_df = self.data_dict[year]
        else:
            return None

        numeric_df = combined_df.select_dtypes(include=[np.number])

        return numeric_df.describe()
    
    def compare_stats(self, stats, players, years=None):
        comparison_results = ""
        for year, dataframe in self.data_dict.items():
            if years and year not in years:
                continue
            for player in players:
                player_data = dataframe[dataframe['Player'] == player]
                print(f"Data for player {player} in {year}: {player_data}")
                if not player_data.empty:
                    comparison_results += f"Stats for {player} in {year}:\n"
                    for stat in stats:
                        stat_value = player_data[stat].values[0]
                        comparison_results += f"{stat}: {stat_value}\n"
                    comparison_results += "\n"
        return comparison_results

    def plot_stats(self, stat_columns, player_names, years=None):
        df_selected = pd.DataFrame()
        for year, dataframe in self.data_dict.items():
            if years and year not in years:
                continue
            df_year_selected = dataframe[dataframe['Player'].isin(player_names)][['Player'] + stat_columns]
            df_year_selected['Year'] = year  
            df_selected = pd.concat([df_selected, df_year_selected])
        df_melted = df_selected.melt(id_vars=['Player', 'Year'], var_name='Stat', value_name='Value')

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Player', y='Value', hue='Stat', data=df_melted)
        plt.title('Player Stats Comparison')
        plt.show()

