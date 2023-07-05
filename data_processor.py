import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import json
import collections

class DataProcessor:
    def __init__(self, text_edit_widget):
        self.data_dict = {}
        self.textEdit = text_edit_widget
        
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
                    stats['Year'] = year  # Add the year to the stats
                    stats['Player'] = player  # Add the player name to the stats
                    flattened_data.append(stats)
                
        return pd.DataFrame(flattened_data)

    def load_json(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open JSON File", "", "JSON Files (*.json)")
        if file_name[0]:
            self.file_name = file_name[0]  # Store the file name to display it later
            with open(self.file_name, 'r') as json_file:
                data = json.load(json_file)
                for year, year_data in data.items():
                    self.data_dict[year] = pd.DataFrame.from_records(list(year_data.values()))

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
        if year in self.data_dict and sort_order != "No Sort":
            self.data_dict[year].sort_values(by=sort_by, axis=0, ascending=(sort_order == "Ascending"), inplace=True)
            
    def get_sortable_columns(self, year):
        if year in self.data_dict:
            return self.data_dict[year].columns.tolist()
        return []

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



