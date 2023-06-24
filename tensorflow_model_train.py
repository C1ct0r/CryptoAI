import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
from keras.callbacks import TensorBoard
import tensorflow as tf

# Read data from csv file
df = pd.read_csv('data/trainingdata/btc_trainingdata_4.csv')

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

# Load model to continue training
model = tf.keras.models.load_model('models/btc1-2.h5')

# Train model
history = model.fit(X_train, y_train, epochs=2, batch_size=32, validation_data=(X_val, y_val), callbacks=[tensorboard_callback])

# Save model
model.save('models/btc1-3.h5')