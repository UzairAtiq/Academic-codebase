import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
    """Load the air pollution dataset."""
    df = pd.read_csv('datasets/air_pollution.csv')
    print(f"Original dataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head(10))
    print(f"\nColumn names: {df.columns.tolist()}")
    print(f"\nData types:")
    print(df.dtypes)
    return df

def check_duplicates(df):
    """Check for and remove duplicate records."""
    print("\n" + "="*60)
    print("CHECKING FOR DUPLICATES")
    print("="*60)
    
    # Check for exact duplicates
    duplicates = df.duplicated()
    num_duplicates = duplicates.sum()
    print(f"Number of duplicate rows: {num_duplicates}")
    
    if num_duplicates > 0:
        print("\nDuplicate rows:")
        print(df[duplicates])
        
        # Remove duplicates
        df_clean = df.drop_duplicates()
        print(f"\nDataset shape after removing duplicates: {df_clean.shape}")
        return df_clean
    else:
        print("No duplicate rows found.")
        return df

def analyze_missing_values(df):
    """Analyze missing values in the dataset."""
    print("\n" + "="*60)
    print("MISSING VALUE ANALYSIS")
    print("="*60)
    
    # Count missing values per column
    missing_counts = df.isnull().sum()
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing_counts.index,
        'Missing_Count': missing_counts.values,
        'Missing_Percentage': missing_percentages.values
    })
    
    print("\nMissing values per column:")
    print(missing_df)
    
    # Total missing values
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    overall_missing_pct = (total_missing / total_cells) * 100
    
    print(f"\nTotal missing values: {total_missing} out of {total_cells} cells ({overall_missing_pct:.2f}%)")
    
    return missing_df

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    print("\n" + "="*60)
    print("HANDLING MISSING VALUES")
    print("="*60)
    
    df_clean = df.copy()
    
    # For air pollution data (numeric columns with years), we have several strategies:
    # 1. Keep city and country columns as-is (they shouldn't have missing values)
    # 2. For year columns (pollution measurements), we can:
    #    - Forward fill: use previous year's value
    #    - Backward fill: use next year's value
    #    - Interpolate: calculate based on surrounding years
    #    - Mean imputation: use country/global mean
    
    # Check if city/country have missing values
    id_cols = ['city', 'country']
    year_cols = [col for col in df.columns if col not in id_cols]
    
    print(f"\nIdentifier columns: {id_cols}")
    print(f"Year columns: {year_cols}")
    
    # Check for missing values in identifier columns
    for col in id_cols:
        missing = df_clean[col].isnull().sum()
        if missing > 0:
            print(f"\nWarning: {missing} missing values found in '{col}' column")
            # Remove rows with missing city or country
            df_clean = df_clean.dropna(subset=[col])
            print(f"Removed rows with missing '{col}'. New shape: {df_clean.shape}")
    
    # Handle missing values in year columns
    print(f"\nStrategy for year columns: Interpolation along rows (time series)")
    print("This will estimate missing values based on available years for each city.")
    
    # Store original missing count
    original_missing = df_clean[year_cols].isnull().sum().sum()
    
    # Interpolate across years for each city (row-wise)
    df_clean[year_cols] = df_clean[year_cols].interpolate(method='linear', axis=1, limit_direction='both')
    
    # After interpolation, if there are still missing values (e.g., all years missing for a city),
    # we can either:
    # 1. Drop those rows
    # 2. Fill with country mean
    # 3. Fill with global mean
    
    remaining_missing = df_clean[year_cols].isnull().sum().sum()
    
    print(f"\nMissing values before interpolation: {original_missing}")
    print(f"Missing values after interpolation: {remaining_missing}")
    
    if remaining_missing > 0:
        print(f"\nApplying country-level mean imputation for remaining missing values...")
        
        # Group by country and fill with country mean
        for col in year_cols:
            df_clean[col] = df_clean.groupby('country')[col].transform(
                lambda x: x.fillna(x.mean())
            )
        
        still_missing = df_clean[year_cols].isnull().sum().sum()
        print(f"Missing values after country-level imputation: {still_missing}")
        
        if still_missing > 0:
            print(f"\nApplying global mean imputation for any remaining missing values...")
            # Fill remaining with global mean
            df_clean[year_cols] = df_clean[year_cols].fillna(df_clean[year_cols].mean())
            
            final_missing = df_clean[year_cols].isnull().sum().sum()
            print(f"Missing values after global imputation: {final_missing}")
    
    return df_clean

def generate_statistics(df_original, df_clean):
    """Generate statistics comparing original and cleaned datasets."""
    print("\n" + "="*60)
    print("PREPROCESSING SUMMARY")
    print("="*60)
    
    print(f"\nOriginal dataset shape: {df_original.shape}")
    print(f"Cleaned dataset shape: {df_clean.shape}")
    print(f"Rows removed: {df_original.shape[0] - df_clean.shape[0]}")
    
    print(f"\nOriginal missing values: {df_original.isnull().sum().sum()}")
    print(f"Cleaned missing values: {df_clean.isnull().sum().sum()}")
    
    # Get year columns for statistics
    year_cols = [col for col in df_clean.columns if col not in ['city', 'country']]
    
    print("\nDescriptive statistics of cleaned data:")
    print(df_clean[year_cols].describe())
    
    return

def save_cleaned_data(df):
    """Save the cleaned dataset."""
    output_path = 'datasets/air_pollution_normalized.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Cleaned dataset saved to: {output_path}")
    return output_path

def generate_report(df_original, df_clean, missing_analysis):
    """Generate a detailed preprocessing report."""
    report_path = 'findings/air_pollution_preprocessing_report.md'
    
    year_cols = [col for col in df_clean.columns if col not in ['city', 'country']]
    
    report = f"""# Air Pollution Dataset Preprocessing Report

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview

### Original Dataset
- **Shape:** {df_original.shape[0]} rows × {df_original.shape[1]} columns
- **Columns:** {', '.join(df_original.columns.tolist())}
- **Total cells:** {df_original.shape[0] * df_original.shape[1]:,}

### Cleaned Dataset
- **Shape:** {df_clean.shape[0]} rows × {df_clean.shape[1]} columns
- **Rows removed:** {df_original.shape[0] - df_clean.shape[0]}

## Preprocessing Steps

### 1. Duplicate Detection and Removal

- **Duplicates found:** {df_original.duplicated().sum()}
- **Action:** Removed all duplicate rows

### 2. Missing Value Analysis

#### Missing Values by Column (Original Dataset)

| Column | Missing Count | Missing Percentage |
|--------|---------------|-------------------|
"""
    
    for _, row in missing_analysis.iterrows():
        report += f"| {row['Column']} | {int(row['Missing_Count'])} | {row['Missing_Percentage']:.2f}% |\n"
    
    total_missing_original = df_original.isnull().sum().sum()
    total_cells = df_original.shape[0] * df_original.shape[1]
    
    report += f"""
**Total missing values (original):** {total_missing_original:,} out of {total_cells:,} cells ({(total_missing_original/total_cells)*100:.2f}%)

### 3. Missing Value Handling Strategy

For the air pollution dataset, missing values were handled using a multi-step approach:

1. **Identifier Columns (city, country):**
   - Rows with missing city or country names were removed
   
2. **Year Columns (pollution measurements):**
   - **Step 1 - Linear Interpolation:** Missing values were interpolated based on available years for each city (time series interpolation)
   - **Step 2 - Country-level Mean Imputation:** Remaining missing values were filled with the mean pollution level of the country
   - **Step 3 - Global Mean Imputation:** Any still-remaining missing values were filled with the global mean

### 4. Results

- **Missing values after preprocessing:** {df_clean.isnull().sum().sum()}
- **Data completeness:** {((1 - df_clean.isnull().sum().sum()/(df_clean.shape[0]*df_clean.shape[1]))*100):.2f}%

## Descriptive Statistics (Cleaned Data)

### Pollution Levels by Year (PM2.5 μg/m³)

"""
    
    stats = df_clean[year_cols].describe()
    report += "| Statistic | " + " | ".join(year_cols) + " |\n"
    report += "|" + "----|" * (len(year_cols) + 1) + "\n"
    
    for stat in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']:
        report += f"| {stat} | "
        for col in year_cols:
            report += f"{stats.loc[stat, col]:.2f} | "
        report += "\n"
    
    report += f"""

## Data Quality Assessment

✓ **Duplicates:** Removed
✓ **Missing values:** Handled using interpolation and imputation
✓ **Data integrity:** All pollution measurements are numeric
✓ **Completeness:** {((1 - df_clean.isnull().sum().sum()/(df_clean.shape[0]*df_clean.shape[1]))*100):.2f}%

## Output

- **Normalized dataset saved to:** `datasets/air_pollution_normalized.csv`
- **Format:** CSV (comma-separated values)

## Recommendations

1. The dataset is now ready for analysis and visualization
2. Consider analyzing trends over time (2017-2023)
3. Compare pollution levels across countries and cities
4. Identify cities with highest/lowest pollution levels
5. Analyze correlation with health outcomes (e.g., lung cancer rates)

---
*Report generated by air_pollution_preprocessing.py*
"""
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Preprocessing report saved to: {report_path}")
    return report_path

def main():
    """Main preprocessing pipeline."""
    print("="*60)
    print("AIR POLLUTION DATASET PREPROCESSING")
    print("="*60)
    
    # Load data
    df_original = load_data()
    
    # Check and remove duplicates
    df = check_duplicates(df_original)
    
    # Analyze missing values
    missing_analysis = analyze_missing_values(df)
    
    # Handle missing values
    df_clean = handle_missing_values(df)
    
    # Generate statistics
    generate_statistics(df_original, df_clean)
    
    # Save cleaned data
    save_cleaned_data(df_clean)
    
    # Generate report
    generate_report(df_original, df_clean, missing_analysis)
    
    print("\n" + "="*60)
    print("PREPROCESSING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
