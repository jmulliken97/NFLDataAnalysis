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

    def load_data_from_s3(self):
    # List all files in the bucket
        files = self.s3_client.list_objects(Bucket=self.bucket_name)['Contents']
        
        for file in files:
            object_key = file['Key']
            if object_key.endswith('.json'):
                # Fetch file content
                s3_file_content = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)['Body'].read().decode('utf-8')
                data = json.loads(s3_file_content)
                
                for year, year_data in data.items():
                    df = pd.DataFrame.from_records(year_data)
                    self.data_dict[year] = df

        return self.data_dict

    def get_data(self):
        return self.data_dict
