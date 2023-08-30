from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_data(data):
    try:
        return float(data)
    except ValueError:
        return data  

def scrape_year_data(year_url, request_headers):
    response = requests.get(year_url, headers=request_headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'statistics'})
    df = pd.read_html(str(table))[0]

    # Flatten multi-level column headers if they exist
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df = df.rename(columns={"Unnamed: 0_level_0 Team": "Team"})

    for column in df.columns:
        df[column] = df[column].apply(clean_data)
    
    return df.to_dict(orient='records')

def scrape_year(year, base_url, request_headers):
    year_url = base_url + '?yr=' + year
    year_data = scrape_year_data(year_url, request_headers)
    time.sleep(1)  # Wait for 1 second before the next request
    return year, year_data

def scrape_all(start_year, end_year):
    all_data = {}
    
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    base_url = 'https://www.footballdb.com/stats/penalties.html'
    response = requests.get(base_url, headers=request_headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    year_menu = soup.find('select', {'name': 'yr'})
    year_options = [option['value'] for option in year_menu.find_all('option')]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scrape_year, year, base_url, request_headers): year for year in year_options if start_year <= int(year) <= end_year}
        for future in as_completed(futures):
            year = futures[future]
            try:
                all_data[year] = future.result()[1]
            except Exception as exc:
                print(f'An exception occurred for year {year}: {exc}')
    
    with open('penalties_data.json', 'w') as json_file:
        json.dump(all_data, json_file)
    
    return all_data

