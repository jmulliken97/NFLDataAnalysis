import boto3
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

class DataLoader:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.data_dict = {}
        self.stats_file_mapping = {
            'Passing': 'passing_stats_all_years.json',
            'Rushing': 'rushing_stats_all_years.json',
            'Receiving': 'receiving_stats_all_years.json',
            'Defense': 'defense_stats_all_years.json',
            'Kicking': 'kicking_stats_all_years.json'
        }
        self.preload_data()

    def preload_data(self):
        for stats_type in self.stats_file_mapping.keys():
            self.data_dict[stats_type] = self._load_data_from_s3(stats_type)
    
    def get_data(self):
        return self.data_dict

    def _load_data_from_s3(self, stats_type):
        data_for_stat = {}
        
        file_pattern = self.stats_file_mapping.get(stats_type, '')
        if not file_pattern:
            raise ValueError(f"Unknown stats type: {stats_type}")
        
        files = self.s3_client.list_objects(Bucket=self.bucket_name)['Contents']
        
        for file in files:
            object_key = file['Key']
            if object_key == file_pattern:
                # Fetch file content
                s3_file_content = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)['Body'].read().decode('utf-8')
                data = json.loads(s3_file_content)
                
                for year, year_data in data.items():
                    df = pd.DataFrame.from_records(year_data)
                    data_for_stat[year] = df
                break

        return data_for_stat


