import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Define paths
kaggle_dataset = "yasserh/wine-quality-dataset"
project_path = "project_path"
data_dir = os.path.join(project_path, "data")
os.makedirs(data_dir, exist_ok=True)

# Authenticate with Kaggle
api = KaggleApi()
api.authenticate()

# Download dataset as zip
api.dataset_download_files(kaggle_dataset, path=data_dir, unzip=True)

# Identify and rename the relevant file
original_file = os.path.join(data_dir, "WineQT.csv")
target_file = os.path.join(data_dir, "WineQT_unprocessed.csv")

if os.path.exists(original_file):
    os.rename(original_file, target_file)
    print(f"Saved as: {target_file}")
else:
    print("WineQT.csv not found in the dataset.")
