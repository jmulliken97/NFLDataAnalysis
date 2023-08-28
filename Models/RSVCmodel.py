import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor

# Load the cleaned JSON file into a DataFrame
file_path = "E:/Bootcamp/NFLDataAnalysis/Models/enriched_data_qb_receivers.json"
df_cleaned = pd.read_json(file_path, orient="records")

# Extracting features and target
features = ['Gms', 'Cmp', 'Att', 'QB_TD', 'Int', 'CompletionPercentage', 'YardsPerAttempt', 'TouchdownPercentage', 
            'InterceptionPercentage', 'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec']
target = 'QB_Yds'
X = df_cleaned[features]
y = df_cleaned[target]

# Splitting the data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Parameters to tune for Gradient Boosting Regressor
param_grid_gb = {
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5],
    'min_samples_split': [2, 4, 6],
    'min_samples_leaf': [1, 2, 4]
}

# Setting up RandomizedSearchCV
n_iter_search = 50  # Number of parameter settings that are sampled
gb_random_search = RandomizedSearchCV(GradientBoostingRegressor(random_state=42), param_distributions=param_grid_gb, 
                                     n_iter=n_iter_search, scoring='neg_mean_squared_error', cv=3, verbose=1, n_jobs=-1, random_state=42)

# Performing the random search
gb_random_search.fit(X_train_scaled, y_train)

# Getting the best parameters and score from the search
best_params_gb_random = gb_random_search.best_params_
best_score_gb_random = -gb_random_search.best_score_

print(f"Best Parameters: {best_params_gb_random}")
print(f"Best MSE Score: {best_score_gb_random}")

#Best MSE Score: 4682.969193851182
