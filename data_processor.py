import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import json
import collections

class DataProcessor:
    def __init__(self, text_edit_widget):
        self.data_dict = {}
        self.textEdit = text_edit_widget
        
    def determine_stats_type(self, stats):
        passing_headers = ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY']
        rushing_headers = ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM']
        receiving_headers = ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']

        stats_keys = stats.keys()

        if all(item in stats_keys for item in passing_headers):
            return "passing"
        elif all(item in stats_keys for item in rushing_headers):
            return "rushing"
        elif all(item in stats_keys for item in receiving_headers):
            return "receiving"
        else:
            return "unknown"

    def calculate_score(self, player, stats_type):
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

            # Calculate the touchdown-to-interception ratio
            if player["INT"] != 0:
                player["TD:INT Ratio"] = round(player["TD"] / player["INT"], 2)
            else:
                # If no interceptions,use the number of touchdowns
                player["TD:INT Ratio"] = round(player["TD"], 2)

            # Calculate the Adjusted Net Yards per Attempt
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

        score = 0
        for stat, weight in weights.items():
            score += player[stat] * weight

        return score

    def flatten(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
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
            self.file_name = file_name[0]  # Store the file name to display it later
            with open(self.file_name, 'r') as json_file:
                data = json.load(json_file)
                for year, year_data in data.items():
                    for player, stats in year_data.items():
                        stats_type = self.determine_stats_type(stats)
                        if stats_type != "unknown":
                            self.calculate_score(stats, stats_type)
                    self.data_dict[year] = pd.DataFrame.from_records(list(year_data.values()))
            # Save the updated data back to the file
            with open(self.file_name, 'w') as json_file:
                json.dump(data, json_file)

    def get_file_name(self):
        return self.file_name if hasattr(self, 'file_name') else 'No file loaded.'
    
    def get_player_names(self, year):
        if year in self.data_dict:
            return self.data_dict[year]['Player'].unique().tolist()
        return []

    def get_stat_columns(self, year):
        if year in self.data_dict:
            return self.data_dict[year].columns.tolist()
        return []
    
    def sort_dataframe(self, year, sort_by, sort_order): 
        df = self.data_dict[year]
        if sort_order == "Ascending":
            self.data_dict[year] = df.sort_values(by=sort_by)
        else:
            self.data_dict[year] = df.sort_values(by=sort_by, ascending=False)  
 
    def get_sortable_columns(self, year):
        if year in self.data_dict:
            return self.data_dict[year].columns.tolist()
        return []
    
    def compare_stats(self, year, stats, players):
        comparison_results = ""
        for player in players:
            player_data = self.data_dict[year][self.data_dict[year]['Player'] == player]
            if not player_data.empty:
                comparison_results += f"Stats for {player}:\n"
                for stat in stats:
                    stat_value = player_data[stat].values[0]
                    comparison_results += f"{stat}: {stat_value}\n"
                comparison_results += "\n"
        return comparison_results
    
    def plot_stats(self, year, stat_columns, player_names):
        if year in self.data_dict:
            bar_width = 0.35
            fig, ax = plt.subplots()

            for idx, stat in enumerate(stat_columns):
                stat_values = []
                for player in player_names:
                    player_data = self.data_dict[year][self.data_dict[year]['Player'] == player]
                    if not player_data.empty:
                        stat_value = player_data[stat].values[0]
                        stat_values.append(stat_value)

                x_offset = (idx - len(stat_columns)/2)*bar_width
                ax.bar([i + x_offset for i in range(len(player_names))], stat_values, width=bar_width, align='center', label=stat)

            ax.set_ylabel('Stats Value')
            ax.set_title('Player Stats Comparison')
            ax.set_xticks(range(len(player_names)))
            ax.set_xticklabels(player_names)
            ax.legend()

            fig.tight_layout()
            plt.show()



