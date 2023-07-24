from bs4 import BeautifulSoup
import requests
import json
import os

def scrape_all(url, stat_type, max_players):
    # Extract the year from the URL
    year = url.split('/')[7]

    headers_dict = {
        "passing": ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY'],
        "rushing": ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM'],
        "receiving": ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']
    }

    headers = headers_dict[stat_type]

    new_stats = {}
    player_count = 0
    base_url = "https://www.nfl.com"
    current_url = url

    while player_count < max_players:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'lxml')

        rows = soup.find_all('tr')

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

            new_stats[name] = stats  # Store the new data in new_stats
            player_count += 1

            if player_count >= max_players:
                break

        if player_count >= max_players:
            break  # We have reached the required number of players

        # Get the 'Next Page' link
        next_link = soup.find('a', class_='nfl-o-table-pagination__next')
        if next_link is None:
            break  # No more pages

        # Construct the full URL for the next page
        current_url = base_url + next_link['href']

    json_file_path = f'{stat_type}_stats.json'

    all_stats = {}

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
