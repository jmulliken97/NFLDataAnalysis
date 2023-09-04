import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

# Load the data
data_path = "./updated_processed_data_historical.csv"
data = pd.read_csv(data_path)

def preprocess_data(data):
    # Handle missing values
    data['Time'].fillna('Unknown', inplace=True)
    
    # Extract the year from the 'Date' column
    data['Year'] = pd.to_datetime(data['Date'], errors='coerce').dt.year
    
    # One-hot encoding for categorical features
    encoded_data = pd.get_dummies(data, columns=['Day', 'Home Team', 'Away Team', 'Time'])
    
    return encoded_data

# Preprocess the data
encoded_data = preprocess_data(data)

# Filtering out the training and testing datasets
# Training data: 1966-2021
train_data = encoded_data[data['Year'] <= 2021]

# Testing/validation data: 2022 season
test_data = encoded_data[data['Year'] == 2022]

# Splitting features and target variables
X_train_class = train_data.drop(columns=['Home Win', 'Away Win', 'Point Differential', 'Date', 'Home Score', 'Away Score'])
y_train_class = train_data['Home Win']

X_train_regress = train_data.drop(columns=['Home Win', 'Away Win', 'Point Differential', 'Date', 'Home Score', 'Away Score'])
y_train_regress = train_data['Point Differential']

# Train the classification model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_class, y_train_class)

# Train the regression model
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train_regress, y_train_regress)

# Save the trained models
joblib.dump(clf, "classification_model.pkl")
joblib.dump(regressor, "regression_model.pkl")

print("Models trained and saved!")

