import pandas as pd
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from scipy.stats import uniform, randint

# Load the dataset
df = pd.read_json("./enriched_qb_receivers_with_sos_approximated.json", orient="records")

# Load the Outliers data from the Excel sheet
xls = pd.ExcelFile("./Passing Info.xlsx")
outliers_data = xls.parse('Outliers')

merged_data = df.merge(outliers_data[['Unnamed: 0', 'Int', 'Rate']], 
                       left_on='Player', right_on='Unnamed: 0', 
                       how='left', suffixes=('', '_y'))

# Calculate differences for 'Int' and 'Rate'
merged_data['Int_diff'] = merged_data['Int_y'] - merged_data['Int']
merged_data['Rate_diff'] = merged_data['Rate_y'] - merged_data['Rate']

# Handle discrepancies: Replace 'Int' values and drop rows with large 'Rate' discrepancies
std_deviation = merged_data['Rate_diff'].std()
replace_entries = merged_data[(merged_data['Rate_diff'].abs() <= std_deviation) & 
                              (~merged_data['Rate_diff'].isna())]['Player']
drop_entries = merged_data[merged_data['Rate_diff'].abs() > std_deviation]['Player']

# Apply the replacements and drop the specified entries
for player in replace_entries:
    df.loc[df['Player'] == player, 'Rate'] = merged_data.loc[merged_data['Player'] == player, 'Rate_y'].values[0]

df = df[~df['Player'].isin(drop_entries)]

# Add interaction term
df['Att_Pct_Interaction'] = df['Att'] * df['CompletionPercentage']

# Define features and target
features = ['Gms', 'Cmp', 'Att', 'QB_TD', 'Int', 'CompletionPercentage', 
            'YardsPerAttempt', 'TouchdownPercentage', 
            'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec', 'SOS', 
            'Att_Pct_Interaction']
X = df[features]
y = df['QB_Yds']

scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Handle NaN values by imputation
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_scaled)
X_imputed_df = pd.DataFrame(X_imputed, columns=X_scaled.columns)

# Parameter distributions for RandomizedSearchCV
param_distributions = {
    'n_estimators': randint(50, 250),
    'learning_rate': uniform(0.01, 0.2),
    'max_depth': randint(3, 7),
    'min_samples_split': randint(2, 5),
    'min_samples_leaf': randint(1, 5),
    'subsample': uniform(0.6, 0.4),
    'max_features': ['sqrt', 'log2', None]
}

# Initialize RandomizedSearchCV with K-Fold CV
kf = KFold(n_splits=5, shuffle=True, random_state=42)
random_search = RandomizedSearchCV(GradientBoostingRegressor(n_iter_no_change=10, validation_fraction=0.1, random_state=42),
                                   param_distributions=param_distributions, 
                                   n_iter=1000, scoring='neg_mean_squared_error', 
                                   n_jobs=-1, cv=kf, verbose=1, random_state=42)

# Fit the model with the data
random_search.fit(X_imputed_df, y)

# Get the best parameters from the random search
best_params = random_search.best_params_

# Initialize and train the Gradient Boosting Regressor with the best parameters
best_model = GradientBoostingRegressor(**best_params, n_iter_no_change=10, validation_fraction=0.1, random_state=42)
best_model.fit(X_imputed_df, y)

# Predict on the entire dataset (optional)
y_pred = best_model.predict(X_imputed_df)

# Calculate and print the Mean Squared Error
mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error with Best Parameters: {mse}")