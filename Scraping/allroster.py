import requests
from bs4 import BeautifulSoup
import json
import time

years = [i for i in range(1970, 2023)]
all_data = []

def get_teams_for_year(year):
    url = f"https://www.jt-sw.com/football/pro/rosters.nsf/By/Season?OpenDocument&Season={year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ul = soup.find('ul')
    
    if not ul:
        print(f"Unordered list not found for year {year}")
        return []
    
    team_links = ul.find_all('a')
    return [link['href'].split('/')[-1].split('-')[-1] for link in team_links]

for year in years:
    teams = get_teams_for_year(year)

    for team in teams:
        url = f"https://www.jt-sw.com/football/pro/rosters.nsf/Annual/{year}-{team}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        table = soup.find('table', {'cellpadding': '4'})
        
        # If table exists, extract the data
        if table:
            rows = table.find_all('tr')
            
            headers = [header.text for header in rows[0].find_all('th')]
            if not all(x in headers for x in ["Pos", "Player", "Exp", "DOB"]):
                print(f"Expected headers not found in {year}-{team}. Skipping team.")
                continue

            pos_index = headers.index("Pos")
            player_index = headers.index("Player")
            exp_index = headers.index("Exp")
            dob_index = headers.index("DOB")
            
            for row in rows[1:]:  # skipping the header row
                cols = row.find_all('td')
                player_data = {
                    "Year": year,
                    "Team": team.upper(),
                    "Pos": cols[pos_index].text.strip(),
                    "Player": cols[player_index].text.strip(),
                    "Exp": cols[exp_index].text.strip(),
                    "DOB": cols[dob_index].text.strip()
                }
                all_data.append(player_data)
        else:
            print(f"Table not found for URL: {url}")
        
        time.sleep(1)

with open('all_scraped_data.json', 'w') as f:
    json.dump(all_data, f)