import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(data_path='C:/Users/Admin/Desktop/MLOPS_PROJECT_21i-0709_21i-1709_20i-0847/Pipelining/data/WineQT.csv'):
    """Load data for training"""
    data = pd.read_csv(data_path)
    data = data.drop(['Id'], axis=1)
    data = data.drop_duplicates(keep='first')
    data = data.iloc[np.random.permutation(len(data))]
    data['quality'].hist(bins=20)

    return data


def train_model(data, model_path='C:/Users/Admin/Desktop/MLOPS_PROJECT_21i-0709_21i-1709_20i-0847/Pipelining/src/api/model.keras'):
    """Train a simple ML model and save to disk"""
    # Prepare data
    train, test = train_test_split(data, test_size=0.2, random_state=1)
    train.shape, test.shape
    train_stats = train.describe()
    train_stats.pop('quality')
    train_stats = train_stats.transpose()
    train_stats
    x_train = train.drop('quality', axis=1)
    x_test = test.drop('quality', axis=1)

    y_train = train['quality']
    y_test = test['quality']

    scaler = StandardScaler()
    norm_train_X = scaler.fit_transform(x_train)
    norm_test_X = scaler.transform(x_test)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(len(norm_train_X[0]),)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(loss='mse',
                  optimizer='adam',
                  metrics=['mae', 'root_mean_squared_error'])

    # Define the checkpoint callback
    checkpoint_callback = ModelCheckpoint(
        filepath='model.keras',
        monitor='val_root_mean_squared_error',        # Metric to monitor (e.g., validation loss)
        save_best_only=True,       # Save only the best model
        mode='min',                # 'min' for loss, 'max' for accuracy
        verbose=0                # Print a message when saving the model
    )
    model.fit(
        norm_train_X,
        y_train,
        validation_data=(
            norm_test_X,
            y_test),
        epochs=100,
        callbacks=[checkpoint_callback])
    model = tf.keras.models.load_model('model.keras')
    y_pred = model.predict(norm_test_X).flatten()

    def regression_accuracy(y_true, y_pred, threshold=0.5):
        correct = 0
        for true, pred in zip(y_true, y_pred):
            if abs(true - pred) <= threshold:
                correct += 1
        return correct / len(y_true)

    accuracy = regression_accuracy(y_test, y_pred, threshold=0.5)

    return model, accuracy


if __name__ == '__main__':
    data_path = os.environ.get('DATA_PATH', 'data/WineQT.csv')
    model_path = os.environ.get('MODEL_PATH', 'model.keras')

    data = load_data(data_path)
    model, accuracy = train_model(data, model_path)

    # Save metrics for CI/CD pipeline
    metrics_path = os.environ.get('METRICS_PATH', 'metrics.txt')
    with open(metrics_path, 'w') as f:
        f.write(f"accuracy: {accuracy}\n")

    print("Training completed successfully!")
