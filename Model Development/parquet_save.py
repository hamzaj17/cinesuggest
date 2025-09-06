import pandas as pd
from pathlib import Path

# Define paths
data_dir = Path(r"D:\cinesuggest\Model Development\data")
csv_path = data_dir / "ratings_cleaned.csv"
parquet_path = data_dir / "ratings_cleaned.parquet"

# Load CSV
print("⏳ Loading CSV file...")
ratings = pd.read_csv(csv_path)

# Save as Parquet
ratings.to_parquet(parquet_path, index=False)

print(f"✅ Parquet file saved at: {parquet_path}")
