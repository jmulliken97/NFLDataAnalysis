import requests
from bs4 import BeautifulSoup
import json
import time

# List of years and team abbreviations
years = [i for i in range(1970, 2023)]
teams = ["ari", "atl", "bal", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gb", "hou", "ind", 
         "jax", "kc", "lac", "lar", "lv", "mia", "min", "ne", "no", "nyg", "nyj", "phi", "pit", "sea", 
         "sf", "tb", "ten", "was"]

all_data = []

for year in years:
    for team in teams:
        # Construct the URL
        url = f"https://www.jt-sw.com/football/pro/rosters.nsf/Annual/{year}-{team}"
        
        # Fetch the content of the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table
        table = soup.find('table', {'cellpadding': '4'})
        
        # If table exists, extract the data
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # skipping the header row
                cols = row.find_all('td')
                player_data = {
                    "Year": year,
                    "Team": team.upper(),
                    "Pos": cols[0].text.strip(),
                    "Player": cols[2].text.strip(),
                    "Exp": cols[6].text.strip(),
                    "DOB": cols[7].text.strip()
                }
                all_data.append(player_data)
        else:
            print(f"Table not found for URL: {url}")
        
        # Introduce a pause between requests
        time.sleep(1)

# Save the data to a JSON file
with open('all_scraped_data.json', 'w') as f:
    json.dump(all_data, f)

