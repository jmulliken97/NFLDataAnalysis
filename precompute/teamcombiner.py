import json
import pandas as pd
import numpy as np

# Load the data
with open("./updated_schedule_data.json", "r") as file:
    data = json.load(file)

# Combine all year data into a single dataframe
all_games = []
for year, games in data.items():
    for game in games:
        game['year'] = int(year)
        all_games.append(game)
df_games = pd.DataFrame(all_games)

# Load the roster data
with open("./rosters.json", "r") as file:
    rosters = json.load(file)

# Convert roster data to DataFrame and calculate team-level metrics
df_rosters = pd.concat([pd.DataFrame(v) for k, v in rosters.items()], keys=rosters.keys()).reset_index(level=1, drop=True).rename_axis('team').reset_index()
team_metrics = df_rosters.groupby('team').agg({
    'Age': 'mean',
    'Weight': 'mean',
    'NFL Exp.': 'sum'
}).rename(columns={
    'Age': 'avg_age',
    'Weight': 'avg_weight',
    'NFL Exp.': 'total_nfl_experience'
})

# Mapping of full team names to abbreviations
team_mapping = {
    'Arizona Cardinals': 'ARZ',
    'Atlanta Falcons': 'ATL',
    'Baltimore Ravens': 'BAL',
    'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR',
    'Chicago Bears': 'CHI',
    'Cincinnati Bengals': 'CIN',
    'Cleveland Browns': 'CLE',
    'Dallas Cowboys': 'DAL',
    'Denver Broncos': 'DEN',
    'Detroit Lions': 'DET',
    'Green Bay Packers': 'GB',
    'Houston Texans': 'HOU',
    'Indianapolis Colts': 'IND',
    'Jacksonville Jaguars': 'JAX',
    'Kansas City Chiefs': 'KC',
    'Las Vegas Raiders': 'LV',
    'Los Angeles Chargers': 'LAC',
    'Los Angeles Rams': 'LAR',
    'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN',
    'New England Patriots': 'NE',
    'New Orleans Saints': 'NO',
    'New York Giants': 'NYG',
    'New York Jets': 'NYJ',
    'Philadelphia Eagles': 'PHI',
    'Pittsburgh Steelers': 'PIT',
    'San Francisco 49ers': 'SF',
    'Seattle Seahawks': 'SEA',
    'Tampa Bay Buccaneers': 'TB',
    'Tennessee Titans': 'TEN',
    'Washington Commanders': 'WAS',
    'Washington Football Team': 'WAS',  # Handling the name change
    'Washington Redskins': 'WAS'  # Handling the old name
}

# Adjust team names in the game data to match abbreviations
df_games['home_team'] = df_games['home_team'].map(team_mapping).fillna(df_games['home_team'])
df_games['away_team'] = df_games['away_team'].map(team_mapping).fillna(df_games['away_team'])

# Randomly assign home and away teams
mask = np.random.rand(len(df_games)) < 0.5
df_games['home_team'] = np.where(mask, df_games['winner_tie'], df_games['loser_tie'])
df_games['away_team'] = np.where(mask, df_games['loser_tie'], df_games['winner_tie'])

# Correct the home_win column
df_games['home_win'] = (df_games['home_team'] == df_games['winner_tie']).astype(int)

# Merge team metrics with the game data
df_merged = df_games.merge(team_metrics, left_on='home_team', right_index=True, suffixes=('', '_home'))
df_merged = df_merged.merge(team_metrics, left_on='away_team', right_index=True, suffixes=('', '_away'))

# Save the adjusted data to a new JSON file
df_merged.to_json("./train.json", orient="records")

