from src.model.predict import make_prediction
from src.model.train import load_data, train_model
import unittest
import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Add the src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now import the modules from src


class TestModelFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method"""
        # Create a test dataset
        self.test_data_path = 'tests/test_data.csv'
        X = np.random.rand(20, 4)
        y = (X[:, 0] + X[:, 1] > 1).astype(int)
        data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)])
        data['target'] = y

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.test_data_path), exist_ok=True)
        data.to_csv(self.test_data_path, index=False)

        # Train and save a test model
        self.test_model_path = 'tests/test_model.pkl'
        self.test_data = data

    def test_load_data(self):
        """Test data loading function"""
        data = load_data(self.test_data_path)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(data.shape[1], 5)  # 4 features + target
        self.assertEqual(data.shape[0], 20)  # 20 samples

    def test_train_model(self):
        """Test model training function"""
        model, accuracy = train_model(self.test_data, self.test_model_path)
        self.assertIsInstance(model, RandomForestClassifier)
        self.assertTrue(os.path.exists(self.test_model_path))
        self.assertTrue(0 <= accuracy <= 1)

    def test_make_prediction(self):
        """Test prediction function"""
        # First train a model
        model, _ = train_model(self.test_data, self.test_model_path)

        # Test prediction
        features = [0.1, 0.2, 0.3, 0.4]
        result = make_prediction(model, features)

        self.assertIn('prediction', result)
        self.assertIn('probability', result)
        self.assertIsInstance(result['prediction'], list)
        self.assertIsInstance(result['probability'], float)

    def tearDown(self):
        """Clean up after each test method"""
        # Remove test files
        if os.path.exists(self.test_data_path):
            os.remove(self.test_data_path)
        if os.path.exists(self.test_model_path):
            os.remove(self.test_model_path)


if __name__ == '__main__':
    unittest.main()
