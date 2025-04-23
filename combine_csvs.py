import os
import pandas as pd

# Set the directory containing your CSV files
csv_dir = 'csvs/'  # <-- change this to your actual path

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

# Read and combine all CSV files
combined_df = pd.concat(
    [pd.read_csv(os.path.join(csv_dir, f)) for f in csv_files],
    ignore_index=True
)

# Save to a new CSV
combined_df.to_csv(os.path.join(csv_dir, 'combined.csv'), index=False)

