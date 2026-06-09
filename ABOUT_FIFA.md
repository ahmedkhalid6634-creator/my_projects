# FIFA 24 Data Cleaning, Analysis, and Visualization Pipeline

A robust, project-first Python data engineering and exploratory data analysis (EDA) pipeline designed to clean, normalize, and visualize a raw dataset of over 5,000 FIFA 24 players. This project ad[...]

---

## 🚀 Key Project Capabilities
- **Heuristic Stat Reconstruction:** Engineered custom statistical alignment functions to dynamically impute missing tactical variables by modeling feature correlations.
- **Text Encoding & Unicode Normalization:** Built algorithmic text-cleansing routines to isolate and purge corrupted multi-lingual player profiles, stripping anomalies like unexpected currency mar[...]
- **Exploratory Data Analysis (EDA):** Generated automated statistical data profiling suites detailing high-dimensional variable correlations.
- **Dynamic Dashboards:** Developed interactive, browser-ready visual analytics to drill down into player market valuations, traits, and operational clusters.

---

## 🛠️ Data Pipeline Architecture & Implementation

### 1. Data Cleaning & Preprocessing
The ingestion pipeline cleans the raw dataset through a strict four-stage sequential workflow:
1. **Text Normalization & Decoding Correction:** Iterates through structural string records to extract, correct, and rebuild corrupted player names and attributes impacted by standard Unicode tran[...]
2. **Missing Value Recovery & Feature Engineering:** Resolves structural gaps within defensive attribute columns. Specifically catches missing data within legacy metrics like the `marking` column,[...]
3. **Strict Datatype Standardization:** Programmatically casts heavily mixed or object-based series into standardized, memory-efficient numeric (`int64`, `float64`) or structured categorical types[...]
4. **Contextual Deduplication:** Runs multi-field uniqueness checks using anchor variables (such as player `age` combined with core identity attributes) to safely isolate and prune duplicated entr[...]

### 2. Core Functional Modules

#### `def_awareness_function`
When migrating or cleaning player performance metrics, critical operational attributes like *Defensive Awareness* (traditionally known or structured as `marking`) are frequently omitted or corrupt[...]
* **Methodology:** It maps the statistical correlation between adjacent, highly-dependent defensive metrics: **Standing Tackle**, **Sliding Tackle**, and **Interceptions**. 
* **Formula Principle:** While heuristic in nature, the function models the defensive profile of a player based on these active metrics, applying a weighted correlation index to approximate the mi[...]

#### `normalize_functions`
A robust text-processing module deployed to catch text encoding anomalies, multi-lingual script corruptions, and rogue syntax markers.
* **Target Anomalies:** Detects and scrubs non-alphanumeric artifacts, out-of-context currency strings (like standalone `$` characters), and encoding errors.
* **Primary Use Case:** Rebuilding accurate player names. Because the original dataset contains global nomenclature with complex diacritics and accents, improper file compression or database expor[...]

---

## ⚠️ Important Statistical Assumptions & Data Drift Notes

Because certain features were missing or unrecoverable from the initial raw data pull, a few calculated margins of error should be considered when reviewing the outputs:

* **Overall Rating Variance (3-8 Points Drift):** Due to missing structural variables—most notably player **Positions** and **International Reputation**—the generated overall metrics may exper[...]
* **Defensive Awareness Drift:** Because the `def_awareness_function` relies entirely on adjacent active defensive actions (tackling and interceptions), the calculated output may drift by an **unk[...]

---

## 📊 Analytical Outputs & Reports

The pipeline auto-generates two comprehensive analytical reports inside the repository for stakeholders to review project outcomes:

### 📥 Static Performance Audit Summary (`fifa_data_report.html`)
A static, publication-ready overall data report detailing the health and statistical characteristics of the post-cleaned dataset.
* Contains macro-level summaries of all clean player variables.
* Incorporates static high-resolution correlation matrices highlighting how player performance stats map to market values and salaries.
* Highlights distribution plots, outlier zones, and critical data cleanup KPIs.

### 🎮 Interactive Analytics Dashboard (`fifa_dashboard.html`)
A dynamic, client-facing interactive visual dashboard built to allow seamless data exploration directly in the browser.
* Employs interactive components to filter and sort through the 5,000+ player dataset dynamically.
* Features responsive multi-axis scatter plots, interactive distribution charts, and drill-down tooltips to analyze player value patterns, age brackets, and skill correlations on the fly.

---

## 📂 Repository Structure

```text
├── data/
│   ├── raw_fifa_data.csv          # Original messy dataset
│   └── cleaned_fifa_data.csv      # Output processed dataset
├── modules/
│   ├── def_awareness.py           # Contains def_awareness_function
│   └── normalize.py               # Text cleaning & Unicode normalize functions
├── pipeline.py                    # Main execution script running stages 1 to 4
├── fifa_data_report.html          # Summarized analytical static report
└── fifa_dashboard.html            # Interactive visualizations dashboard
```
