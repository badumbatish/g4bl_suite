import tensorflow as tf
import numpy as np

# define the training data
# the first column represents the number of attempts to guess the word
# the second column represents whether the word was present or not (0 = absent, 1 = present)
training_data = np.array([[5, 1],
                          [4, 1],
                          [3, 0],
                          [7, 0],
                          [6, 1],
                          [2, 1],
                          [1, 0],
                          [8, 0],
                          [9, 0],
                          [10, 1]])

# separate the input features and target labels
X = training_data[:, 0].reshape(-1, 1)
y = training_data[:, 1].reshape(-1, 1)

# define the neural network architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# train the model
model.fit(X, y, epochs=100)

# use the model to make predictions
test_data = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
predictions = model.predict(test_data)

# print the predictions
for i in range(len(test_data)):
    print(f"Number of attempts: {test_data[i][0]}, Probability of word being present: {predictions[i][0]}")
