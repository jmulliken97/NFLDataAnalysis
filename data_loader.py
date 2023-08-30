import boto3
import pandas as pd
import json
import os
import concurrent.futures
from dotenv import load_dotenv
import pickle
from cryptography.fernet import Fernet, InvalidToken

load_dotenv()

class DataLoader:
    def __init__(self, bucket_name):
        self.s3_resource = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.data_dict = {}
        self.cache_dir = os.path.join(os.path.expanduser("~"), ".my_app_data")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, "data_cache.pkl")
        self.stats_file_mapping = {
            'Passing': 'passing_stats_all_years.json',
            'Rushing': 'rushing_stats_all_years.json',
            'Receiving': 'receiving_stats_all_years.json',
            'Defense': 'defense_stats_all_years.json',
            'Kicking': 'kicking_stats_all_years.json'
        }
        key_file = os.path.join(self.cache_dir, "encryption_key.key")
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.key)
        self.cipher_suite = Fernet(self.key)
        self.preload_data()

    def preload_data(self):
        try:
            with open(self.cache_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                self.data_dict = pickle.loads(decrypted_data)
                return
        except (FileNotFoundError, pickle.UnpicklingError, ValueError, InvalidToken):
            print("Failed to decrypt data from cache. Loading from S3.")
            pass
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._load_data_from_s3, stats_type): stats_type for stats_type in self.stats_file_mapping.keys()}
            for future in concurrent.futures.as_completed(futures):
                stats_type = futures[future]
                try:
                    self.data_dict[stats_type] = future.result()
                except Exception as exc:
                    print(f"{stats_type} generated an exception: {exc}")

        self._cache_data()
            
    def _cache_data(self):
        serialized_data = pickle.dumps(self.data_dict)
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        with open(self.cache_file, 'wb') as f:
            f.write(encrypted_data)

    def get_data(self):
        return self.data_dict

    def _load_data_from_s3(self, stats_type):
        data_for_stat = {}
        
        file_pattern = self.stats_file_mapping.get(stats_type, '')
        if not file_pattern:
            raise ValueError(f"Unknown stats type: {stats_type}")

        bucket = self.s3_resource.Bucket(self.bucket_name)
        for obj in bucket.objects.filter(Prefix=file_pattern):
            if obj.key == file_pattern:
                s3_file_content = obj.get()['Body'].read().decode('utf-8')
                data = json.loads(s3_file_content)
                for year, year_data in data.items():
                    df = pd.DataFrame.from_records(year_data)
                    data_for_stat[year] = df
                break
        return data_for_stat




