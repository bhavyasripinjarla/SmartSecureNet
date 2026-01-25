import pandas as pd

INPUT_FILE = "data/cicids2017_merged.csv"
OUTPUT_FILE = "data/cicids2017_selected.csv"

# Desired features (normalized names)
DESIRED_FEATURES = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Packet Length Mean",
    "Packet Length Std",
    "Packet Length Variance",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Fwd IAT Mean",
    "Bwd IAT Mean",
    "Fwd Header Length",
    "Bwd Header Length",
    "Average Packet Size",
    "Active Mean",
    "Idle Mean",
    "Label"
]

CHUNK_SIZE = 200_000

def normalize_columns(df):
    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()
    return df

def select_features_chunkwise():
    first_chunk = True
    total_rows = 0
    selected_columns = None

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
        chunk = normalize_columns(chunk)

        # Detect available columns only once
        if selected_columns is None:
            selected_columns = [c for c in DESIRED_FEATURES if c in chunk.columns]

            print("Using columns:")
            for col in selected_columns:
                print("  -", col)

        # Select available columns
        chunk_selected = chunk[selected_columns]

        # Write output
        chunk_selected.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk
        )

        total_rows += len(chunk_selected)
        first_chunk = False
        print(f"Processed {total_rows} rows")

    print("\nFeature selection completed successfully")
    print(f"Saved file: {OUTPUT_FILE}")
    print(f"Total rows written: {total_rows}")

if __name__ == "__main__":
    select_features_chunkwise()
