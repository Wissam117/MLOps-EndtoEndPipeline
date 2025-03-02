import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def load_data(data_path='data/dataset.csv'):
    """Load data for training"""
    if not os.path.exists(data_path):
        # If no dataset, create a simple synthetic dataset
        print(f"Dataset not found at {data_path}, creating synthetic data...")
        X = np.random.rand(100, 4)
        y = (X[:, 0] + X[:, 1] > 1).astype(int)
        data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)])
        data['target'] = y
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        data.to_csv(data_path, index=False)
    else:
        print(f"Loading dataset from {data_path}")
        data = pd.read_csv(data_path)
    
    return data

def train_model(data, model_path='model.pkl'):
    """Train a simple ML model and save to disk"""
    # Prepare data
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")
    
    # Save model
    print(f"Saving model to {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    return model, accuracy

if __name__ == '__main__':
    data_path = os.environ.get('DATA_PATH', 'data/dataset.csv')
    model_path = os.environ.get('MODEL_PATH', 'model.pkl')
    
    data = load_data(data_path)
    model, accuracy = train_model(data, model_path)
    
    # Save metrics for CI/CD pipeline
    metrics_path = os.environ.get('METRICS_PATH', 'metrics.txt')
    with open(metrics_path, 'w') as f:
        f.write(f"accuracy: {accuracy}\n")
    
    print("Training completed successfully!")