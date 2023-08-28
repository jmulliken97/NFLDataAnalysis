import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset
file_path = "E:/Bootcamp/NFLDataAnalysis/Models/enriched_data_qb_receivers.json"
df_cleaned = pd.read_json(file_path, orient="records")

# Convert the extended data to a pandas DataFrame
df = pd.DataFrame(df_cleaned)

# Features and target columns
features = ['Gms', 'Cmp', 'Att', 'QB_TD', 'Int', 'CompletionPercentage', 'YardsPerAttempt', 'TouchdownPercentage', 'InterceptionPercentage', 
            'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec']
target = 'QB_Yds'

# Splitting the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

# Calculate MSE
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error: {mse}")

#Mean Squared Error: 2639.982017682442