import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np

# Read data from csv file
df = pd.read_csv('data/checkdata/btc_checkdata_1.csv')

# Select 2000 random rows
#df = df.sample(n=2000)

# Pandas dataframe to Numpy arrays
inputs = df[['price', 'rsi', 'upper_bb', 'lower_bb']].to_numpy()
targets = df[['gain_loss']].to_numpy()

# Normalize input
scaler = StandardScaler()
inputs = scaler.fit_transform(inputs)

# Load the model
model = tf.keras.models.load_model('models/btc1-2.h5')

# Make predictions using the model
predictions = model.predict(inputs)

# Make the output readable
predictions_readable = np.where(predictions > 0.5, 1, 0)

# Calculate the accuracy
accuracy = np.mean(predictions_readable == targets)

# Print the result
print(f"The accuracy of the model on the validation set is {accuracy:.2%}.")