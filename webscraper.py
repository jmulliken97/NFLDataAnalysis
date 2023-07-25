from bs4 import BeautifulSoup
import requests
import json
import os

def scrape_all(stat_types, max_players, start_year, end_year):
    headers_dict = {
        "passing": ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Cmp', 'Cmp %', 'TD', 'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'SckY'],
        "rushing": ['Player', 'Rush Yds', 'Att', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM'],
        "receiving": ['Player', 'Rec', 'Yds', 'TD', '20+', '40+', 'LNG', 'Rec 1st', '1st%', 'Rec FUM', 'Rec YAC/R', 'Tgts']
    }

    base_url = "https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all"

    for stat_type in stat_types:
        headers = headers_dict[stat_type]
        all_stats = {}
        json_file_path = f'{stat_type}_stats.json'

        # If the JSON file already exists, load its data
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                all_stats = json.load(json_file)

        for year in range(start_year, end_year+1):
            player_count = 0
            current_url = base_url.replace("passing", stat_type).replace("2023", str(year))

            while player_count < max_players:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.text, 'lxml')

                rows = soup.find_all('tr')

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
                    player_count += 1

                    if player_count >= max_players:
                        break

                if player_count >= max_players:
                    break  

                # Get the 'Next Page' link
                next_link = soup.find('a', class_='nfl-o-table-pagination__next')
                if next_link is None:
                    break  

                # Construct the full URL for the next page
                current_url = base_url + next_link['href']

            # Ensure the year exists in the dictionary
            if str(year) not in all_stats:
                all_stats[str(year)] = {}

            all_stats[str(year)].update(new_stats)  # Update the data for the current year with the new data

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(all_stats, json_file)

    return all_stats

