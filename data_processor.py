import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import json

class DataProcessor:
    def __init__(self, text_edit_widget):
        self.data_df = None
        self.textEdit = text_edit_widget

    def load_json(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open JSON File", "", "JSON Files (*.json)")
        if file_name[0]:
            self.file_name = file_name[0]  # Store the file name to display it later
            with open(self.file_name, 'r') as json_file:
                data = json.load(json_file)
                self.data_df = pd.DataFrame(data).transpose()
            
                # Remove the 'Player' column from the DataFrame if it exists
                if 'Player' in self.data_df.columns:
                    self.data_df.drop(columns=['Player'], inplace=True)

                self.textEdit.setText(self.data_df.to_string())
                
    def get_file_name(self):
        return self.file_name if hasattr(self, 'file_name') else 'No file loaded.'
    
    def get_player_names(self):
        if self.data_df is not None:
            return self.data_df.index.tolist()
        return []

    def get_stat_columns(self):
        if self.data_df is not None:
            return self.data_df.columns.tolist()
        return []
    
    def sort_dataframe(self, sort_by, sort_order):
        if self.data_df is not None and sort_order != "No Sort":
            self.data_df.sort_values(by=sort_by, axis=0, ascending=(sort_order == "Ascending"), inplace=True)
            self.textEdit.setText(self.data_df.to_string())
            
    def get_sortable_columns(self):
        if self.data_df is not None:
            return self.data_df.columns.tolist()
        return []

    def plot_stats(self, stat_columns, player_names):
        if self.data_df is not None:
            bar_width = 0.35
            fig, ax = plt.subplots()

            for idx, stat in enumerate(stat_columns):
                stat_values = []
                for player in player_names:
                    if player in self.data_df.index:
                        stat_value = self.data_df.loc[player, stat]
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


