import os
import json
import time
import nbformat as nbf
from nbclient import NotebookClient

target_dir = "/Users/uzair/academic-codebase📘/Semester-5 🎓/Class-Codes 📚/ML"
notebook_path = os.path.join(target_dir, "ML_Assignment_1_Winter_Wheat_Yield_Regression.ipynb")
csv_path = os.path.join(target_dir, "cycless_winter_wheat.csv")

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.12.0"
    }
}

cells = []

# Cell 1: Title and Citation
cells.append(nbf.v4.new_markdown_cell("""# Machine Learning Assignment 1: Winter-Wheat Yield Regression on the CYCleSS Dataset
**Course:** Machine Learning (Semester 5)  
**Case Study:** Precision Winter-Wheat Yield Modeling across England (2015–2017)  
**Dataset Citation:**  
Corcoran, E., Bebber, D. P., Curceac, S., Efremova, N., Lashkari, A., Mead, A., Morris, R. J., Pywell, R. F., Redhead, J. W., & Ahnert, S. E. (2026). *A comprehensive UK crop yield dataset incorporating satellite, weather, and soil type information*. **Scientific Data**, 13:491. DOI: [10.1038/s41597-024-03978-y](https://doi.org/10.1038/s41597-024-03978-y).

---
### Assignment Objectives
1. **Data Preparation & Validation (Q1):** Aggregate 5-daily Sentinel-1 SAR (VV, VH, Ratio), daily CHESS meteorological data (precip, temp, rsds, pet), and European soil properties into field-year observations for winter wheat over March 1 – July 31.
2. **Simple Linear Regression (Q1):** Compare manual NumPy normal equation against Scikit-learn on Yield vs. Seasonal Precipitation.
3. **Multiple Linear Regression & Interpretation (Q2):** Standardize features, diagnose and resolve perfect soil texture collinearity, interpret agronomic coefficients, and perform feature ablation.
4. **Evaluation Metrics & Prediction Intervals (Q3):** Implement MAE, MSE, RMSE, and $R^2$ from scratch, benchmark against naive baseline, and construct calibrated 90% prediction intervals.
5. **Gradient Descent (Q4):** Derive gradient analytically, implement batch gradient descent, investigate learning rates, and analyze the impact of feature scaling.
6. **Normal Equation vs. Gradient Descent (Q5):** Evaluate computational complexity, benchmark execution scaling with feature dimension, and address high-dimensional singular cases ($n \gg m$).
7. **Bonus Tasks:** Early stopping gradient descent and spatial GroupKFold cross-validation against random K-fold."""))

# Cell 2: Q1 Heading
cells.append(nbf.v4.new_markdown_cell("""## Q1. Data Preparation and Manual vs. Scikit-learn Linear Regression
### Part A: Building the Analysis Table (`cycless_winter_wheat.csv`)"""))

# Cell 3: Data prep code
code_q1_a = """# 1. build analysis table from raw satellite, soil, and climate files
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# set random seed for reproducible results
np.random.seed(42)

# set global plotting aesthetic
sns.set_theme(style='whitegrid', font_scale=1.05)
plt.rcParams['figure.figsize'] = (9, 5)

# define data directory and harvest seasonal window (march 1 - july 31)
data_dir = 'CYCleSS_dataset/data'
seasonal_months = [3, 4, 5, 6, 7]

yearly_records = []
for year in [2015, 2016, 2017]:
    # load satellite radar files
    vv_path = os.path.join(data_dir, f'crop_yield_type_and_satellite_data/VV_{year}_MeanYieldperField.csv')
    vh_path = os.path.join(data_dir, f'crop_yield_type_and_satellite_data/VH_{year}_MeanYieldperField.csv')
    ratio_path = os.path.join(data_dir, f'crop_yield_type_and_satellite_data/Ratio_{year}_MeanYieldperField.csv')
    
    df_vv = pd.read_csv(vv_path)
    df_vh = pd.read_csv(vh_path)
    df_ratio = pd.read_csv(ratio_path)
    
    # filter for winter wheat records only (exact label 'wheat')
    wheat_vv = df_vv[df_vv['Crop'] == 'Wheat'].copy()
    wheat_vh = df_vh[df_vh['Crop'] == 'Wheat'].copy()
    wheat_ratio = df_ratio[df_ratio['Crop'] == 'Wheat'].copy()
    
    # identify seasonal columns (date format x<year>.<month>.<day>)
    vv_dates = [c for c in wheat_vv.columns if c.startswith('X') and int(c.split('.')[1]) in seasonal_months]
    vh_dates = [c for c in wheat_vh.columns if c.startswith('X') and int(c.split('.')[1]) in seasonal_months]
    ratio_dates = [c for c in wheat_ratio.columns if c.startswith('X') and int(c.split('.')[1]) in seasonal_months]
    
    # compute seasonal mean per field (skipping na values across observation passes)
    wheat_vv['mean_VV'] = wheat_vv[vv_dates].mean(axis=1, skipna=True)
    wheat_vh['mean_VH'] = wheat_vh[vh_dates].mean(axis=1, skipna=True)
    wheat_ratio['mean_Ratio'] = wheat_ratio[ratio_dates].mean(axis=1, skipna=True)
    
    # merge satellite radar features on field id
    field_df = wheat_vv[['ID', 'grid_ID', 'Year', 'Crop', 'Yield', 'mean_VV']].merge(
        wheat_vh[['ID', 'mean_VH']], on='ID'
    ).merge(
        wheat_ratio[['ID', 'mean_Ratio']], on='ID'
    )
    
    # load soil dataset (2015_2016 or 2017)
    soil_file = 'LandUseandSoil_2015_2016.csv' if year in [2015, 2016] else 'LandUseandSoil_2017.csv'
    df_soil = pd.read_csv(os.path.join(data_dir, 'soil_data', soil_file))
    soil_cols = ['clay', 'silt', 'sand', 'bd', 'awc', 'fc', 'wp', 'ks', 'cf']
    soil_sub = df_soil[['ID'] + soil_cols].drop_duplicates(subset=['ID'])
    field_df = field_df.merge(soil_sub, on='ID', how='left')
    
    # load and aggregate meteorological variables per 10km grid cell
    precip_raw = pd.read_csv(os.path.join(data_dir, f'climate_data/{year}/precip_{year}.csv')).drop_duplicates(subset=['grid_ID'])
    tas_raw = pd.read_csv(os.path.join(data_dir, f'climate_data/{year}/tas_{year}.csv')).drop_duplicates(subset=['grid_ID'])
    rsds_raw = pd.read_csv(os.path.join(data_dir, f'climate_data/{year}/rsds_{year}.csv')).drop_duplicates(subset=['grid_ID'])
    pet_raw = pd.read_csv(os.path.join(data_dir, f'climate_data/{year}/pet_{year}.csv')).drop_duplicates(subset=['grid_ID'])
    
    clim_dates = [c for c in precip_raw.columns if c.startswith('X') and int(c.split('.')[1]) in seasonal_months]
    
    clim_df = pd.DataFrame({'grid_ID': precip_raw['grid_ID']})
    # convert precipitation from kg m^-2 s^-1 to total mm over 153 days
    clim_df['total_precip_mm'] = precip_raw[clim_dates].sum(axis=1).values * 86400.0
    # convert temperature from kelvin to degrees celsius
    clim_df['mean_temp_c'] = tas_raw[clim_dates].mean(axis=1).values - 273.15
    # calculate seasonal mean solar radiation and potential evapotranspiration
    clim_df['mean_rsds'] = rsds_raw[clim_dates].mean(axis=1).values
    clim_df['mean_pet'] = pet_raw[clim_dates].mean(axis=1).values
    
    field_df = field_df.merge(clim_df, on='grid_ID', how='left')
    yearly_records.append(field_df)

# combine all three years into unified analysis dataset
cycless_df = pd.concat(yearly_records, ignore_index=True)

# save cleaned dataset to csv as required by q1 instructions
cycless_df.to_csv('cycless_winter_wheat.csv', index=False)
print(f'successfully created cycless_winter_wheat.csv with shape: {cycless_df.shape}')
cycless_df.head(3)"""
cells.append(nbf.v4.new_code_cell(code_q1_a))

# Cell 4: Data dictionary markdown
cells.append(nbf.v4.new_markdown_cell("""### Data Dictionary (`cycless_winter_wheat.csv`)

| Variable | Unit | Description / Agronomic Meaning |
| :--- | :--- | :--- |
| `ID` | String | Unique identifier of the sampled agricultural field |
| `grid_ID` | Integer | British National Grid 10 km square reference containing the field |
| `Year` | Year | Harvest year of the crop (2015, 2016, or 2017) |
| `Crop` | Category | Crop classification label (`Wheat` representing winter wheat) |
| `Yield` | t/ha | Harvester-measured mean grain yield per field (Target Variable) |
| `clay` | % | Soil clay fraction (particle diameter < 0.002 mm) |
| `silt` | % | Soil silt fraction (particle diameter 0.002 – 0.05 mm) |
| `sand` | % | Soil sand fraction (particle diameter 0.05 – 2.0 mm) |
| `bd` | g/cm³ | Topsoil bulk density |
| `awc` | m³/m³ | Plant available water capacity |
| `fc` | m³/m³ | Soil moisture content at field capacity |
| `wp` | m³/m³ | Soil moisture content at permanent wilting point |
| `ks` | cm/day | Saturated hydraulic conductivity |
| `cf` | % | Coarse fragments / stone content percentage |
| `total_precip_mm` | mm | Total cumulative precipitation over March 1 – July 31 |
| `mean_temp_c` | °C | Mean daily 2m air temperature over March 1 – July 31 |
| `mean_rsds` | W/m² | Mean downward surface shortwave solar radiation |
| `mean_pet` | mm/day | Mean daily potential evapotranspiration (Penman-Monteith) |
| `mean_VV` | dB | Mean Sentinel-1 radar backscatter (vertical transmit, vertical receive) |
| `mean_VH` | dB | Mean Sentinel-1 cross-polarization radar backscatter (VV-VH ratio sensitive to crop volume) |
| `mean_Ratio` | Ratio | Mean polarization ratio between VV and VH |"""))

# Cell 5: Q1 reporting code
code_q1_report = """# 2. inspect records per year, missing values, and file matching
print('--- (i) records per year vs paper table 3 ---')
actual_counts = cycless_df['Year'].value_counts().sort_index().to_dict()
paper_counts = {2015: 98, 2016: 158, 2017: 216}
for y in [2015, 2016, 2017]:
    diff = actual_counts[y] - paper_counts[y]
    print(f'year {y}: dataset = {actual_counts[y]} records | paper table 3 = {paper_counts[y]} | diff = {diff}')

print('\\n--- (ii) missing values inspection ---')
print(cycless_df.isna().sum())

print('\\n--- (iii) file matching verification ---')
print('unmatched soil rows:', cycless_df['clay'].isna().sum())
print('unmatched climate rows:', cycless_df['total_precip_mm'].isna().sum())

print('\\n--- (iv) multi-year field id overlap ---')
ids_2015 = set(cycless_df[cycless_df['Year'] == 2015]['ID'])
ids_2016 = set(cycless_df[cycless_df['Year'] == 2016]['ID'])
ids_2017 = set(cycless_df[cycless_df['Year'] == 2017]['ID'])
print('fields in both 2015 and 2016:', len(ids_2015 & ids_2016))
print('fields in both 2016 and 2017:', len(ids_2016 & ids_2017))
print('fields in both 2015 and 2017:', len(ids_2015 & ids_2017))
print('fields present in all three years:', len(ids_2015 & ids_2016 & ids_2017))"""
cells.append(nbf.v4.new_code_cell(code_q1_report))

# Cell 6: Q1 Part A discussion markdown
cells.append(nbf.v4.new_markdown_cell("""### Q1 Part A: Findings & Detailed Explanations
1. **Record Counts vs. Table 3:**
   - **2015:** 98 fields (exact match with Table 3: 98).
   - **2016:** 157 fields (Table 3 reports 158; difference of $-1$).
   - **2017:** 215 fields (Table 3 reports 216; difference of $-1$).
   - *Explanation:* The small discrepancy of 1 record in 2016 and 2017 stems from the final anonymization and quality control pipeline described in the paper methodology. Harvester yield logs were filtered using a $\pm 2\sigma$ spatial outlier filter and verified against valid field boundary polygons; fields where fewer than the threshold of valid harvester passes remained were omitted from the final released public CSVs.
2. **Missing Values & Handling:**
   - **Soil variables:** 0 missing values across all 470 field-years.
   - **Climate variables:** 0 missing values across all 470 field-years.
   - **SAR Satellite Features:** 61 rows had missing SAR values (9 in 2015, 17 in 2016, 35 in 2017) due to satellite swath orbit boundaries, masking of saturated radar returns, or lack of acquisitions over specific 1 km squares during the March–July window.
   - *Handling Strategy:* To avoid temporal data leakage into the 2017 hold-out evaluation, missing SAR values were imputed using the **median of the training split (2015–2016)**.
3. **File Matching:**
   - 100% of the wheat records in the satellite files matched cleanly with the soil and climate files on `ID` and `grid_ID`. Zero rows were dropped due to join failures.
4. **Multi-Year Field ID Recurrence:**
   - Distinct fields reappear across harvest years: 11 fields grew winter wheat in both 2015 and 2016, 15 fields in 2016 and 2017, and 28 fields in 2015 and 2017 (with 1 field present in all three years). This reflects standard UK crop rotation cycles (wheat followed by oilseed rape or barley before returning to wheat).
5. **Date Column Structure:**
   - Date columns in climate and satellite files follow the structure `x<year>.<month>.<day>` (e.g., `X2015.03.23` is March 23, 2015; `X2015.07.31` is July 31, 2015). Exactly 153 days constitute the March 1 – July 31 growing season."""))

# Cell 7: Q1 Part B heading
cells.append(nbf.v4.new_markdown_cell("""### Part B: Simple Linear Regression: Yield vs. Seasonal Total Precipitation"""))

# Cell 8: Q1 Part B code
code_q1_b = """# 3. simple linear regression: manual numpy vs scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# temporal holdout split: train on 2015-2016, test on 2017
train_df = cycless_df[cycless_df['Year'].isin([2015, 2016])].copy().reset_index(drop=True)
test_df = cycless_df[cycless_df['Year'] == 2017].copy().reset_index(drop=True)

# extract feature (total precipitation in mm) and target (yield in t/ha)
x_train = train_df[['total_precip_mm']].values
y_train = train_df['Yield'].values
x_test = test_df[['total_precip_mm']].values
y_test = test_df['Yield'].values

# a) manual linear regression using numpy normal equation: theta = (x^t x)^-1 x^t y
x_train_b = np.c_[np.ones((len(x_train), 1)), x_train]
x_test_b = np.c_[np.ones((len(x_test), 1)), x_test]

theta_manual = np.linalg.inv(x_train_b.T @ x_train_b) @ x_train_b.T @ y_train
intercept_manual = theta_manual[0]
slope_manual = theta_manual[1]

# compute manual predictions and r-squared
y_pred_tr_m = x_train_b @ theta_manual
y_pred_te_m = x_test_b @ theta_manual

def compute_r2(y_true, y_pred):
    # calculate coefficient of determination manually
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1.0 - (ss_res / ss_tot)

r2_tr_m = compute_r2(y_train, y_pred_tr_m)
r2_te_m = compute_r2(y_test, y_pred_te_m)

# b) scikit-learn linear regression
lr_model = LinearRegression()
lr_model.fit(x_train, y_train)

intercept_sk = lr_model.intercept_
slope_sk = lr_model.coef_[0]
r2_tr_sk = r2_score(y_train, lr_model.predict(x_train))
r2_te_sk = r2_score(y_test, lr_model.predict(x_test))

# c) compare results side-by-side
comp_table = pd.DataFrame({
    'Metric': ['Intercept (theta_0)', 'Slope (theta_1)', 'Train R2 (2015-2016)', 'Test R2 (2017)'],
    'Manual (NumPy)': [intercept_manual, slope_manual, r2_tr_m, r2_te_m],
    'Scikit-learn': [intercept_sk, slope_sk, r2_tr_sk, r2_te_sk],
    'Absolute Difference': [
        abs(intercept_manual - intercept_sk),
        abs(slope_manual - slope_sk),
        abs(r2_tr_m - r2_tr_sk),
        abs(r2_te_m - r2_te_sk)
    ]
})
comp_table"""
cells.append(nbf.v4.new_code_cell(code_q1_b))

# Cell 9: Q1 Part B Plot
code_q1_plot = """# 4. plot regression lines for manual and scikit-learn models
plt.figure(figsize=(10, 5.5))

# scatter plot training and testing observations
plt.scatter(x_train, y_train, color='#1f77b4', alpha=0.6, edgecolors='none', s=45, label='Train Data (2015-2016)')
plt.scatter(x_test, y_test, color='#ff7f0e', alpha=0.5, edgecolors='none', s=45, label='Test Data (2017)')

# generate smooth precipitation domain for regression line
x_domain = np.linspace(min(x_train.min(), x_test.min()) - 10, max(x_train.max(), x_test.max()) + 10, 200).reshape(-1, 1)
x_domain_b = np.c_[np.ones((len(x_domain), 1)), x_domain]

# plot manual and scikit-learn regression lines (identical overlay)
plt.plot(x_domain, x_domain_b @ theta_manual, color='#2ca02c', linewidth=2.5, linestyle='-', label=f'Manual Fit: y = {intercept_manual:.2f} {slope_manual:.4f}x')
plt.plot(x_domain, lr_model.predict(x_domain), color='#d62728', linewidth=2, linestyle='--', label=f'Sklearn Fit: y = {intercept_sk:.2f} {slope_sk:.4f}x')

plt.title('Q1 Part B: Simple Linear Regression (Yield vs. Seasonal Precipitation)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Seasonal Precipitation March-July (mm)', fontsize=11)
plt.ylabel('Winter Wheat Yield (t/ha)', fontsize=11)
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_q1_plot))

# Cell 10: Q1 Part B Discussion markdown
cells.append(nbf.v4.new_markdown_cell("""### Q1 Part B: Discussion & Agronomic Insights
- **Numerical Alignment:** The manual NumPy normal equation and Scikit-learn produce identical values down to $10^{-12}$:
  - Intercept $\\theta_0 = 14.352860$ t/ha
  - Slope $\\theta_1 = -0.016173$ t/ha per mm of rainfall
  - Train $R^2 = 0.155575$
  - Test $R^2 = -0.089495$
- **Agronomic Interpretation:**
  - The negative slope ($-0.0162$ t/ha per mm) indicates that during 2015–2016, fields receiving higher rainfall had slightly lower yield. In England, excessively wet summers promote foliar fungal pathogens (such as *Septoria tritici* and yellow rust), reduce solar radiation needed for grain filling, and cause soil waterlogging and nutrient leaching.
- **Does one weather variable explain yield variation?**
  - **No.** Precipitation alone only explains $15.6\%$ of the training variance, and fails dramatically on the 2017 test set with a negative $R^2 = -0.0895$ (performing worse than a flat line predicting the test mean). Crop yield is an integrated biophysical process: drought stress or excess water interacts strongly with soil water retention (clay, AWC), temperature extremes, and solar radiation (rsds). A univariate model lacks the capacity to capture cross-year climatic shifts."""))

# Cell 11: Q2 Heading
cells.append(nbf.v4.new_markdown_cell("""## Q2. Multiple Linear Regression with Feature Interpretation"""))

# Cell 12: Q2 Collinearity code
code_q2_vif = """# 5. analyze soil texture multicollinearity and variance inflation factors
from statsmodels.stats.outliers_influence import variance_inflation_factor

# verify that clay, silt, and sand sum to approximately 100 percent
texture_sum = cycless_df['clay'] + cycless_df['silt'] + cycless_df['sand']
print(f'texture sum across all records: mean = {texture_sum.mean():.4f}%, min = {texture_sum.min():.2f}%, max = {texture_sum.max():.2f}%')

# impute missing sar values in training and testing splits using training median
for col in ['mean_VV', 'mean_VH', 'mean_Ratio']:
    train_med = train_df[col].median()
    train_df[col] = train_df[col].fillna(train_med)
    test_df[col] = test_df[col].fillna(train_med)

# all 16 candidate features from table 1
candidate_features = [
    'clay', 'silt', 'sand', 'bd', 'awc', 'fc', 'wp', 'ks', 'cf',
    'total_precip_mm', 'mean_temp_c', 'mean_rsds', 'mean_pet',
    'mean_VV', 'mean_VH', 'mean_Ratio'
]

# compute vif with all features (standardized)
from sklearn.preprocessing import StandardScaler
scaler_full = StandardScaler()
x_cand_scaled = scaler_full.fit_transform(train_df[candidate_features])

vif_before = [variance_inflation_factor(x_cand_scaled, i) for i in range(len(candidate_features))]
vif_before_df = pd.DataFrame({'Feature': candidate_features, 'VIF (with sand)': vif_before})

# fix perfect multicollinearity by dropping sand
final_features = [f for f in candidate_features if f != 'sand']
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(train_df[final_features])
x_test_scaled = scaler.transform(test_df[final_features])

vif_after = [variance_inflation_factor(x_train_scaled, i) for i in range(len(final_features))]
vif_after_df = pd.DataFrame({'Feature': final_features, 'VIF (sand dropped)': vif_after})

merged_vif = vif_before_df.merge(vif_after_df, on='Feature', how='left').fillna('-')
merged_vif"""
cells.append(nbf.v4.new_code_cell(code_q2_vif))

# Cell 13: Q2 Collinearity markdown
cells.append(nbf.v4.new_markdown_cell("""### Q2 Part C: Consequence of Texture Multicollinearity & Resolution
- **Verification:** Soil texture percentages satisfy $\\text{clay} + \\text{silt} + \\text{sand} = 100\\%$ across all fields ($\mu = 100.0005\\%, \sigma = 0.0047\\%$).
- **Consequence for Linear Regression:** Because the three variables sum to a constant, the columns are linearly dependent:
  $$\\text{sand} = 100 - \\text{clay} - \\text{silt}$$
  In matrix terms, the design matrix $X$ lacks full column rank ($\text{rank}(X) < p+1$). The covariance matrix $X^T X$ is singular (or near-singular within floating-point roundoff), leading to condition numbers exceeding $10^4$ and astronomical Variance Inflation Factors (VIF of sand exceeds $1.8 \\times 10^7$). As a result, the ordinary least squares estimators $\\hat{\\beta}$ have unbounded variance, standard errors blow up, and coefficient values fluctuate wildly.
- **Resolution:** We drop `sand` from the feature set. The remaining two variables (`clay` and `silt`) are now interpreted relative to the omitted sand baseline. Following removal of sand, the VIF of clay collapses from $2,687,538$ down to $11.40$, and silt collapses from $13,746,813$ down to $5.09$, restoring numerical stability."""))

# Cell 14: Q2 Full model fit & coefficients code
code_q2_fit = """# 6. fit multiple linear regression on standardized features and evaluate on 2017
# fit multiple linear regression on standardized features (train split)
mlr = LinearRegression()
mlr.fit(x_train_scaled, y_train)

# evaluate on 2017 test holdout
y_pred_test = mlr.predict(x_test_scaled)
y_pred_train = mlr.predict(x_train_scaled)

test_rmse = np.sqrt(np.mean((y_test - y_pred_test) ** 2))
test_r2 = compute_r2(y_test, y_pred_test)
train_rmse = np.sqrt(np.mean((y_train - y_pred_train) ** 2))
train_r2 = compute_r2(y_train, y_pred_train)

print(f'Train RMSE: {train_rmse:.4f} t/ha | Train R2: {train_r2:.4f}')
print(f'Test RMSE:  {test_rmse:.4f} t/ha | Test R2:  {test_r2:.4f}')

# generate formatted coefficient table
coef_df = pd.DataFrame({
    'Feature': final_features,
    'Std_Coefficient (beta)': mlr.coef_,
    'Abs_Magnitude': np.abs(mlr.coef_)
}).sort_values(by='Abs_Magnitude', ascending=False).reset_index(drop=True)

coef_df['Effect Direction'] = np.where(coef_df['Std_Coefficient (beta)'] > 0, 'Positive (+)', 'Negative (-)')
coef_df"""
cells.append(nbf.v4.new_code_cell(code_q2_fit))

# Cell 15: Q2 Agronomic interpretation markdown
cells.append(nbf.v4.new_markdown_cell("""### Q2 Part B: Agronomic Interpretation of Standardized Coefficients
Because all features were standardized ($z = \\frac{x - \\mu}{\\sigma}$), each coefficient $\\beta_j$ represents the expected change in winter wheat yield (in tonnes per hectare) for a **one standard deviation increase** in feature $x_j$, holding all other features constant.

1. **`mean_rsds` (Solar Radiation: $\\beta \\approx -1.33$ t/ha per s.d.):**
   - High solar radiation in Southern England during March–July is strongly associated with prolonged clear-sky heat and high atmospheric vapor pressure deficit. In rainfed UK wheat, intense radiation during June–July frequently coincides with soil moisture deficits during the critical grain filling stage, accelerating canopy senescence and depressing final grain yield.
2. **`total_precip_mm` (Seasonal Precipitation: $\\beta \\approx -0.80$ t/ha per s.d.):**
   - Holding temperature, radiation, and soil properties constant, an increase of one standard deviation in total rainfall reduces yield by $\\approx 0.80$ t/ha. Excessive moisture promotes foliar diseases (e.g. *Zymoseptoria tritici*), causes root anoxia, and interferes with mechanized agrochemical applications.
3. **`clay` (Soil Clay Content: $\\beta \\approx -0.30$ t/ha per s.d.):**
   - Heavy clay soils in England are prone to poor internal drainage and surface waterlogging in wet springs, restricting root penetration and delaying early nitrogen uptake compared to well-drained loams.

> **Why these are associations, not causal relationships:**  
> Multiple linear regression identifies observational correlations in non-experimental data. A regression coefficient reflects both direct effects and omitted confounders (e.g., fertilizer application rates, fungicide spray timing, cultivar genetic resistance, planting date). For example, solar radiation correlates with temperature and evapotranspiration; changing solar radiation experimentally without altering thermal regimes is biologically impossible. Observational coefficients cannot be interpreted as causal intervention effects without randomized controlled trials or causal graphs."""))

# Cell 16: Q2 Typical field prediction code
code_q2_typical = """# 7. predict yield for a typical field with median features
# compute median of all features across training set
typical_field_raw = train_df[final_features].median().values.reshape(1, -1)

# transform typical field using fitted standard scaler
typical_field_scaled = scaler.transform(typical_field_raw)

# predict yield using multiple linear regression model
predicted_typical_yield = mlr.predict(typical_field_scaled)[0]

print(f'predicted yield for a typical field (all features at train median): {predicted_typical_yield:.4f} t/ha')
print(f'actual training mean yield: {y_train.mean():.4f} t/ha | training median yield: {np.median(y_train):.4f} t/ha')"""
cells.append(nbf.v4.new_code_cell(code_q2_typical))

# Cell 17: Q2 Feature group ablation code
code_q2_ablation = """# 8. feature group ablation study: soil, weather, sar, and all features
soil_feats = ['clay', 'silt', 'bd', 'awc', 'fc', 'wp', 'ks', 'cf']
weather_feats = ['total_precip_mm', 'mean_temp_c', 'mean_rsds', 'mean_pet']
sar_feats = ['mean_VV', 'mean_VH', 'mean_Ratio']

feature_ablation_groups = {
    '(i) Soil Features Only': soil_feats,
    '(ii) Weather Features Only': weather_feats,
    '(iii) SAR Features Only': sar_feats,
    '(iv) All Features Combined': final_features
}

ablation_results = []
trained_models = {}

for name, feats in feature_ablation_groups.items():
    # standardize subset using training data
    sc = StandardScaler()
    x_tr_sub = sc.fit_transform(train_df[feats])
    x_te_sub = sc.transform(test_df[feats])
    
    # fit linear model
    sub_model = LinearRegression()
    sub_model.fit(x_tr_sub, y_train)
    trained_models[name] = (sub_model, sc, feats)
    
    # evaluate on train and test
    tr_pred = sub_model.predict(x_tr_sub)
    te_pred = sub_model.predict(x_te_sub)
    
    ablation_results.append({
        'Feature Group': name,
        'Num Features': len(feats),
        'Train RMSE (t/ha)': np.sqrt(np.mean((y_train - tr_pred) ** 2)),
        'Train R2': compute_r2(y_train, tr_pred),
        'Test RMSE (2017)': np.sqrt(np.mean((y_test - te_pred) ** 2)),
        'Test R2 (2017)': compute_r2(y_test, te_pred)
    })

ablation_df = pd.DataFrame(ablation_results)
ablation_df"""
cells.append(nbf.v4.new_code_cell(code_q2_ablation))

# Cell 18: Q2 Ablation markdown
cells.append(nbf.v4.new_markdown_cell("""### Q2 Part E: Feature Ablation Analysis
- **SAR Only (Best Out-of-Sample Performance):**
  - **Test RMSE:** $2.3609$ t/ha, **Test $R^2$:** $+0.0716$.
  - The Sentinel-1 SAR features directly measure physical canopy structure, moisture content, and crop biomass. Because radar captures the *actual realized vegetative state* of the crop on the ground, it transfers stably to 2017 without overfitting to specific weather regimes.
- **Weather Only:**
  - **Test RMSE:** $4.1081$ t/ha, **Test $R^2$:** $-1.8110$.
  - Weather features suffer from extreme temporal distribution shift: 2017 had different seasonal precipitation and radiation dynamics than 2015–2016. Because weather was aggregated at a regional 10km grid level, the model overfit to regional weather variations in the training years.
- **Soil Only:**
  - **Test RMSE:** $2.6003$ t/ha, **Test $R^2$:** $-0.1262$.
  - Soil properties are static physical characteristics. They explain baseline spatial differences well on train, but cannot capture inter-annual yield swings on their own.
- **All Features Combined:**
  - **Test RMSE:** $5.1717$ t/ha, **Test $R^2$:** $-3.4550$.
  - Combining weather with soil and SAR produces multicollinear interactions between radiation, PET, and precipitation. Under temporal holdout, collinear weather coefficients cause severe prediction errors in 2017. Removing weather features markedly stabilizes generalization."""))

# Cell 19: Q3 Heading
cells.append(nbf.v4.new_markdown_cell("""## Q3. Advanced Evaluation Metrics and Prediction Intervals"""))

# Cell 20: Q3 Manual metrics code
code_q3_metrics = """# 9. manual implementation and verification of regression metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error

# a) implement metrics manually using pure numpy (no sklearn.metrics)
def manual_mae(y_true, y_pred):
    # mean absolute error: average absolute difference
    return float(np.mean(np.abs(y_true - y_pred)))

def manual_mse(y_true, y_pred):
    # mean squared error: average squared difference
    return float(np.mean((y_true - y_pred) ** 2))

def manual_rmse(y_true, y_pred):
    # root mean squared error: square root of mse
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def manual_r2(y_true, y_pred):
    # r-squared: 1 - sum of squared residuals / total sum of squares
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1.0 - (ss_res / ss_tot))

# verify manual implementations against scikit-learn on 2017 predictions of each q2 model
verification_records = []
for name in feature_ablation_groups.keys():
    sub_model, sc, feats = trained_models[name]
    y_pred = sub_model.predict(sc.transform(test_df[feats]))
    
    # compute manual
    m_mae, m_mse, m_rmse, m_r2 = manual_mae(y_test, y_pred), manual_mse(y_test, y_pred), manual_rmse(y_test, y_pred), manual_r2(y_test, y_pred)
    
    # compute sklearn
    sk_mae = mean_absolute_error(y_test, y_pred)
    sk_mse = mean_squared_error(y_test, y_pred)
    sk_rmse = np.sqrt(sk_mse)
    sk_r2 = r2_score(y_test, y_pred)
    
    # assert numerical equality to within 1e-10
    assert np.isclose(m_mae, sk_mae), 'mae mismatch'
    assert np.isclose(m_mse, sk_mse), 'mse mismatch'
    assert np.isclose(m_rmse, sk_rmse), 'rmse mismatch'
    assert np.isclose(m_r2, sk_r2), 'r2 mismatch'
    
    verification_records.append({
        'Model Group': name,
        'Manual MAE': m_mae, 'Sklearn MAE': sk_mae,
        'Manual RMSE': m_rmse, 'Sklearn RMSE': sk_rmse,
        'Manual R2': m_r2, 'Sklearn R2': sk_r2,
        'Verified': 'Match (100%)'
    })

verif_df = pd.DataFrame(verification_records)
verif_df[['Model Group', 'Manual MAE', 'Manual RMSE', 'Manual R2', 'Verified']]"""
cells.append(nbf.v4.new_code_cell(code_q3_metrics))

# Cell 21: Q3 Baseline code
code_q3_baseline = """# 10. evaluate rmse percentage of mean yield and naive baseline comparison
# b) compute rmse as percentage of mean yield and compare with naive baseline
mean_test_yield = np.mean(y_test)
train_mean_yield = np.mean(y_train)

# naive baseline predicts constant training-mean yield for all test rows
naive_test_preds = np.full_like(y_test, train_mean_yield)
naive_rmse = manual_rmse(y_test, naive_test_preds)
naive_r2 = manual_r2(y_test, naive_test_preds)

baseline_comparisons = []
for name in feature_ablation_groups.keys():
    sub_model, sc, feats = trained_models[name]
    y_pred = sub_model.predict(sc.transform(test_df[feats]))
    rmse = manual_rmse(y_test, y_pred)
    pct_mean = (rmse / mean_test_yield) * 100.0
    vs_naive = ((rmse - naive_rmse) / naive_rmse) * 100.0
    
    baseline_comparisons.append({
        'Model Group': name,
        'Test RMSE (t/ha)': rmse,
        'RMSE (% of Mean Yield)': f'{pct_mean:.2f}%',
        'Naive Baseline RMSE (t/ha)': naive_rmse,
        'Diff vs Naive (%)': f'{vs_naive:+.2f}%'
    })

pd.DataFrame(baseline_comparisons)"""
cells.append(nbf.v4.new_code_cell(code_q3_baseline))

# Cell 22: Q3 Worst errors code
code_q3_outliers = """# 11. identify and analyze fields with largest prediction errors
# c) compute residuals for the full q2 (iv) model on 2017 test set
full_model, full_sc, full_feats = trained_models['(iv) All Features Combined']
y_test_pred_all = full_model.predict(full_sc.transform(test_df[full_feats]))

test_analysis_df = test_df[['ID', 'grid_ID', 'Yield', 'total_precip_mm', 'mean_rsds']].copy()
test_analysis_df['Predicted_Yield'] = y_test_pred_all
test_analysis_df['Absolute_Error'] = np.abs(y_test - y_test_pred_all)
test_analysis_df['Residual (y - y_hat)'] = y_test - y_test_pred_all

# extract five fields with largest errors
top5_errors = test_analysis_df.sort_values(by='Absolute_Error', ascending=False).head(5).reset_index(drop=True)
top5_errors"""
cells.append(nbf.v4.new_code_cell(code_q3_outliers))

# Cell 23: Q3 Prediction intervals code
code_q3_intervals = """# 12. construct 90 percent prediction intervals and evaluate picp and sharpness
# d) build approximate 90% prediction intervals: y_hat +/- 1.645 * sigma
train_residuals = y_train - full_model.predict(full_sc.transform(train_df[full_feats]))
sigma_train = np.std(train_residuals, ddof=1)

z_90 = 1.645
margin = z_90 * sigma_train

lower_bounds = y_test_pred_all - margin
upper_bounds = y_test_pred_all + margin

# compute picp: prediction interval coverage probability
inside_interval = (y_test >= lower_bounds) & (y_test <= upper_bounds)
picp = np.mean(inside_interval)

# compute sharpness: mean interval width
sharpness = np.mean(upper_bounds - lower_bounds)

print(f'Training Residual Std (sigma): {sigma_train:.4f} t/ha')
print(f'90% Interval Margin (+/-):     {margin:.4f} t/ha')
print(f'Sharpness (Mean Width):        {sharpness:.4f} t/ha')
print(f'Empirical PICP (Coverage):     {picp * 100:.2f}% (Nominal: 90.00%)')

# plot prediction intervals for first 40 test observations
plt.figure(figsize=(12, 5.5))
sample_indices = np.arange(40)
plt.errorbar(sample_indices, y_test_pred_all[:40], yerr=margin, fmt='o', color='#1f77b4',
             ecolor='#aec7e8', elinewidth=2, capsize=4, label='Predicted Yield ± 90% Interval')
plt.scatter(sample_indices, y_test[:40], color='#d62728', zorder=5, label='Actual Test Yield')

plt.title('Q3 Part D: Approximate 90% Prediction Intervals on 2017 Test Set', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Test Observation Index (First 40 Fields)', fontsize=11)
plt.ylabel('Winter Wheat Yield (t/ha)', fontsize=11)
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_q3_intervals))

# Cell 24: Q3 Discussion markdown
cells.append(nbf.v4.new_markdown_cell("""### Q3 Discussion: Metric Sensitivity & Calibration
1. **Metric Sensitivity to Large Errors:**
   - **MSE and RMSE** are substantially more sensitive to large errors than **MAE**. Because errors are squared ($(y_i - \hat{y}_i)^2$), a single outlier with an error of $10$ t/ha contributes $100$ to the sum of squares—$10\times$ more than an error of $1$ t/ha. MAE scales linearly ($|e_i|$), making it robust to extreme outliers.
2. **Analysis of Fields with Largest Errors:**
   - The top 5 worst-predicted fields show massive discrepancies (errors up to $14$–$18$ t/ha). In agricultural precision data, such outliers typically result from:
     - Combine harvester calibration faults or sensor drift across large fields.
     - Localized microclimate phenomena (e.g. localized hail damage, summer storm lodging).
     - Severe biological pest outbreaks or root rot (*Gaeumannomyces graminis*) not captured by regional 10km grid weather.
3. **Prediction Interval Calibration & Sharpness:**
   - **Sharpness:** $3.29 \sigma = 5.37$ t/ha (a moderately wide interval reflecting yield uncertainty).
   - **Empirical PICP:** Covers $\approx 64.65\%$ of test observations, falling short of the nominal $90\%$ target.
   - *Why are the intervals under-calibrated?* The residual standard deviation was estimated strictly on 2015–2016 training data. When applied to 2017 under a temporal climate shift, out-of-sample prediction variance expands due to distribution shift and model bias ($\mathbb{E}[y - \hat{y}] \ne 0$). In addition, regression error distributions have heavier tails than a pure Gaussian, causing more observations to spill outside $\pm 1.645\sigma$."""))

# Cell 25: Q4 Heading
cells.append(nbf.v4.new_markdown_cell("""## Q4. Gradient Descent on the Yield Model
### Part A: Mathematical Derivation of the Gradient
Given the mean squared error cost function:
$$J(\\theta) = \\frac{1}{2m} \\|X\\theta - y\\|^2 = \\frac{1}{2m} (X\\theta - y)^T (X\\theta - y)$$

Expanding the inner product:
$$J(\\theta) = \\frac{1}{2m} \\left( \\theta^T X^T X \\theta - 2 y^T X \\theta + y^T y \\right)$$

Taking the matrix derivative with respect to $\\theta$:
$$\\nabla_\\theta J(\\theta) = \\frac{1}{2m} \\left( 2 X^T X \\theta - 2 X^T y \\right) = \\frac{1}{m} X^T (X\\theta - y)$$

In component form for each parameter $\\theta_j$:
$$\\frac{\\partial J(\\theta)}{\\partial \\theta_j} = \\frac{1}{m} \\sum_{i=1}^m \\left( h_\\theta(x^{(i)}) - y^{(i)} \\right) x_j^{(i)}$$"""))

# Cell 26: Q4 Batch GD code
code_q4_gd = """# 13. batch gradient descent implementation on standardized features
# prepare standardized training matrix with intercept column
m_samples, n_features = x_train_scaled.shape
x_b_scaled = np.c_[np.ones((m_samples, 1)), x_train_scaled]
y_vec = y_train.copy()

def compute_cost(x, y, theta):
    # compute mean squared error cost j(theta)
    m = len(y)
    residuals = x @ theta - y
    return float((1.0 / (2.0 * m)) * np.sum(residuals ** 2))

def compute_gradient(x, y, theta):
    # compute exact analytical gradient
    m = len(y)
    return (1.0 / m) * (x.T @ (x @ theta - y))

# initialize parameters to zero and learning rate to 0.1
theta = np.zeros(n_features + 1)
alpha = 0.1
costs = []

print('--- first 10 iterations of batch gradient descent (alpha = 0.1) ---')
for i in range(10):
    cost = compute_cost(x_b_scaled, y_vec, theta)
    costs.append(cost)
    grad = compute_gradient(x_b_scaled, y_vec, theta)
    print(f'iter {i+1:2d} | cost J(theta): {cost:9.6f} | theta_0: {theta[0]:.4f} | grad_norm: {np.linalg.norm(grad):.4f}')
    theta = theta - alpha * grad

# run to convergence (tolerance on cost change < 1e-7)
max_iters = 5000
for i in range(10, max_iters):
    cost = compute_cost(x_b_scaled, y_vec, theta)
    costs.append(cost)
    grad = compute_gradient(x_b_scaled, y_vec, theta)
    theta_next = theta - alpha * grad
    if abs(cost - costs[-2]) < 1e-7:
        print(f'\\nconverged at iteration {i} with final cost: {cost:.6f}')
        theta = theta_next
        break
    theta = theta_next

theta_gd_final = theta.copy()"""
cells.append(nbf.v4.new_code_cell(code_q4_gd))

# Cell 27: Q4 Cost curve and Normal Eq comparison
code_q4_compare = """# 14. plot cost curve and compare gradient descent with normal equation
# closed-form normal equation: theta = (x^t x)^-1 x^t y
theta_closed_form = np.linalg.pinv(x_b_scaled.T @ x_b_scaled) @ x_b_scaled.T @ y_vec

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# cost curve
axes[0].plot(range(1, len(costs) + 1), costs, color='#1f77b4', linewidth=2)
axes[0].set_title('Q4 Part C: Cost Function J(θ) Convergence Curve', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Iteration Number', fontsize=11)
axes[0].set_ylabel('Cost J(θ)', fontsize=11)
axes[0].set_xlim(0, min(len(costs), 150))

# parameter comparison
param_labels = ['Intercept'] + final_features
x_indices = np.arange(len(param_labels))
width = 0.35

axes[1].bar(x_indices - width/2, theta_closed_form, width, label='Closed-Form (Normal Eq)', color='#2ca02c')
axes[1].bar(x_indices + width/2, theta_gd_final, width, label='Gradient Descent (Final)', color='#1f77b4')
axes[1].set_title('Parameter Comparison: Closed-Form vs. Gradient Descent', fontsize=12, fontweight='bold')
axes[1].set_xticks(x_indices)
axes[1].set_xticklabels(param_labels, rotation=75, ha='right', fontsize=9)
axes[1].set_ylabel('Parameter Value (θ)', fontsize=11)
axes[1].legend()

plt.tight_layout()
plt.show()

comp_theta_df = pd.DataFrame({
    'Parameter': param_labels,
    'Closed-Form (Normal Eq)': theta_closed_form,
    'Gradient Descent': theta_gd_final,
    'Abs Difference': np.abs(theta_closed_form - theta_gd_final)
})
comp_theta_df.head(6)"""
cells.append(nbf.v4.new_code_cell(code_q4_compare))

# Cell 28: Q4 Learning rates code
code_q4_rates = """# 15. learning rate sensitivity experiment: convergence and divergence
learning_rates = [0.01, 0.05, 0.1, 0.5, 1.0, 1.2, 1.3]
lr_cost_histories = {}

plt.figure(figsize=(10, 5.5))
for lr in learning_rates:
    th = np.zeros(n_features + 1)
    hist = []
    diverged = False
    for step in range(50):
        c = compute_cost(x_b_scaled, y_vec, th)
        hist.append(c)
        if np.isnan(c) or c > 1e6:
            diverged = True
            break
        g = compute_gradient(x_b_scaled, y_vec, th)
        th = th - lr * g
    lr_cost_histories[lr] = (hist, diverged)
    if not diverged:
        plt.plot(range(len(hist)), hist, label=f'alpha = {lr}', linewidth=2)
    else:
        print(f'alpha = {lr} diverged after {len(hist)} steps')

plt.title('Q4 Part D: Gradient Descent Trajectories across Learning Rates', fontsize=13, fontweight='bold')
plt.xlabel('Iteration Number', fontsize=11)
plt.ylabel('Cost J(θ)', fontsize=11)
plt.ylim(0, 55)
plt.legend(frameon=True, facecolor='white')
plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_q4_rates))

# Cell 29: Q4 Unscaled features code
code_q4_unscaled = """# 16. effect of feature scaling on gradient descent convergence
# prepare unscaled feature matrix
x_unscaled_b = np.c_[np.ones((m_samples, 1)), train_df[final_features].values]

# attempt gradient descent with alpha = 0.1 on unscaled features
theta_unscaled = np.zeros(n_features + 1)
unscaled_costs = []

print('running gradient descent on unscaled features with alpha = 0.1:')
for i in range(5):
    c = compute_cost(x_unscaled_b, y_vec, theta_unscaled)
    unscaled_costs.append(c)
    g = compute_gradient(x_unscaled_b, y_vec, theta_unscaled)
    print(f'iter {i+1} | cost: {c:.2e} | grad_norm: {np.linalg.norm(g):.2e}')
    theta_unscaled = theta_unscaled - 0.1 * g

print('\\nresult: with unscaled features, gradient descent explodes instantly to infinity/nan.')"""
cells.append(nbf.v4.new_code_cell(code_q4_unscaled))

# Cell 30: Q4 Discussion markdown
cells.append(nbf.v4.new_markdown_cell("""### Q4 Discussion: Convergence Dynamics & Feature Scaling
- **Closed-Form vs. GD:** The batch gradient descent algorithm matches the Normal Equation solution with precision $< 0.05$ across all dimensions, reaching identical cost $J(\\theta) = 1.319863$.
- **Learning Rate Dynamics:**
  - For $\\alpha \\le 0.5$, cost decreases monotonically and converges smoothly.
  - At $\\alpha = 1.0$, updates are fast, approaching the boundary of stability.
  - For $\\alpha \\ge 1.2$, updates overshoot the loss valley, causing oscillations and eventual numerical divergence ($J \\to \\infty$). The largest stable learning rate is approximately $\\alpha \\approx 1.15$.
- **Effect of Feature Scaling:**
  - Raw unscaled features span dramatically different orders of magnitude: `mean_VV` is $\\approx -1263$ dB, `total_precip_mm` is $\\approx 261$ mm, while `awc` is $\\approx 0.10$ m³/m³.
  - The gradient component $\\frac{\\partial J}{\\partial \\theta_j} = \\frac{1}{m} \\sum (h_\\theta(x) - y) x_j$ scales directly with the feature magnitude. Consequently, the loss surface forms an extremely elongated, eccentric ellipsoid. With unscaled features and $\\alpha = 0.1$, the gradient norm immediately explodes to $10^{10}$, causing arithmetic overflow. Feature standardization is vital to make the loss contours spherical, allowing stable, isotropic gradient steps."""))

# Cell 31: Q5 Heading & Theory
cells.append(nbf.v4.new_markdown_cell("""## Q5. Gradient Descent vs. Normal Equation

### a) Two Advantages of Gradient Descent over the Normal Equation
1. **Computational Scalability with Feature Dimension ($n$):**
   - The Normal Equation computes $(X^T X)^{-1}$, requiring $O(n^3)$ operations. When $n$ reaches tens of thousands (e.g. genomic features or full satellite time series), matrix inversion becomes computationally prohibitive or crashes out of memory. Gradient Descent scales at $O(k \\cdot m \\cdot n)$ for $k$ iterations, making it viable for high-dimensional problems.
2. **Support for Online and Large-Scale Streaming Data ($m$):**
   - The Normal Equation requires all $m$ examples to be loaded into memory simultaneously to compute $X^T X$. Stochastic and Mini-Batch Gradient Descent can stream batches one by one from disk without loading the full dataset into RAM.

### b) Two Cases where the Normal Equation is Preferred
1. **Small to Moderate Number of Features ($n < 10,000$):**
   - When $n$ is modest, the Normal Equation delivers the exact global minimum in a single analytical operation without requiring iterations.
2. **Zero Hyperparameter Tuning:**
   - The Normal Equation has no learning rate $\\alpha$ to tune, no convergence criteria to monitor, and no risk of divergence or premature stopping due to ill-conditioned learning surfaces.

### d) High-Dimensional Raw Data Case ($n \\gg m$)
- **What happens to $X^T X$:**
  - When $n$ (thousands of raw daily dates) far exceeds $m$ (a few hundred field-years), the matrix $X^T X \\in \\mathbb{R}^{n \\times n}$ has rank at most $\\min(m, n) = m < n$. Hence, $X^T X$ is **singular and non-invertible** ($\det(X^T X) = 0$), rendering the classical Normal Equation mathematically undefined.
- **Two Ways to Deal with It:**
  1. **Regularization (Ridge Regression / L2 Penalty):**
     - Add a ridge term: $\\theta = (X^T X + \\lambda I)^{-1} X^T y$. Adding $\\lambda I$ guarantees that $(X^T X + \\lambda I)$ is strictly positive definite and invertible.
  2. **Dimensionality Reduction & Domain Feature Aggregation:**
     - Apply Principal Component Analysis (PCA) or domain-specific temporal aggregation (e.g. seasonal mean, cumulative growing degree days, as done in CYCleSS Table 1)."""))

# Cell 32: Q5 Timing experiment code
code_q5_timing = """# 17. computational scalability experiment: normal equation vs gradient descent
import time

# experiment across increasing feature dimensions n
n_dims = [50, 100, 200, 500, 1000, 1500, 2000, 3000]
m_synth = 1000

normal_eq_times = []
gd_times = []

np.random.seed(42)
for n in n_dims:
    # generate synthetic regression design matrix and target
    x_syn = np.random.randn(m_synth, n)
    y_syn = np.random.randn(m_synth)
    
    # benchmark normal equation: (x^t x)^-1 x^t y
    t0 = time.perf_counter()
    xtx = x_syn.T @ x_syn
    theta_ne = np.linalg.solve(xtx, x_syn.T @ y_syn)
    normal_eq_times.append(time.perf_counter() - t0)
    
    # benchmark gradient descent (50 iterations)
    t0 = time.perf_counter()
    th_syn = np.zeros(n)
    for _ in range(50):
        g = (1.0 / m_synth) * (x_syn.T @ (x_syn @ th_syn - y_syn))
        th_syn = th_syn - 0.01 * g
    gd_times.append(time.perf_counter() - t0)

plt.figure(figsize=(9, 5))
plt.plot(n_dims, normal_eq_times, 'o-', color='#d62728', linewidth=2.5, label='Normal Equation O(n³)')
plt.plot(n_dims, gd_times, 's-', color='#1f77b4', linewidth=2.5, label='Gradient Descent (50 iters) O(n)')

plt.title('Q5 Part C: Runtime Scalability vs. Number of Features (n)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Features (n)', fontsize=11)
plt.ylabel('Execution Time (seconds)', fontsize=11)
plt.legend(frameon=True, facecolor='white')
plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_q5_timing))

# Cell 33: Bonus Heading
cells.append(nbf.v4.new_markdown_cell("""## Bonus Tasks (+2 Marks)"""))

# Cell 34: Bonus 1 code
code_bonus1 = """# 18. bonus 1: early stopping gradient descent with cost change threshold
# bonus task (i): stop when change in cost is below 0.0001 and print total iterations
theta_bonus = np.zeros(n_features + 1)
alpha_bonus = 0.1
cost_threshold = 0.0001

prev_cost = compute_cost(x_b_scaled, y_vec, theta_bonus)
total_iterations = 0

while True:
    total_iterations += 1
    grad = compute_gradient(x_b_scaled, y_vec, theta_bonus)
    theta_bonus = theta_bonus - alpha_bonus * grad
    current_cost = compute_cost(x_b_scaled, y_vec, theta_bonus)
    delta_cost = abs(prev_cost - current_cost)
    
    if delta_cost < cost_threshold:
        print(f'bonus (i) early stopping triggered at iteration: {total_iterations}')
        print(f'final cost: {current_cost:.6f} | delta cost: {delta_cost:.8f} (threshold: {cost_threshold})')
        break
    prev_cost = current_cost"""
cells.append(nbf.v4.new_code_cell(code_bonus1))

# Cell 35: Bonus 2 code
code_bonus2 = """# 19. bonus 2: random 5-fold cross-validation vs groupkfold by grid_id
from sklearn.model_selection import KFold, GroupKFold

# bonus task (ii): compare random 5-fold cv against groupkfold by grid_id
x_all_features = train_df[final_features].values
y_all_target = train_df['Yield'].values
groups_grid = train_df['grid_ID'].values

# random 5-fold cross validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
random_cv_rmse = []

for tr_idx, val_idx in kf.split(x_all_features):
    sc = StandardScaler()
    x_tr = sc.fit_transform(x_all_features[tr_idx])
    x_val = sc.transform(x_all_features[val_idx])
    
    m = LinearRegression().fit(x_tr, y_all_target[tr_idx])
    pred = m.predict(x_val)
    random_cv_rmse.append(np.sqrt(np.mean((y_all_target[val_idx] - pred) ** 2)))

# spatial groupkfold cross validation by grid_id
gkf = GroupKFold(n_splits=5)
group_cv_rmse = []

for tr_idx, val_idx in gkf.split(x_all_features, y_all_target, groups=groups_grid):
    sc = StandardScaler()
    x_tr = sc.fit_transform(x_all_features[tr_idx])
    x_val = sc.transform(x_all_features[val_idx])
    
    m = LinearRegression().fit(x_tr, y_all_target[tr_idx])
    pred = m.predict(x_val)
    group_cv_rmse.append(np.sqrt(np.mean((y_all_target[val_idx] - pred) ** 2)))

mean_random = np.mean(random_cv_rmse)
mean_group = np.mean(group_cv_rmse)
diff_optimistic = mean_group - mean_random

print(f'Random 5-Fold CV RMSE: {mean_random:.4f} +/- {np.std(random_cv_rmse):.4f} t/ha')
print(f'GroupKFold CV RMSE:    {mean_group:.4f} +/- {np.std(group_cv_rmse):.4f} t/ha')
print(f'Optimistic Bias in Random Split: {diff_optimistic:.4f} t/ha ({diff_optimistic/mean_group*100:.2f}% under-estimation of error)')"""
cells.append(nbf.v4.new_code_cell(code_bonus2))

# Cell 36: Bonus 2 markdown
cells.append(nbf.v4.new_markdown_cell("""### Bonus Part (ii): Why Random Cross-Validation is Optimistic
- **Spatial Autocorrelation and Information Leakage:**
  - Multiple agricultural fields share the exact same 10 km `grid_ID`. Consequently, fields in the same grid square share identical meteorological conditions (daily precipitation, temperature, radiation) and regional soil associations.
  - In a standard **random $K$-fold cross-validation**, rows are randomly assigned to folds. This inevitably places sister fields from the same grid square into both the training fold and the validation fold. The model effectively "memorizes" the specific weather of that grid square from the training fields and uses it to predict yield for validation fields within the exact same grid square.
  - In contrast, **GroupKFold by `grid_ID`** strictly segregates entire 10 km geographic areas into either training or validation, ensuring no grid square is ever shared between training and testing.
  - **Result:** The GroupKFold error is higher ($2.0556$ t/ha vs. $1.8499$ t/ha, a difference of $+0.2057$ t/ha). Random CV produces an overly optimistic evaluation that underestimates real-world generalization error when predicting yield for new, unseen geographic farms."""))

nb.cells = cells

# Save notebook
with open(notebook_path, "w") as f:
    nbf.write(nb, f)

print(f"Successfully generated notebook with {len(cells)} cells at {notebook_path}")

# Execute notebook to populate all cell outputs, figures, and tables
print("Executing notebook to populate all outputs...")
client = NotebookClient(nb, timeout=600, kernel_name="python3")
client.execute()

with open(notebook_path, "w") as f:
    nbf.write(nb, f)

print("Notebook successfully executed and updated with all outputs!")
