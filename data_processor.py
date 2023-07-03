import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import json

class DataProcessor:
    def __init__(self):
        self.data_df = None

    def load_json(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open JSON File", "", "JSON Files (*.json)")
        if file_name[0]:
            with open(file_name[0], 'r') as json_file:
                data = json.load(json_file)
                self.data_df = pd.DataFrame(data).transpose()
                sort_order = self.comboBox_sort.currentText()
                if sort_order != "No Sort":
                    self.data_df.sort_values(by="YDS", axis=0, ascending=(sort_order == "Ascending"), inplace=True)
                self.textEdit.setText(self.data_df.to_string())

    def plot_stats(self, stat_columns, player_names):
        plt.figure(figsize=(10, 6))

        for stat in stat_columns:
            for player in player_names:
                if player in self.data_df.index:
                    self.data_df.loc[player, stat].plot(kind='line', label=f'{player} {stat}')

        plt.ylabel("Stats Value")
        plt.title("Player Stats Comparison")
        plt.legend()
        plt.show()
