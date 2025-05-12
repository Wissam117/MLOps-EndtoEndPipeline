import os
import pandas as pd
import numpy as np

def preprocess_wine_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.drop_duplicates()
    df = df.dropna()
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to: {output_path}")

if __name__ == '__main__':
    # Get the project directory (parent of src)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # src directory
    project_dir = os.path.dirname(script_dir)  # Pipelining directory

    # Define absolute paths
    input_csv = os.path.join(project_dir, "data", "WineQT_unprocessed.csv")
    output_csv = os.path.join(project_dir, "data", "WineQT.csv")

    # Verify input file exists
    if not os.path.exists(input_csv):
        print(f"Error: Input file not found at {input_csv}")
        exit(1)

    preprocess_wine_data(input_csv, output_csv)