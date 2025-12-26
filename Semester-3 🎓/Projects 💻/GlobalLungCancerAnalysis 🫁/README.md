# 🫁 Global Lung Cancer Analysis

> *A Python-based data analysis project investigating the correlation between global air pollution and lung cancer incidence*

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## 📊 Project Overview

This collaborative data science project analyzes the relationship between global air pollution levels (PM2.5) and lung cancer incidence across 890,000 patient records from 27 European countries and 6,985 cities worldwide.

**🎯 Goal:** Identify patterns and correlations between environmental pollution and lung cancer outcomes, while analyzing risk factors affecting patient survival rates.

---

## 🛠️ Technologies Used

- **Python 3.12** - Core programming language
- **Pandas & NumPy** - Data manipulation and analysis
- **Matplotlib & Seaborn** - Data visualization
- **Jupyter Notebook** - Interactive analysis environment
- **Plotly** - Interactive visualizations

---

## 📈 Analysis Summary

### **Analysis 1: Lung Cancer Patient Data** *(Uzair Atiq)*
- Preprocessed 890,000 patient records from 27 European countries (2014-2024)
- Analyzed survival rates (22% overall survival)
- Examined risk factors: smoking status, BMI, comorbidities, treatment types
- Normalized and cleaned medical data for further analysis

### **Analysis 2: Air Pollution Trends** *(Laiba Sajjad)*
- Processed pollution data from 6,985 cities across 133 countries (2017-2023)
- Handled missing values using linear interpolation and country-level means
- Analyzed PM2.5 levels across continents
- Identified pollution trends and patterns globally

### **Analysis 3: Correlation & Insights** *(Sanaullah Turab)*
- Investigated correlation between air pollution and lung cancer incidence
- Compared European health outcomes with global pollution patterns
- Generated data-driven insights and visualizations
- Provided recommendations based on findings

---

## ✨ Strengths

- **Large-scale datasets** covering 890K+ patient records and 6,985 cities
- **Comprehensive preprocessing** with robust handling of missing values
- **Multi-dimensional analysis** combining medical and environmental data
- **Collaborative approach** with specialized analysis components
- **Professional documentation** with detailed findings reports

## ⚠️ Shortcomings

- Limited to European patient data (not globally representative)
- Time period mismatch between datasets (2014-2024 vs 2017-2023)
- Correlation doesn't imply causation
- Missing data in earlier pollution years (69% in 2017)

---

## 👥 Team

| Team Member | Role | Contribution |
|-------------|------|-------------|
| **Uzair Atiq** | Data Analyst | Analysis 1 - Lung Cancer Patient Data |
| **Laiba Sajjad** | Data Analyst | Analysis 2 - Air Pollution Trends |
| **Sanaullah Turab** | Data Analyst | Analysis 3 - Correlation & Insights |

---

## 🛠️ Technologies Stack

| Technology               | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| **Python 3.12**          | Primary programming language                 |
| **Pandas & NumPy**       | Data manipulation and numerical computations |
| **Matplotlib & Seaborn** | Data visualization and plotting              |
| **Scikit-learn**         | Data preprocessing and normalization         |
| **SciPy**                | Statistical analysis and hypothesis testing  |
| **Jupyter Notebook**     | Interactive analysis environment             |

---

## 📁 Project Structure

```
global-lung-cancer-analysis/
├── datasets/                      # Raw and processed datasets
│   ├── lung_cancer_part1.csv     # Medical data (Part 1)
│   ├── lung_cancer_part2.csv     # Medical data (Part 2)
│   ├── lung_cancer_part3.csv     # Medical data (Part 3)
│   └── air_pollution.csv         # Global pollution data
│
├── notebooks/                     # Jupyter notebooks
│   └── LungCancer-Analysis.ipynb # Main analysis notebook
│
├── scripts/                       # Python preprocessing scripts
│   ├── data_preprocessing.py     # Medical data preprocessing
│   └── air_pollution_preprocessing.py  # Pollution data preprocessing
│
├── visuals/                       # Generated visualizations
│   └── (plots, charts, heatmaps)
│
├── findings/                      # Analysis reports
│   ├── lung_cancer_report.md
│   ├── air_pollution_report.md
│   └── data_preprocessing_report.md
│
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.12+
pip (Python package manager)
```

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/sanaullah-turab/global-lung-cancer-analysis.git
   cd global-lung-cancer-analysis
   ```

2. **Install required packages**

   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn scipy jupyter
   ```

3. **Launch Jupyter Notebook**
   ```bash
   cd notebooks
   jupyter notebook LungCancer-Analysis.ipynb
   ```

---

## 📊 Key Analyses

### 1. Data Preprocessing

- Duplicate removal and missing value handling
- MinMaxScaler normalization (0-1 range)
- Time series interpolation for pollution data
- Dataset splitting for memory efficiency

### 2. Exploratory Data Analysis

- Patient demographic distributions
- Cancer stage and treatment type analysis
- Smoking status and comorbidity prevalence
- Global pollution trend analysis (2017-2023)

### 3. Statistical Analysis

- Correlation analysis between variables
- Hypothesis testing (t-tests, ANOVA)
- Survival rate analysis by risk factors
- Pollution-cancer correlation studies

### 4. Visualizations

- Distribution plots and histograms
- Box plots for comparative analysis
- Heatmaps for correlation matrices
- Time series trend visualizations
- Geographic pollution mapping

---

## 📈 Key Findings

### Medical Dataset Insights

- **Survival Rate**: 22.01% overall survival rate
- **Gender Distribution**: 50/50 split (Male/Female)
- **Cancer Stages**: Evenly distributed across Stage I-IV
- **Top Comorbidities**:
  - Hypertension: 75% prevalence
  - Asthma: 47% prevalence
  - Cirrhosis: 22.6% prevalence

### Air Pollution Insights

- **Global Coverage**: 133 countries, 6,985 cities
- **Trend**: Declining pollution levels from 2017 to 2023
- **Geographic Variation**: Significant differences across continents
- **Data Completeness**: 100% complete after preprocessing

### Correlation Analysis

- Analysis of pollution levels vs. lung cancer incidence
- Risk factor impact on survival outcomes
- Treatment effectiveness across cancer stages
- Geographic health outcome variations

---

## 🔬 Methodology

1. **Data Collection**: Aggregation of medical records and pollution measurements
2. **Data Cleaning**: Duplicate removal, missing value imputation, normalization
3. **Exploratory Analysis**: Statistical summaries, distribution analysis
4. **Visualization**: Creation of insightful charts and graphs
5. **Statistical Testing**: Hypothesis testing and correlation analysis
6. **Interpretation**: Drawing data-driven conclusions and recommendations

---

## 📝 Documentation

Detailed documentation available in the `findings/` directory:

- [Lung Cancer Analysis Report](findings/lung_cancer_report.md)
- [Air Pollution Analysis Report](findings/air_pollution_report.md)
- [Data Preprocessing Report](findings/data_preprocessing_report.md)

---

## 👨‍💻 Author

**Sanaullah Turab**  
Enrollment: 01-136242-026  
Class: BSAI - Section 3A  
Date: December 2025

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Dataset sources and providers
- Python scientific computing community
- Open-source contributors

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ using Python

</div>
