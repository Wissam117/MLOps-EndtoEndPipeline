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
    input_csv = os.path.join("..", "data", "WineQT_unprocessed.csv")
    output_csv = os.path.join("..", "data", "WineQT.csv")

    preprocess_wine_data(input_csv, output_csv)
