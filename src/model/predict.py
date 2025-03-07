import os
import numpy as np
import tensorflow as tf


def load_model(model_path='model.keras'):
    """Load trained TensorFlow model from disk"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load TensorFlow model instead of pickle
    model = tf.keras.models.load_model(model_path)

    return model


def make_prediction(model, features):
    """Make prediction using the loaded TensorFlow model"""
    # Ensure features are in the right format
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)

    return {
        'prediction': prediction.flatten().tolist(),
        'probability': 1.0  # Placeholder for regression model
    }


if __name__ == '__main__':
    # Example usage
    model_path = os.environ.get('MODEL_PATH', 'model.keras')
    model = load_model(model_path)

    # Example features (adjust based on your model)
    example_features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]

    result = make_prediction(model, example_features)
    print(f"Prediction: {result['prediction']}")
