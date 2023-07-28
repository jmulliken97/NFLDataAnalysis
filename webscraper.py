from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

def scrape_all(stat_type, max_players, start_year, end_year):
    headers_dict = {
        "passing": ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%T%', 'Int', 'Int%I%', 'Lg', 'Sack', 'Loss', 'Rate'],
        "rushing": ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM'],
        "receiving": ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM']
    }

    headers = headers_dict[stat_type]
    all_stats = {}
    
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for year in range(start_year, end_year + 1):
        new_stats = {}
        player_count = 0
        current_url = f"https://www.footballdb.com/statistics/nfl/player-stats/{stat_type}/{year}/regular-season"

        while player_count < max_players:
            response = requests.get(current_url, headers=request_headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find_all('table')[0] 
            df = pd.read_html(str(table))[0]

            # Clean column names
            df.columns = df.columns.str.replace('Int%I%', 'Int%')
            df.columns = df.columns.str.replace('TD%T%', 'TD%')

            # Update headers to match cleaned column names
            headers = df.columns.tolist()

            for _, row in df.iterrows():
                name = row['Player']
                name = name.split('\u00a0')[0]  # Clean player name

                stats = {}
                for idx, stat_name in enumerate(headers):
                    stat_value = row[stat_name]

                    # Try to convert the stat value to a float
                    try:
                        stat_value = float(stat_value)
                    except ValueError:
                        pass  # If it can't be converted to a float, leave it as a string

                    stats[stat_name] = stat_value

                new_stats[name] = stats  # Store the new data in new_stats
                player_count += 1

                if player_count >= max_players:
                    break

            if player_count >= max_players:
                break  # We have reached the required number of players

            time.sleep(1)  # Wait for 1 second before the next request

        json_file_path = f'{stat_type}_stats.json'

        # If the JSON file already exists, load its data
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                all_stats = json.load(json_file)

        # Ensure the year exists in the dictionary
        if year not in all_stats:
            all_stats[year] = {}

        all_stats[year].update(new_stats)  # Update the data for the current year with the new data

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(all_stats, json_file)

    return all_stats
