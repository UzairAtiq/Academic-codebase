import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import os

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('/home/sanaullah/University-Stuff/cancer-trend-analysis-project/datasets/dataset_med.csv')

print(f"\n{'='*50}")
print("INITIAL DATASET INFO")
print(f"{'='*50}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumn names and types:")
print(df.dtypes)
print(f"\nFirst few rows:")
print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"\nMemory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Check for duplicates
print(f"\n{'='*50}")
print("CHECKING FOR DUPLICATES")
print(f"{'='*50}")
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

if duplicates > 0:
    print(f"Removing {duplicates} duplicate rows...")
    df = df.drop_duplicates()
    print(f"New shape after removing duplicates: {df.shape}")
else:
    print("No duplicates found!")

# Check for missing values
print(f"\n{'='*50}")
print("CHECKING FOR MISSING VALUES")
print(f"{'='*50}")
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100

missing_df = pd.DataFrame({
    'Column': missing_values.index,
    'Missing_Count': missing_values.values,
    'Percentage': missing_percent.values
})
missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_df) > 0:
    print("Columns with missing values:")
    print(missing_df.to_string(index=False))
else:
    print("No missing values found!")

# Handle missing values
if len(missing_df) > 0:
    print(f"\n{'='*50}")
    print("HANDLING MISSING VALUES")
    print(f"{'='*50}")
    
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                # For numerical columns, fill with median
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                print(f"Filled {col} (numerical) with median: {median_val}")
            else:
                # For categorical columns, fill with mode or 'Unknown'
                if df[col].mode().shape[0] > 0:
                    mode_val = df[col].mode()[0]
                    df[col].fillna(mode_val, inplace=True)
                    print(f"Filled {col} (categorical) with mode: {mode_val}")
                else:
                    df[col].fillna('Unknown', inplace=True)
                    print(f"Filled {col} (categorical) with 'Unknown'")
    
    print(f"\nMissing values after handling: {df.isnull().sum().sum()}")

# Normalize numerical columns
print(f"\n{'='*50}")
print("NORMALIZING NUMERICAL COLUMNS")
print(f"{'='*50}")

# Identify numerical columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(f"Numerical columns to normalize: {numerical_cols}")

if len(numerical_cols) > 0:
    # Create a copy for normalized data
    df_normalized = df.copy()
    
    # Use MinMaxScaler (normalizes to 0-1 range)
    scaler = MinMaxScaler()
    df_normalized[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    print("Normalization complete using MinMaxScaler (0-1 range)")
    print("\nSample of normalized data:")
    print(df_normalized[numerical_cols].head())
else:
    df_normalized = df.copy()
    print("No numerical columns to normalize")

# Split dataset into multiple files
print(f"\n{'='*50}")
print("SPLITTING DATASET INTO SMALLER FILES")
print(f"{'='*50}")

total_rows = len(df_normalized)
num_splits = 3  # Split into 3 files
rows_per_split = total_rows // num_splits

output_dir = '/home/sanaullah/University-Stuff/cancer-trend-analysis-project/datasets'

for i in range(num_splits):
    start_idx = i * rows_per_split
    if i == num_splits - 1:
        # Last split gets all remaining rows
        end_idx = total_rows
    else:
        end_idx = (i + 1) * rows_per_split
    
    split_df = df_normalized.iloc[start_idx:end_idx]
    output_file = os.path.join(output_dir, f'dataset_med_normalized_part{i+1}.csv')
    split_df.to_csv(output_file, index=False)
    print(f"Saved part {i+1}: {output_file} ({len(split_df)} rows)")

# Save the complete normalized dataset as well
complete_output = os.path.join(output_dir, 'dataset_med_normalized_complete.csv')
df_normalized.to_csv(complete_output, index=False)
print(f"\nSaved complete normalized dataset: {complete_output} ({len(df_normalized)} rows)")

# Generate summary report
print(f"\n{'='*50}")
print("SUMMARY REPORT")
print(f"{'='*50}")
print(f"Original dataset rows: {total_rows}")
print(f"Duplicates removed: {duplicates}")
print(f"Missing values handled: {len(missing_df)} columns")
print(f"Numerical columns normalized: {len(numerical_cols)}")
print(f"Dataset split into: {num_splits} files")
print(f"\nOutput files created:")
for i in range(num_splits):
    print(f"  - dataset_med_normalized_part{i+1}.csv")
print(f"  - dataset_med_normalized_complete.csv")
print(f"\n{'='*50}")
print("PREPROCESSING COMPLETE!")
print(f"{'='*50}")
