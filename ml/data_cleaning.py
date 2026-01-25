import pandas as pd
import numpy as np

INPUT_FILE = "data/cicids2017_selected.csv"
OUTPUT_FILE = "data/cicids2017_cleaned.csv"

CHUNK_SIZE = 200_000

def clean_data_chunkwise():
    first_chunk = True
    total_rows = 0
    medians = None

    # -------- First pass: compute medians --------
    print("Computing feature medians...")

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
        chunk.columns = chunk.columns.str.strip()

        # Replace infinities with NaN
        chunk.replace([np.inf, -np.inf], np.nan, inplace=True)

        numeric_cols = chunk.select_dtypes(include=[np.number])

        if medians is None:
            medians = numeric_cols.median()
        else:
            medians = medians.add(numeric_cols.median(), fill_value=0)

    medians = medians / (total_rows + 1 if total_rows else 1)

    print("Median calculation completed")

    # -------- Second pass: clean & save --------
    print("Cleaning data and writing output...")

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
        chunk.columns = chunk.columns.str.strip()

        # Replace infinities with NaN
        chunk.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Fill NaN with medians
        for col in medians.index:
            if col in chunk.columns:
                chunk[col].fillna(medians[col], inplace=True)

        # Write cleaned chunk
        chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk
        )

        total_rows += len(chunk)
        first_chunk = False
        print(f"Processed {total_rows} rows")

    print("\nData cleaning completed successfully")
    print(f"Clean dataset saved as: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_data_chunkwise()
