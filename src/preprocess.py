import os
import pandas as pd
import numpy as np

def preprocess_wine_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.drop_duplicates()
    df = df.dropna()
    if 'Id' in df.columns:
        df = df.drop(columns=['Id'])
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to: {output_path}")

if __name__ == '__main__':
    # Get the path to the directory containing this script (i.e., /project_path/data)
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # Go one level up to project root
    project_root = os.path.abspath(os.path.join(data_dir, os.pardir))

    # Define input and output paths
    input_csv = os.path.join(data_dir, "WineQT_unprocessed.csv")
    output_csv = os.path.join(data_dir, "WineQT.csv")

    preprocess_wine_data(input_csv, output_csv)
