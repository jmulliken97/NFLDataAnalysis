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
            'passing': 'passing_stats_all_years.json',
            'rushing': 'rushing_stats_all_years.json',
            'receiving': 'receiving_stats_all_years.json',
            'defense': 'defense_stats_all_years.json',
            'kicking': 'kicking_stats_all_years.json'
        }

    def load_data_from_s3(self, stats_type):
        self.data_dict = {}
        
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
                    self.data_dict[year] = df
                break

        return self.data_dict

    def get_data(self):
        return self.data_dict

