import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
import os
import mlflow
import mlflow.keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(data_path='data/WineQT.csv'):
    data = pd.read_csv(data_path)
    data = data.drop(['Id'], axis=1)
    data = data.drop_duplicates(keep='first')
    data = data.iloc[np.random.permutation(len(data))]
    return data


def regression_accuracy(y_true, y_pred, threshold=0.5):
    correct = sum(abs(true - pred) <= threshold for true, pred in zip(y_true, y_pred))
    return correct / len(y_true)


def train_model_with_mlflow(data, model_path='model.keras'):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Wine_Quality_Keras_Regression")

    with mlflow.start_run():
        mlflow.set_tag("project", "wine-quality-regression")
        mlflow.set_tag("author", "Fatima Asim")

        train, test = train_test_split(data, test_size=0.2, random_state=1)
        x_train = train.drop('quality', axis=1)
        x_test = test.drop('quality', axis=1)
        y_train = train['quality']
        y_test = test['quality']

        scaler = StandardScaler()
        norm_train_X = scaler.fit_transform(x_train)
        norm_test_X = scaler.transform(x_test)

        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(norm_train_X.shape[1],)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

        model.compile(loss='mse', optimizer='adam', metrics=['mae', 'root_mean_squared_error'])

        mlflow.log_param("optimizer", "adam")
        mlflow.log_param("loss", "mse")
        mlflow.log_param("epochs", 100)
        mlflow.log_param("dense_units", 128)

        checkpoint_callback = ModelCheckpoint(
            filepath=model_path,
            monitor='val_root_mean_squared_error',
            save_best_only=True,
            mode='min',
            verbose=0
        )

        model.fit(
            norm_train_X, y_train,
            validation_data=(norm_test_X, y_test),
            epochs=100,
            callbacks=[checkpoint_callback],
            verbose=0
        )

        model = tf.keras.models.load_model(model_path)
        y_pred = model.predict(norm_test_X).flatten()
        acc = regression_accuracy(y_test, y_pred, threshold=0.5)

        mlflow.log_metric("custom_accuracy", acc)
        mlflow.keras.log_model(model, artifact_path="model")

        print(f"Run ID: {mlflow.active_run().info.run_id}")
        print(f"Custom Regression Accuracy: {acc:.4f}")

        return model, acc


if __name__ == '__main__':
    data_path = os.environ.get('DATA_PATH', 'data/WineQT.csv')
    model_path = os.environ.get('MODEL_PATH', 'model.keras')
    metrics_path = os.environ.get('METRICS_PATH', 'metrics.txt')

    data = load_data(data_path)
    model, accuracy = train_model_with_mlflow(data, model_path)

    with open(metrics_path, 'w') as f:
        f.write(f"accuracy: {accuracy}\n")

    print("Training completed successfully!")
