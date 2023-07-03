from bs4 import BeautifulSoup
import requests
import json

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

    rows = soup.find_all('tr')

    headers_dict = {
        "passing": ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY'],
        "rushing": ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM'],
        "receiving": ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']
    }

    headers = headers_dict[stat_type]

    all_stats = {}

    for row in rows:
        cells = row.find_all('td')

        if not cells:
            continue

        name = cells[0].text.strip()

        stats = {}
        for idx, cell in enumerate(cells):
            stat_name = headers[idx]
            stats[stat_name] = cell.text.strip()

        all_stats[name] = stats

    # Write the results to a JSON file
    with open(f'{stat_type}_stats.json', 'w') as json_file:
        json.dump(all_stats, json_file)

    return all_stats




