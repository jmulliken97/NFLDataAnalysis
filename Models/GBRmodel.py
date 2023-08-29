import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_json("E:/Bootcamp/NFLDataAnalysis/Models/enriched_qb_receivers_with_sos_approximated.json", orient="records")

# Load the Outliers data from the Excel sheet
xls = pd.ExcelFile("E:/Bootcamp/NFLDataAnalysis/Models/Passing Info.xlsx")
outliers_data = xls.parse('Outliers')

# Define features and target
features = ['Gms', 'Cmp', 'Att', 'QB_TD', 'Int', 'CompletionPercentage', 
            'YardsPerAttempt', 'TouchdownPercentage', 'InterceptionPercentage', 
            'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec', 'SOS']

# Add interaction term
df['Att_Pct_Interaction'] = df['Att'] * df['CompletionPercentage']
features.append('Att_Pct_Interaction')

# Add binary indicator for outliers
outliers_dict = set(outliers_data['Unnamed: 0'].dropna().values)
df['is_outlier'] = df['Player'].apply(lambda x: 1 if x in outliers_dict else 0)
features.append('is_outlier')

# Normalize the features
scaler = StandardScaler()
X = df[features]
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Handle NaN values by imputation
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_scaled)
X_imputed_df = pd.DataFrame(X_imputed, columns=X_scaled.columns)

# Split the dataset
y = df['QB_Yds']
X_train, X_val, y_train, y_val = train_test_split(X_imputed_df, y, test_size=0.2, random_state=42)

# Initialize and train the Gradient Boosting Regressor
model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, max_depth=5, 
                                  min_samples_split=2, min_samples_leaf=2, random_state=42)
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_val)

# Calculate and print the Mean Squared Error
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error: {mse}")

param_grid = {
    'n_estimators': [100, 150, 200],
    'learning_rate': [0.05, 0.1, 0.15],
    'max_depth': [3, 4, 5, 6],
    'min_samples_split': [2, 3, 4],
    'min_samples_leaf': [1, 2, 3]
}

# Initialize the Grid Search
grid_search = GridSearchCV(GradientBoostingRegressor(random_state=42), param_grid, 
                           cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=1)

# Fit the model
grid_search.fit(X_train, y_train)

# Get the best parameters from the grid search
best_params = grid_search.best_params_

# Initialize and train the Gradient Boosting Regressor with the best parameters
best_model = GradientBoostingRegressor(**best_params, random_state=42)
best_model.fit(X_train, y_train)

# Predict on the validation set
y_pred = best_model.predict(X_val)

# Calculate and print the Mean Squared Error with Best Parameters
mse_best = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error with Best Parameters: {mse_best}")



