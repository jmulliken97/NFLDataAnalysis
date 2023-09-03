import pytest
from unittest.mock import patch, Mock
import pandas as pd
from ..data_processor import DataProcessor


# Mock the DataLoader class
class MockDataLoader:
    def __init__(self, bucket_name):
        pass

    def get_data(self):
        return {
            "passing": {
                "2021": pd.DataFrame({
                    "Player": ["John Doe"],
                    "Team": ["Team A"],
                    "Gms": [10],
                    "Att": [100],
                    "Cmp": [60],
                    "Pct": [60.0],
                    "Yds": [1000],
                    "YPA": [10.0],
                    "TD": [5],
                    "TD%": [5.0],
                    "T%": [5.0],
                    "Int": [2],
                    "Int%": [2.0],
                    "I%": [2.0],
                    "Lg": [50],
                    "Sack": [5],
                    "Loss": [30],
                    "Rate": [90.0]
                })
            }
        }

# Mock the QtWidgets.QFileDialog.getOpenFileName method
mock_get_open_file_name = Mock(return_value=("mock_bucket.json", "JSON Files (*.json)"))

@pytest.fixture
def data_processor():
    with patch("your_module.DataLoader", MockDataLoader), patch("your_module.QtWidgets.QFileDialog.getOpenFileName", mock_get_open_file_name):
        return DataProcessor()

def test_load_and_process_data(data_processor):
    preloaded_data = {
        "passing": {
            "2021": pd.DataFrame({
                "Player": ["John Doe"],
                "Team": ["Team A"],
                "Gms": [10],
                "Att": [100],
                "Cmp": [60],
                "Pct": [60.0],
                "Yds": [1000],
                "YPA": [10.0],
                "TD": [5],
                "TD%": [5.0],
                "T%": [5.0],
                "Int": [2],
                "Int%": [2.0],
                "I%": [2.0],
                "Lg": [50],
                "Sack": [5],
                "Loss": [30],
                "Rate": [90.0]
            })
        }
    }
    years = data_processor.load_and_process_data(preloaded_data, "passing")
    assert years == ["2021"]

def test_process_data(data_processor):
    data = {
        "Player": ["John Doe", "Jane Smith"],
        "Team": ["Team A", "Team B"],
        "Gms": ["10", "12"],
        "Att": ["100", "110"],
        "Cmp": ["60", "65"],
        "Pct": ["60.0", "59.1"],
        "Yds": ["1000", "1100"],
        "YPA": ["10.0", "10.1"],
        "TD": ["5", "6"]
    }
    df = pd.DataFrame(data)
    processed_df = data_processor.process_data(df)
    assert processed_df.shape == (2, 9)
    assert processed_df["Gms"].dtype == "float64"

def test_get_player_names(data_processor):
    data_processor.data_dict = {
        "All": pd.DataFrame({
            "Player": ["John Doe", "Jane Smith"],
            "Year": [2021, 2021]
        })
    }
    players = data_processor.get_player_names()
    assert set(players) == {"John Doe", "Jane Smith"}

def test_get_columns(data_processor):
    data_processor.data_dict = {
        "2021": pd.DataFrame({
            "Player": ["John Doe"],
            "Team": ["Team A"],
            "Gms": [10]
        })
    }
    columns = data_processor.get_columns("2021")
    assert set(columns) == {"Player", "Team", "Gms"}

def test_correlation_analysis(data_processor):
    data_processor.data_dict = {
        "2021": pd.DataFrame({
            "Gms": [10, 12],
            "Att": [100, 110],
            "Cmp": [60, 65]
        })
    }
    correlation_matrix = data_processor.correlation_analysis("2021")
    assert not correlation_matrix.empty

def test_descriptive_stats(data_processor):
    data_processor.data_dict = {
        "2021": pd.DataFrame({
            "Gms": [10, 12],
            "Att": [100, 110],
            "Cmp": [60, 65]
        })
    }
    stats = data_processor.descriptive_stats("2021")
    assert not stats.empty

def test_distribution(data_processor):
    data_processor.data_dict = {
        "2021": pd.DataFrame({
            "Gms": [10, 12],
            "Att": [100, 110],
            "Cmp": [60, 65]
        })
    }
    distribution_data = data_processor.distribution("Gms", "2021")
    assert distribution_data.tolist() == [10, 12]

def test_detect_outliers(data_processor):
    data_processor.data_dict = {
        "2021": pd.DataFrame({
            "Gms": [10, 12, 100],
            "Att": [100, 110, 500],
            "Cmp": [60, 65, 200]
        })
    }
    outliers_df = data_processor.detect_outliers("2021")
    assert not outliers_df.empty
