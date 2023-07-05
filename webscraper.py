from bs4 import BeautifulSoup
import requests
import json
import os

def get_player_stats(url, stat_type, player_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    rows = soup.find_all('tr')

    if not rows:
        print('No rows found.')
        return "No rows found."

    headers_dict = {
        "passing": ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY'],
        "rushing": ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM'],
        "receiving": ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']
    }

    headers = headers_dict[stat_type]

    player_stats = {}

    for row in rows:
        cells = row.find_all('td')

        if not cells or cells[0].text.strip() != player_name:
            continue

        stats = {}
        for idx, cell in enumerate(cells):
            stat_name = headers[idx]
            stats[stat_name] = cell.text.strip()

        player_stats[player_name] = stats
        break

    return player_stats


def scrape_all(url, stat_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract the year from the URL
    year = url.split('/')[7]

    rows = soup.find_all('tr')

    headers_dict = {
        "passing": ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY'],
        "rushing": ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM'],
        "receiving": ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']
    }

    headers = headers_dict[stat_type]

    new_stats = {}

    for row in rows:
        cells = row.find_all('td')

        if not cells:
            continue

        name = cells[0].text.strip()

        stats = {}
        for idx, cell in enumerate(cells):
            stat_name = headers[idx]
            stat_value = cell.text.strip()

            # Try to convert the stat value to a float
            try:
                stat_value = float(stat_value)
            except ValueError:
                pass  # If it can't be converted to a float, leave it as a string

            stats[stat_name] = stat_value

        new_stats[name] = stats

    json_file_path = f'{stat_type}_stats.json'

    all_stats = {}

    # If the JSON file already exists, load its data
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            all_stats = json.load(json_file)

    # Ensure the year exists in the dictionary
    if year not in all_stats:
        all_stats[year] = {}

    all_stats[year].update(new_stats)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_stats, json_file)

    return all_stats


