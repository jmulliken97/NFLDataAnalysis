import requests
from bs4 import BeautifulSoup
import json
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "statsbucketpython" 
S3_KEY = "rosters.json"

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

ROSTER_URL = "https://www.ourlads.com/nfldepthcharts/roster/{team_code}"
DEPTH_CHART_URL = "https://www.ourlads.com/nfldepthcharts/depthchart/{team_code}"
OUTPUT_FILE = "rosters.json"

TEAM_CODES = [
    "ARZ", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", "HOU", "IND", 
    "JAX", "KC", "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SEA", 
    "SF", "TB", "TEN", "WAS"
]

def fetch_roster_data(team_code):
    response = requests.get(ROSTER_URL.format(team_code=team_code))
    soup = BeautifulSoup(response.content, 'html.parser')
    
    players = []
    player_data = soup.find_all("tr")[1:]  # Skip the header row

    for player in player_data:
        columns = player.find_all("td")
        if len(columns) < 9:  # Skip rows that don't have enough data
            continue
        player_info = {
            "Number": columns[0].text.strip(),
            "Name": columns[1].text.strip(),
            "Position": columns[2].text.strip(),
            "DOB": columns[3].text.strip(),
            "Age": columns[4].text.strip(),
            "Height": columns[5].text.strip(),
            "Weight": columns[6].text.strip(),
            "School": columns[7].text.strip(),
            "Orig. Team": columns[8].text.strip(),
            "Draft Status": columns[9].text.strip(),
            "NFL Exp.": columns[10].text.strip()
        }
        players.append(player_info)

    return players

def fetch_depth_chart_data(team_code):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    response = requests.get(DEPTH_CHART_URL.format(team_code=team_code), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Fetching the table by its class
    depth_chart_table = soup.find('table', class_='table table-bordered')

    # Fetching body row data and storing it as a list of dictionaries
    data = {}
    body_rows = depth_chart_table.tbody.find_all('tr')
    for body_row in body_rows:
        columns = [column.text.strip() for column in body_row.find_all('td')]
        position = columns[0]
        for idx, player in enumerate(columns[2::2], start=1):  # Start from Player 1 and jump every 2 columns
            if player:  # If player name exists
                player_name = player.split(' ')[0]  # Use only first name for simplicity
                data[player_name] = position + str(idx)

    return data

def load_roster():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=S3_KEY)
        existing_data = json.loads(response['Body'].read().decode('utf-8'))
        return existing_data
    except:
        return {}

def update_all_teams():
    all_teams_data = {}
    for team_code in TEAM_CODES:
        print(f"Fetching data for {team_code}...")
        roster_data = fetch_roster_data(team_code)
        depth_chart_data = fetch_depth_chart_data(team_code)

        # Merging depth chart data into roster data
        for player in roster_data:
            player_name = player["Name"].split(' ')[0]  # Use only first name for simplicity
            if player_name in depth_chart_data:
                player["PositionTag"] = depth_chart_data[player_name]

        all_teams_data[team_code] = roster_data

    existing_data = load_roster()

    if existing_data != all_teams_data:
        print("Data has changed. Updating S3 bucket...")
        s3.put_object(Body=json.dumps(all_teams_data, indent=4), Bucket=BUCKET_NAME, Key=S3_KEY)
        print(f"Roster data for all teams has been updated in the S3 bucket.")
    else:
        print("No changes detected. Data remains unchanged in the S3 bucket.")

if __name__ == "__main__":
    update_all_teams()

