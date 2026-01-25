import pandas as pd
import glob
import os

# Path where CICIDS CSV files are stored
DATASET_PATH = "data/*.csv"

def merge_cicids():
    all_files = glob.glob(DATASET_PATH)

    print(f"Found {len(all_files)} CSV files")

    df_list = []

    for file in all_files:
        print(f"Loading: {os.path.basename(file)}")
        df = pd.read_csv(file, low_memory=False)
        df_list.append(df)

    # Merge all CSVs
    merged_df = pd.concat(df_list, ignore_index=True)

    print("\nMerge completed")
    print(f"Total rows: {merged_df.shape[0]}")
    print(f"Total columns: {merged_df.shape[1]}")

    # Save merged dataset
    output_path = "data/cicids2017_merged.csv"
    merged_df.to_csv(output_path, index=False)

    print(f"\nMerged dataset saved as: {output_path}")

if __name__ == "__main__":
    merge_cicids()
