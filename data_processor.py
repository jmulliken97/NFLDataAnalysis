import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5 import QtWidgets
from collections.abc import MutableMapping
import numpy as np
from data_loader import DataLoader

class DataProcessor:
    def __init__(self, bucket_name=None, text_edit_widget=None):
        if bucket_name is None:
            options = QtWidgets.QFileDialog.Options()
            bucket_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select the S3 Bucket (JSON File)", "", "JSON Files (*.json);;All Files (*)", options=options)
            if not bucket_name:
                raise ValueError("No S3 bucket (JSON file) selected.")
        self.data_loader = DataLoader(bucket_name)
        self.textEdit = text_edit_widget
        self.data_dict = {}
        self.file_years_dict = {}
        self.passing_headers = ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%', 'T%', 'Int', 'Int%', 'I%', 'Lg', 'Sack', 'Loss', 'Rate']
        self.rushing_headers = ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM']
        self.receiving_headers = ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD', 'Tar', 'YAC']
        self.defense_headers = ['Player', 'Team', 'Gms', 'Int', 'Yds', 'Avg', 'Lg TD', 'Lg', 'TD', 'Solo', 'Ast', 'Tot', 'Sack', 'YdsL']
        self.kicking_headers = ['Player', 'Team', 'Gms', 'PAT', 'FG', '0-19', '20-29', '30-39', '40-49', '50+', 'Lg TD', 'Lg', 'Pts']  
        
    def load_and_process_data(self, preloaded_data, stats_type):
        data = preloaded_data.get(stats_type)
        if not data:
            raise ValueError(f"No data found for stats type: {stats_type}")
        self.data_dict = self.process_data(data)
        for key, value in self.data_dict.items():
            print(key, ":", value.keys())
        return list(self.data_dict.keys())

    
    def flatten_data(self, data):
        flattened_data = []
        for year, players_data in data.items():
            for player_name, player_stats in players_data.items():
                player_stat_copy = player_stats.copy()
                player_stat_copy['Year'] = year
                flattened_data.append(player_stat_copy)
        return flattened_data

    def process_data(self, data):
        flattened_data = self.flatten_data(data)
        df = pd.DataFrame(flattened_data)
        
        result_dict = {}
        
        for year, group in df.groupby('Year'):
            efficiency_metrics = {
                "Y/A": [], "TD/A": [], "TD/G": [], 
                "Y/R": [], "TD/R": [], "Y/Tgt": [], "Rec/Tgt": []
            }

            for _, player in group.iterrows():
                for metric in efficiency_metrics.keys():
                    if player.get(metric) is not None: 
                        efficiency_metrics[metric].append(round(player.get(metric), 2))

            for metric, values in efficiency_metrics.items():
                if values and values[0] is not None:  # only append if the list is not empty and the first value is not None
                    group[metric] = values
            
            result_dict[str(year)] = group

        return result_dict

    def get_player_names(self, year=None):
        player_names = []
        df = self.data_dict['All']
        if year is not None:
            df = df[df['Year'] == year]
            player_names = df['Player'].unique().tolist()
        else:
            player_names = df['Player'].unique().tolist()
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


