import pandas as pd
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from scipy.stats import uniform, randint

# Load the dataset
df = pd.read_json("./enriched_data_with_age_exp.json", orient="records")

# Convert "R" to 0 in the 'Exp' column
df['Exp'] = df['Exp'].replace("R", 0).astype(float)

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
df_sorted = df.sort_values(by=['Player', 'Year'])

lag_columns = ['Gms', 'Cmp', 'Att', 'QB_Yds', 'QB_TD', 'Int', 'Rate', 
               'CompletionPercentage', 'YardsPerAttempt', 'TouchdownPercentage', 
               'InterceptionPercentage', 'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec', 
               'Age', 'Exp']

for col in lag_columns:
    df_sorted[f"{col}_prev_year"] = df_sorted.groupby('Player')[col].shift(1)
    df_sorted[f"{col}_diff"] = df_sorted[col] - df_sorted[f"{col}_prev_year"]

# Define the new set of features
selected_features = [
    'Year', 'Gms', 'Cmp', 'Att', 'QB_Yds', 'QB_TD', 'Int', 'Rate', 
    'CompletionPercentage', 'YardsPerAttempt', 'TouchdownPercentage', 
    'InterceptionPercentage', 'Rec', 'Receiver_Yds', 'Receiver_TD', 'AvgYdsPerRec', 'SOS', 
    'Age', 'Exp'
]

for col in lag_columns:
    selected_features.extend([f"{col}_prev_year", f"{col}_diff"])

X_new = df_sorted[selected_features]
y_new = df_sorted['QB_Yds']

# Handle missing values and scale the features
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_new)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Hyperparameter tuning and training
param_distributions = {
    'n_estimators': randint(50, 250),
    'learning_rate': uniform(0.01, 0.2),
    'max_depth': randint(3, 7),
    'min_samples_split': randint(2, 5),
    'min_samples_leaf': randint(1, 5),
    'subsample': uniform(0.6, 0.4),
    'max_features': ['sqrt', 'log2', None]
}

kf = KFold(n_splits=5, shuffle=True, random_state=42)
random_search = RandomizedSearchCV(GradientBoostingRegressor(n_iter_no_change=10, validation_fraction=0.1, random_state=42),
                                   param_distributions=param_distributions, 
                                   n_iter=100, scoring='neg_mean_squared_error', 
                                   n_jobs=-1, cv=kf, verbose=1, random_state=42)

random_search.fit(X_scaled, y_new)

best_params = random_search.best_params_
best_model = GradientBoostingRegressor(**best_params, n_iter_no_change=10, validation_fraction=0.1, random_state=42)
best_model.fit(X_scaled, y_new)

y_pred = best_model.predict(X_scaled)
mse = mean_squared_error(y_new, y_pred)

print(f"Mean Squared Error with Best Parameters: {mse}")

