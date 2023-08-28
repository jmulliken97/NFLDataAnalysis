import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import tensorflow as tf

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

# Defining the Neural Network
model_nn = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compiling the model
model_nn.compile(optimizer='adam', loss='mean_squared_error')

# Training the model
model_nn.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=1)

# Predicting on the validation set
y_pred_nn = model_nn.predict(X_val_scaled).flatten()

# Calculating the Mean Squared Error
mse_nn = mean_squared_error(y_val, y_pred_nn)
print(f"Mean Squared Error for Neural Network: {mse_nn}")

#Mean Squared Error for Neural Network: 19083.92693079007