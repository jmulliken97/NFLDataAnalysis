import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


data_path = "combined_training_data.csv" 
data = pd.read_csv(data_path)


features_combined = ['cum_avg_pts', 'cum_avg_yds', 'cum_avg_tov', 'cum_avg_pts_opp', 'cum_avg_yds_opp', 'cum_avg_tov_opp']
X = data[features_combined]
y = data['win']

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X, y)


cross_val_accuracy = cross_val_score(logreg, X, y, cv=5, scoring='accuracy').mean()
print(f"Cross-validation accuracy: {cross_val_accuracy:.2f}")

