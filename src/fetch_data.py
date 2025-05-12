import os

# Set KAGGLE_CONFIG_DIR before importing kaggle
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script (src)
project_dir = os.path.dirname(script_dir)  # Parent directory (project root)
os.environ['KAGGLE_CONFIG_DIR'] = project_dir  # Set Kaggle config directory

# Verify kaggle.json exists
kaggle_json_path = os.path.join(project_dir, 'kaggle.json')
if not os.path.exists(kaggle_json_path):
    print(f"Error: 'kaggle.json' not found in {project_dir}")
    exit(1)

# Now import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

# Define dataset and data directory
kaggle_dataset = "yasserh/wine-quality-dataset"
data_dir = os.path.join(project_dir, "data")  # Absolute path to project_dir/data

# Create the data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Authenticate with Kaggle
api = KaggleApi()
api.authenticate()

# Download and unzip dataset
try:
    api.dataset_download_files(kaggle_dataset, path=data_dir, unzip=True)
    print(f"Dataset '{kaggle_dataset}' downloaded and unzipped to '{data_dir}'.")
except Exception as e:
    print(f"Error downloading dataset: {e}")
    exit(1)

# Rename the WineQT.csv file
original_file = os.path.join(data_dir, "WineQT.csv")
target_file = os.path.join(data_dir, "WineQT_unprocessed.csv")

if os.path.exists(original_file):
    os.rename(original_file, target_file)
    print(f"Saved as: {target_file}")
else:
    print("WineQT.csv not found in the dataset.")