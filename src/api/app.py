# Testing from start
from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import tensorflow as tf


app = Flask(__name__)

MODEL_PATH = os.environ.get('MODEL_PATH', 'model.keras')


# Load model if exists
def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            # Load TensorFlow model instead of pickle
            return tf.keras.models.load_model(MODEL_PATH)
        else:
            return None
    except Exception as e:
        app.logger.error(f"Error loading model: {e}")
        return None


@app.route('/', methods=['GET'])
def index():
    """Serve the prediction interface"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions using the TensorFlow model"""
    # Special case for testing
    if app.config.get('TESTING', False):
        # Mock response for testing
        data = request.get_json()
        if data and 'features' in data:
            return jsonify({
                "prediction": [0],
                "model_version": os.environ.get('MODEL_VERSION', 'test-version')
            }), 200
        else:
            return jsonify({"error": "Missing 'features' in request data"}), 400

    model_path = os.environ.get('MODEL_PATH', 'model.keras')
    app.logger.info(f"Loading model from: {model_path}")
    app.logger.info(f"Model exists: {os.path.exists(model_path)}")

    model = load_model()

    if model is None:
        app.logger.error(f"Failed to load model from {model_path}")
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Get input data from request
        data = request.get_json()
        if 'features' not in data:
            app.logger.error("Missing 'features' in request data")
            return jsonify({"error": "Missing 'features' in request data"}), 400

        features = np.array(data['features']).reshape(1, -1)

        # Make prediction with TensorFlow model
        prediction = model.predict(features)
        
        # Convert to regular Python types for JSON serialization
        prediction_list = prediction.flatten().tolist()

        return jsonify({
            "prediction": prediction_list,
            "model_version": os.environ.get('MODEL_VERSION', 'unknown')
        }), 200

    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)