import pandas as pd

INPUT_FILE = "data/cicids2017_cleaned.csv"
OUTPUT_FILE = "data/cicids2017_labeled.csv"

CHUNK_SIZE = 200_000

def encode_labels_chunkwise():
    first_chunk = True
    total_rows = 0

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
        # Normalize column names
        chunk.columns = chunk.columns.str.strip()

        # Encode labels
        chunk["Label"] = chunk["Label"].apply(
            lambda x: 0 if str(x).strip().upper() == "BENIGN" else 1
        )

        # Write to output file
        chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk
        )

        total_rows += len(chunk)
        first_chunk = False
        print(f"Processed {total_rows} rows")

    print("\nLabel encoding completed successfully")
    print(f"Labeled dataset saved as: {OUTPUT_FILE}")

if __name__ == "__main__":
    encode_labels_chunkwise()
