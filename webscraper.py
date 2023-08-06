from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time
import concurrent.futures

def clean_lg_field(lg):
    if isinstance(lg, str) and 't' in lg:
        return int(lg.replace('t', '')), True
    else:
        return lg, False
    
def clean_player_name(player):
    full_name = player['Player']
    split_name = full_name.split('\u00a0')  # Split the name by the non-breaking space character
    first_name = split_name[0].split(' ')[0]  # Get the first name
    # Check if split_name has more than one element
    if len(split_name) > 1:
        last_name = split_name[1]  # Get the last name
    else:
        last_name = first_name[0]
    clean_name = f'{first_name[0]}. {last_name}'  # Reassemble the name in the desired format
    player['Player'] = clean_name
    return player

def scrape_year(stat_type, max_players, year):
    headers_dict = {
        "passing": ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%T%', 'Int', 'Int%I%', 'Lg', 'Sack', 'Loss', 'Rate'],
        "rushing": ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM'],
        "receiving": ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM'],
        "defense": ['Player', 'Team', 'Gms', 'Int', 'Yds', 'Avg', 'Lg', 'TD', 'Solo', 'Ast', 'Tot', 'Sack', 'YdsL'], 
        "kicking": ['Player', 'Team', 'Gms', 'PAT', 'FG', '0-19', '20-29', '30-39', '40-49', '50+', 'Lg', 'Pts']
    }

    headers = headers_dict[stat_type]
    all_stats = {}
    new_stats = {}
    player_count = 0

    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    current_url = f"https://www.footballdb.com/statistics/nfl/player-stats/{stat_type}/{year}/regular-season"

    while player_count < max_players:
        response = requests.get(current_url, headers=request_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all('table')[0] 
        df = pd.read_html(str(table))[0]
        
        if stat_type == 'defense':
            # Drop the top level of the MultiIndex for defense stats
            df.columns = df.columns.droplevel(0)

        if stat_type == 'passing':
            df.columns = df.columns.str.replace('Int%I%', 'Int%')
            df.columns = df.columns.str.replace('TD%T%', 'TD%')

        headers = df.columns.tolist()

        for _, row in df.iterrows():
            name = row['Player']

            stats = {}
            for idx, stat_name in enumerate(headers):
                stat_value = row[stat_name]

                # Try to convert the stat value to a float
                try:
                    stat_value = float(stat_value)
                except ValueError:
                    pass  # If it can't be converted to a float, leave it as a string

                if stat_name == 'Lg':
                    stat_value, lg_td = clean_lg_field(stat_value)
                    stats['Lg TD'] = lg_td

                stats[stat_name] = stat_value

            stats = clean_player_name(stats)
            new_stats[name] = stats  # Store the new data in new_stats
            player_count += 1

            if player_count >= max_players:
                break

        if player_count >= max_players:
            break  # We have reached the required number of players

        time.sleep(1)  # Wait for 1 second before the next request

    return {year: new_stats}

def scrape_all(stat_type, max_players, start_year, end_year):
    all_stats = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the function to the years, then collect the results
        results = executor.map(scrape_year, [stat_type]*len(range(start_year, end_year + 1)), 
                               [max_players]*len(range(start_year, end_year + 1)), 
                               range(start_year, end_year + 1))
        
    for result in results:
        all_stats.update(result)

    # Write the collected data to a single JSON file
    with open(f'{stat_type}_stats_all_years.json', 'w') as json_file:
        json.dump(all_stats, json_file)

    return all_stats