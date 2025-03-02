import os
import pickle
import numpy as np

def load_model(model_path='model.pkl'):
    """Load trained model from disk"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def make_prediction(model, features):
    """Make prediction using the loaded model"""
    # Ensure features are in the right format
    features_array = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(features_array)
    probability = model.predict_proba(features_array).max()
    
    return {
        'prediction': prediction.tolist(),
        'probability': float(probability)
    }

if __name__ == '__main__':
    # Example usage
    model_path = os.environ.get('MODEL_PATH', 'model.pkl')
    model = load_model(model_path)
    
    # Example features (adjust based on your model)
    example_features = [0.1, 0.2, 0.3, 0.4]
    
    result = make_prediction(model, example_features)
    print(f"Prediction: {result['prediction']}")
    print(f"Probability: {result['probability']:.4f}")