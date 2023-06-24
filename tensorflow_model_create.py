import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
from keras.callbacks import TensorBoard
from tensorflow import keras
import tensorflow as tf

# Read data from csv file
df = pd.read_csv('data/trainingdata/btc_trainingdata_5.csv')

# Pandas dataframe to Numpy arrays
X = df[['price', 'rsi', 'upper_bb', 'lower_bb']].to_numpy()
y = df[['gain_loss']].to_numpy()

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define Tensorboard callback
log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

# Build and compile model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.007), loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=80, batch_size=32, validation_data=(X_val, y_val), callbacks=[tensorboard_callback])

# Save model
model.save('models/btc1-3.h5')