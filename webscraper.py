import sqlite3
from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time
import concurrent.futures

headers_dict = {
        "passing": ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%T%', 'Int', 'Int%I%', 'Lg', 'Sack', 'Loss', 'Rate'],
        "rushing": ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM'],
        "receiving": ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'TD', 'Lg', '1st', '1st%', '20+', '40+', 'FUM'],
        "defense": ['Player', 'Team', 'Gms', 'Int', 'Yds', 'Avg', 'Lg', 'TD', 'Solo', 'Ast', 'Tot', 'Sack', 'YdsL'], 
        "kicking": ['Player', 'Team', 'Gms', 'PAT', 'FG', '0-19', '20-29', '30-39', '40-49', '50+', 'Lg', 'Pts']
    }

def clean_lg_field(lg):
    if isinstance(lg, str) and 't' in lg:
        return int(lg.replace('t', '')), True
    else:
        return lg, False
    
def clean_player_name(player):
    full_name = player['Player']
    split_name = full_name.split('\u00a0') 
    first_name = split_name[0].split(' ')[0] 
    if len(split_name) > 1:
        last_name = split_name[1]  
    else:
        last_name = first_name[0]
    clean_name = f'{first_name[0]}. {last_name}' 
    player['Player'] = clean_name
    return player

def scrape_year(stat_type, max_players, year):
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

def initialize_db():
    conn = sqlite3.connect("stats.db")
    cursor = conn.cursor()
    tables = {
        "passing": '''CREATE TABLE IF NOT EXISTS passing
                      (Year INT, Player TEXT, Team TEXT, Gms INT, Att INT, Cmp INT, Pct REAL, Yds INT,
                       YPA REAL, TD INT, TD_percentage REAL, Int INT, Int_percentage REAL, Lg INT,
                       Sack INT, Loss INT, Rate REAL, Lg_TD BOOLEAN)''',
        "rushing": '''CREATE TABLE IF NOT EXISTS rushing
                      (Year INT, Player TEXT, Team TEXT, Gms INT, Att INT, Yds INT, Avg REAL, TD INT, Lg INT,
                       1st INT, 1st_percentage REAL, 20_plus INT, 40_plus INT, FUM INT)''',
        "receiving": '''CREATE TABLE IF NOT EXISTS receiving
                        (Year INT, Player TEXT, Team TEXT, Gms INT, Rec INT, Yds INT, Avg REAL, TD INT, Lg INT,
                         1st INT, 1st_percentage REAL, 20_plus INT, 40_plus INT, FUM INT)''',
        "defense": '''CREATE TABLE IF NOT EXISTS defense
                      (Year INT, Player TEXT, Team TEXT, Gms INT, Int INT, Yds INT, Avg REAL, Lg INT, TD INT,
                       Solo INT, Ast INT, Tot INT, Sack INT, YdsL INT)''',
        "kicking": '''CREATE TABLE IF NOT EXISTS kicking
                      (Year INT, Player TEXT, Team TEXT, Gms INT, PAT INT, FG INT, 0_to_19 INT, 20_to_29 INT,
                       30_to_39 INT, 40_to_49 INT, 50_plus INT, Lg INT, Pts INT)'''
    }
    
    for table in tables.values():
        cursor.execute(table)
    conn.commit()
    return conn, cursor


def insert_data_to_db(cursor, year, stat_type, data, headers):
    insert_query = f"INSERT INTO {stat_type} (Year, " + ", ".join(headers) + ") VALUES (" + ", ".join(["?"] * (len(headers) + 1)) + ")"
    for player, stats in data.items():
        stats_list = [year, player] + [stats[key] for key in headers]
        cursor.execute(insert_query, stats_list)

def scrape_all(stat_type, max_players, start_year, end_year):
    conn, cursor = initialize_db()  
    all_stats = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scrape_year, [stat_type]*len(range(start_year, end_year + 1)), 
                               [max_players]*len(range(start_year, end_year + 1)), 
                               range(start_year, end_year + 1))
    for result in results:
        year = list(result.keys())[0]
        data = result[year]
        all_stats[year] = data
        
        insert_data_to_db(cursor, year, stat_type, data, headers_dict[stat_type])
        
    conn.commit()
    conn.close()
    return all_stats