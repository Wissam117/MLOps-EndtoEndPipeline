from src.model.predict import make_prediction
from src.model.train import load_data, train_model
import unittest
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf

# Add the src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now import the modules from src


class TestModelFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method"""
        # Create a test dataset
        self.test_data_path = 'data/WineQT.csv'
        X = np.random.rand(20, 11)  # 11 features for wine quality data
        y = 3 + 2 * X[:, 0] + X[:, 1]  # Simple regression formula
        
        # Column names based on wine quality dataset
        feature_names = [
            'fixed_acidity', 'volatile_acidity', 'citric_acid', 
            'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
            'total_sulfur_dioxide', 'density', 'ph', 'sulphates', 'alcohol'
        ]
        
        data = pd.DataFrame(X, columns=feature_names)
        data['quality'] = y  # Target column name is 'quality'

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.test_data_path), exist_ok=True)
        data.to_csv(self.test_data_path, index=False)
        # Train and save a test model
        self.test_model_path = 'model.keras'
        self.test_data = data

    def test_load_data(self):
        """Test data loading function"""
        data = load_data(self.test_data_path)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(data.shape[1], 11)  
        self.assertEqual(data.shape[0], 20)

    def test_train_model(self):
        """Test model training function"""
        model, accuracy = train_model(self.test_data, self.test_model_path)
        self.assertIsInstance(model, tf.keras.Model)
        self.assertTrue(os.path.exists(self.test_model_path))
        self.assertTrue(0 <= accuracy <= 1)

    def test_make_prediction(self):
        """Test prediction function"""
        # First train a model
        model, _ = train_model(self.test_data, self.test_model_path)

        # Test prediction with 11 features for wine quality
        features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
        result = make_prediction(model, features)

        self.assertIn('prediction', result)
        # No probability in regression models, but it should still return a value
        self.assertIn('probability', result)
        self.assertIsInstance(result['prediction'], list)
        # Result is now a numerical value, not a class
        self.assertTrue(isinstance(result['prediction'][0], (int, float)))

    def tearDown(self):
        """Clean up after each test method"""
        # Remove test files
        if os.path.exists(self.test_data_path):
            os.remove(self.test_data_path)
        if os.path.exists(self.test_model_path):
            os.remove(self.test_model_path)


if __name__ == '__main__':
    unittest.main()