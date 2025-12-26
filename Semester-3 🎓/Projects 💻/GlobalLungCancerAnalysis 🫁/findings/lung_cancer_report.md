# Data Preprocessing Report

**Date:** December 9, 2025  
**Dataset:** dataset_med.csv

## Dataset Description

### What is This Dataset?

This is a **comprehensive lung cancer patient clinical dataset** containing medical records of **890,000 patients** diagnosed with lung cancer across **27 European countries** over a **10-year period (2014-2024)**. The dataset is designed for disease trend analysis, survival prediction, and understanding risk factors associated with lung cancer.

### Key Characteristics

**Clinical Focus:** Lung cancer diagnosis, treatment, and outcomes  
**Geographic Coverage:** 27 European countries (Malta, Ireland, Portugal, France, Sweden, Croatia, Greece, Spain, Netherlands, Denmark, Slovenia, Belgium, Hungary, Romania, Poland, Italy, Germany, Estonia, Czech Republic, Lithuania, Slovakia, Austria, Finland, Luxembourg, Cyprus, Latvia, Bulgaria)  
**Time Period:** June 2, 2014 to May 30, 2024  
**Patient Records:** 890,000 unique cases

### Dataset Purpose

This dataset enables analysis of:

- **Survival Outcomes:** Predict and analyze lung cancer survival rates (22.0% survival rate observed)
- **Risk Factors:** Examine relationships between smoking status, comorbidities, BMI, cholesterol, and cancer outcomes
- **Treatment Effectiveness:** Compare outcomes across different treatment modalities (Chemotherapy, Surgery, Radiation, Combined)
- **Disease Staging:** Analyze progression and outcomes by cancer stage (Stage I-IV)
- **Geographic Trends:** Identify regional patterns in lung cancer incidence and outcomes
- **Comorbidity Impact:** Understand how conditions like hypertension (75%), asthma (47%), cirrhosis (22.6%), and other cancers (8.8%) affect outcomes

### Notable Features

- **Balanced Distribution:** Approximately equal representation across cancer stages and treatment types
- **Diverse Risk Profiles:** Includes patients with varying smoking histories (current, former, never, passive)
- **Complete Clinical Picture:** Combines demographic data, lifestyle factors, comorbidities, treatment details, and outcomes
- **Family History:** Tracks genetic predisposition (50% have family history)
- **Normalized Data:** All numerical features scaled to [0-1] range for machine learning applications

---

## Summary

Successfully preprocessed the medical dataset with the following operations:

- ✓ Removed duplicates
- ✓ Handled missing values
- ✓ Normalized numerical features
- ✓ Split into 3 smaller files

---

## Dataset Information

### Original Dataset

- **File:** `dataset_med.csv`
- **Size:** 89.05 MB
- **Total Rows:** 890,000
- **Total Columns:** 17

### Columns

1. `id` - Patient identifier (normalized)
2. `age` - Patient age (normalized, range: 3-97 years old)
3. `gender` - Patient gender (Male/Female, evenly distributed)
4. `country` - Country of diagnosis (27 European countries)
5. `diagnosis_date` - Date of lung cancer diagnosis (2014-2024)
6. `cancer_stage` - Cancer stage at diagnosis (Stage I, II, III, IV - evenly distributed)
7. `family_history` - Family history of cancer (Yes/No - 50% split)
8. `smoking_status` - Smoking status (Current Smoker, Former Smoker, Never Smoked, Passive Smoker)
9. `bmi` - Body Mass Index (normalized)
10. `cholesterol_level` - Cholesterol level (normalized)
11. `hypertension` - Hypertension status (0/1 - 75% have hypertension)
12. `asthma` - Asthma status (0/1 - 47% have asthma)
13. `cirrhosis` - Cirrhosis status (0/1 - 22.6% have cirrhosis)
14. `other_cancer` - Other cancer history (0/1 - 8.8% have other cancers)
15. `treatment_type` - Type of treatment received (Chemotherapy, Surgery, Radiation, Combined)
16. `end_treatment_date` - Treatment end date
17. `survived` - Survival outcome (0 = Did not survive, 1 = Survived - 22% survival rate)

### Statistical Overview

**Cancer Stage Distribution:**

- Stage III: 222,594 patients (25.0%)
- Stage IV: 222,527 patients (25.0%)
- Stage I: 222,516 patients (25.0%)
- Stage II: 222,363 patients (25.0%)

**Treatment Type Distribution:**

- Chemotherapy: 223,262 patients (25.1%)
- Surgery: 223,261 patients (25.1%)
- Combined Therapy: 222,609 patients (25.0%)
- Radiation: 220,868 patients (24.8%)

**Smoking Status Distribution:**

- Passive Smoker: 223,170 patients (25.1%)
- Never Smoked: 222,751 patients (25.0%)
- Former Smoker: 222,181 patients (25.0%)
- Current Smoker: 221,898 patients (24.9%)

**Survival Outcomes:**

- Survived: 196,004 patients (22.0%)
- Did Not Survive: 693,996 patients (78.0%)

**Comorbidity Prevalence:**

- Hypertension: 667,521 patients (75.0%)
- Asthma: 418,069 patients (47.0%)
- Cirrhosis: 201,101 patients (22.6%)
- Other Cancer History: 78,460 patients (8.8%)

---

## Preprocessing Steps

### 1. Duplicate Removal

- **Duplicates Found:** 0
- **Action:** No duplicates were present in the original dataset

### 2. Missing Values Handling

- **Missing Values Found:** 0 (or handled)
- **Strategy:**
  - Numerical columns: Filled with median values
  - Categorical columns: Filled with mode or 'Unknown'

### 3. Data Normalization

- **Method:** MinMaxScaler (0-1 range normalization)
- **Numerical Columns Normalized:** 9 columns
  - id, age, bmi, cholesterol_level, hypertension, asthma, cirrhosis, other_cancer, survived
- **Result:** All numerical values scaled to range [0.0, 1.0]

### 4. Dataset Splitting

The large dataset was split into 3 equal parts for easier handling:

| File                               | Rows        | Size          | Duplicates | Missing Values |
| ---------------------------------- | ----------- | ------------- | ---------- | -------------- |
| `dataset_med_normalized_part1.csv` | 296,666     | 45.46 MB      | 0          | 0              |
| `dataset_med_normalized_part2.csv` | 296,666     | 45.26 MB      | 0          | 0              |
| `dataset_med_normalized_part3.csv` | 296,668     | 45.19 MB      | 0          | 0              |
| **Total**                          | **890,000** | **135.91 MB** | **0**      | **0**          |

---

## Output Files

### Normalized Split Files (Recommended for analysis)

1. **dataset_med_normalized_part1.csv** - First third of the dataset
2. **dataset_med_normalized_part2.csv** - Second third of the dataset
3. **dataset_med_normalized_part3.csv** - Final third of the dataset

### Complete Normalized Dataset

- **dataset_med_normalized_complete.csv** - Full dataset with all preprocessing applied

---

## Data Quality Verification

✓ **No duplicates** in any of the output files  
✓ **No missing values** in any of the output files  
✓ **All numerical columns normalized** to [0, 1] range  
✓ **Data integrity maintained** - Total rows preserved (890,000)  
✓ **Column structure preserved** - All 17 columns maintained

---

## Usage Recommendations

### For Analysis

Use the split files (`dataset_med_normalized_part1.csv`, `part2.csv`, `part3.csv`) to:

- Reduce memory usage
- Enable parallel processing
- Facilitate easier data manipulation

### For Complete Operations

Use `dataset_med_normalized_complete.csv` when you need the entire dataset in one file.

---

## Next Steps

The preprocessed data is now ready for:

1. Exploratory Data Analysis (EDA)
2. Feature engineering
3. Machine learning model training
4. Statistical analysis
5. Visualization

All files are located in: `/home/sanaullah/University-Stuff/cancer-trend-analysis-project/datasets/`
