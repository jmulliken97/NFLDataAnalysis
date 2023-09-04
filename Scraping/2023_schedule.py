import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.pro-football-reference.com/years/2023/games.htm"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find("table", {"id": "games"})

rows = table.find_all("tr")
data = []
for row in rows:
    cols = row.find_all(["td", "th"])
    cols = [ele.text.strip() for ele in cols]
    if cols[0] and (cols[0].isdigit() or cols[0] == 'Week'):
        data.append(cols)

df = pd.DataFrame(data[1:], columns=data[0])
df = df[df['Week'].str.isnumeric()]
df = df[df['Week'].astype(int) >= 1]

df.columns = pd.io.parsers.ParserBase({'names':df.columns})._maybe_dedup_names(df.columns)

# Convert the dataframe to a JSON string
json_data = df.to_json(orient="records", date_format="iso")

# Print the JSON string
print(json_data)

# If you want to save the JSON data to a file
with open("nfl_schedule_2023.json", "w") as json_file:
    json_file.write(json_data)