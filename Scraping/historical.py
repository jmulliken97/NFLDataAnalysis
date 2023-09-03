import requests
import json
import time
from bs4 import BeautifulSoup

# Define the years that returned
years = [
    2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
]

try:
    with open('historical_data.json', 'r') as json_file:
        all_years_data = json.load(json_file)
except FileNotFoundError:
    all_years_data = {}

for year in years:
    url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'games'})

        if not table:
            print(f"Unable to find data for the year {year}.")
            continue

        year_data = []

        rows = table.findAll('tr')
        for row in rows:
            columns = row.findAll('td')
            data = [col.text for col in columns]
            year_data.append(data)

        all_years_data[year] = year_data

    except requests.RequestException as e:
        print(f"Error fetching data for the year {year}. Error: {e}")

    time.sleep(1)

with open('historical_data.json', 'w') as json_file:
    json.dump(all_years_data, json_file)




