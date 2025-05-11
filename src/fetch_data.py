import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Define dataset and relative path to data folder
kaggle_dataset = "yasserh/wine-quality-dataset"
data_dir = os.path.join("..", "data")
os.makedirs(data_dir, exist_ok=True)

# Authenticate with Kaggle
api = KaggleApi()
api.authenticate()

# Download and unzip dataset
api.dataset_download_files(kaggle_dataset, path=data_dir, unzip=True)

# Rename the WineQT.csv file
original_file = os.path.join(data_dir, "WineQT.csv")
target_file = os.path.join(data_dir, "WineQT_unprocessed.csv")

if os.path.exists(original_file):
    os.rename(original_file, target_file)
    print(f"Saved as: {target_file}")
else:
    print("WineQT.csv not found in the dataset.")
