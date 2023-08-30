import boto3
import json

# Constants
BUCKET_NAME = "statsbucketpython"
STATS_FILE_MAPPING = {
    'Passing': 'passing_stats_all_years.json',
    'Rushing': 'rushing_stats_all_years.json',
    'Receiving': 'receiving_stats_all_years.json',
    'Defense': 'defense_stats_all_years.json',
    'Kicking': 'kicking_stats_all_years.json'
}

s3_client = boto3.client('s3')

class YourClass:

    STATS_TYPES = [("passing", ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%', 'Int', 'Int%', 'Lg TD', 'Lg', 'Sack', 'Loss', 'Rate']), 
                        ("rushing", ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD']),
                        ("receiving", ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD', 'Tar', 'YAC']),
                        ("defense", ['Player', 'Team', 'Gms', 'Int', 'Yds', 'Avg', 'Lg TD', 'Lg', 'TD', 'Solo', 'Ast', 'Tot', 'Sack', 'YdsL']),
                        ("kicking", ['Player', 'Team', 'Gms', 'PAT', 'FG', '0-19', '20-29', '30-39', '40-49', '50+', 'Lg TD', 'Lg', 'Pts'])]

    @staticmethod
    def calculate_score(player_data):
        player = player_data.copy()

        def determine_stats_type(stats):
            stats_keys = stats.keys()
            stat_types = [
                ("passing", ['Player', 'Team', 'Gms', 'Att', 'Cmp', 'Pct', 'Yds', 'YPA', 'TD', 'TD%', 'Int', 'Int%', 'Lg TD', 'Lg', 'Sack', 'Loss', 'Rate']), 
                ("rushing", ['Player', 'Team', 'Gms', 'Att', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD']),
                ("receiving", ['Player', 'Team', 'Gms', 'Rec', 'Yds', 'Avg', 'YPG', 'Lg TD', 'Lg', 'TD', 'FD', 'Tar', 'YAC']),
                ("defense", ['Player', 'Team', 'Gms', 'Int', 'Yds', 'Avg', 'Lg TD', 'Lg', 'TD', 'Solo', 'Ast', 'Tot', 'Sack', 'YdsL']),
                ("kicking", ['Player', 'Team', 'Gms', 'PAT', 'FG', '0-19', '20-29', '30-39', '40-49', '50+', 'Lg TD', 'Lg', 'Pts'])
            ]

            for stat_type, headers in stat_types:
                if all(item in stats_keys for item in headers):
                    return stat_type
            return "unknown"

        stats_type = determine_stats_type(player_data)
        weights = None

        if stats_type == "passing":
            weights = {
                "Yds": 0.05,
                "YPA": 0.15,
                "Pct": 0.15,
                "TD:INT Ratio": 0.2,
                "Rate": 0.05,
                "Sack": -0.05,
                "Loss": -0.05,
                "ANY/A": 0.2,
            }
            for key in ["Yds", "YPA", "Pct", "TD", "Int", "Rate", "Sack", "Loss", "Att"]:
                if key in player:
                    player[key] = 0.0 if player[key] == '--' else float(player[key])
                                    
            if player.get("Int") != 0:
                player["TD:INT Ratio"] = round(player["TD"] / player["Int"], 2)
            else:
                player["TD:INT Ratio"] = round(player["TD"], 2)

            player["ANY/A"] = round((player["Yds"] + 20 * player["TD"] - 45 * player["Int"] - player["Loss"]) / (player["Att"] + player["Sack"]), 2)

        elif stats_type == "rushing":
            player["Y/A"] = player["Yds"] / player["Att"] if player["Att"] else 0
            player["TD/A"] = player["TD"] / player["Att"] if player["Att"] else 0
            player["TD/G"] = player["TD"] / player["Gms"] if player["Gms"] else 0

            weights = {
                "Yds": 0.15,
                "Att": 0.15,
                "TD": 0.15,
                "Avg": 0.15,
                "YPG": 0.1,
                "Lg": 0.05,
                "Y/A": 0.1,
                "TD/A": 0.1,
                "TD/G": 0.1
            }

        elif stats_type == "receiving":
            player["Y/R"] = player["Yds"] / player["Rec"] if player["Rec"] else 0
            player["TD/R"] = player["TD"] / player["Rec"] if player["Rec"] else 0
            player["Y/Tgt"] = player["Yds"] / player["Tar"] if player["Tar"] else 0
            player["Rec/Tgt"] = player["Rec"] / player["Tar"] if player["Tar"] else 0
            player["TD/G"] = player["TD"] / player["Gms"] if player["Gms"] else 0

            weights = {
                "Rec": 0.1,
                "Yds": 0.1,
                "TD": 0.15,
                "Avg": 0.1,
                "YPG": 0.1,
                "Lg": 0.1,
                "Tar": 0.05,
                "YAC": 0.05,
                "Y/R": 0.05,
                "TD/R": 0.05,
                "Y/Tgt": 0.05,
                "Rec/Tgt": 0.05,
                "TD/G": 0.1
            }

        elif stats_type == "defense":
            weights = {
                "Int": 0.15,
                "Yds": 0.10,
                "Avg": 0.10,
                "Lg TD": 0.10,
                "Lg": 0.05,
                "TD": 0.10,
                "Solo": 0.10,
                "Ast": 0.05,
                "Tot": 0.10,
                "Sack": 0.15,
                "YdsL": 0.10
            }
            for key in ["Gms", "Int", "Yds", "Avg", "TD", "Solo", "Ast", "Tot", "Sack", "YdsL"]:
                if key in player:
                    player[key] = 0.0 if player[key] == '--' else float(player[key])
                        
        elif stats_type == "kicking":
            weights = {
                "PAT": 0.15,
                "FG": 0.25,
                "0-19": 0.05,
                "20-29": 0.05,
                "30-39": 0.05,
                "40-49": 0.05,
                "50+": 0.10,
                "Lg": 0.10,
                "Pts": 0.30
            }
            for key in ["Gms", "Lg", "Pts"]:
                if key in player:
                    player[key] = 0.0 if player[key] == '--' else float(player[key])
            for key in ["PAT", "FG", "0-19", "20-29", "30-39", "40-49", "50+"]:
                if key in player:
                    successes, attempts = map(int, (0 if val == '--' else val for val in player[key].split('/')))
                    player[key] = successes / attempts if attempts != 0 else 0

        if weights is None:
            return None, None, None, {}, "unknown"

        score = 0
        for stat, weight in weights.items():
            if player.get(stat) is not None:
                score += player.get(stat, 0) * weight

        if stats_type == "passing":
            return round(score, 2), player.get("TD:INT Ratio"), player.get("ANY/A"), player, stats_type
        elif stats_type in ["rushing", "receiving", "defense", "kicking"]:
            return round(score, 2), None, None, player, stats_type

    @staticmethod
    def load_data_from_s3(stats_type):
        file_pattern = STATS_FILE_MAPPING.get(stats_type, '')
        s3_file_content = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_pattern)['Body'].read().decode('utf-8')
        return json.loads(s3_file_content)
    
    @staticmethod
    def save_data_to_s3(data, stats_type):
        file_pattern = STATS_FILE_MAPPING.get(stats_type, '')
        s3_client.put_object(Body=json.dumps(data), Bucket=BUCKET_NAME, Key=file_pattern)

    @staticmethod
    def process_data(stats_type):
        data = YourClass.load_data_from_s3(stats_type)
        for year, players_data in data.items():
            for player_name, player_stats in players_data.items():
                score, _, _, _, _ = YourClass.calculate_score(player_stats) 
                player_stats["Score"] = score
            YourClass.save_data_to_s3(data, stats_type)


if __name__ == "__main__":
    for stats_type in STATS_FILE_MAPPING.keys():
        YourClass.process_data(stats_type)